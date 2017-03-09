"""
    benchmark BACCARAT:
        benchmarks BACCARAT by encapsulating 'lz run BACCARAT'

    Usage:
        benchmark BACCARAT [--nevents=<number of events>]

    Parameters:
        nevents: number of events to be produced for the benchmark.
                 Default is "{nevents}"
        process: Which process to run. Default: {process}.
                 Valid values: {processes}
"""
from __future__ import print_function, division
import hepshell
import os
import time
import six
import resource
from lz_cli.setup import RESULT_DIR, TMP_DIR
from ROOT import gROOT
import logging
STREAM = six.StringIO()
from .template import MACRO, PROCESSES

logger = logging.getLogger(__name__)


def get_geant_version():
    '''
        Extracting GEANT4 version from $G4LIB, e.g.
        /cvmfs/lz.opensciencegrid.org/geant4/geant4.9.5.p02/lib64/Geant4-9.5.2
    '''
    # geant4.10.02
    g4lib = os.environ.get('G4LIB')
    tmp = g4lib.split('/')[-1].split('-')[-1]
    tmp2 = '.'.join(tmp.split('.')[:-1])
    version = '4.{0}'.format(tmp2)
    return version


GEANT_VERSION = get_geant_version()
ROOT_VERSION = gROOT.GetVersion().replace('/', '.')


class Benchmark(object):

    def __enter__(self):
        self.usage_start = resource.getrusage(resource.RUSAGE_CHILDREN)
        self.meta_data = {}
        return self

    def __exit__(self, *args):
        self.usage_end = resource.getrusage(resource.RUSAGE_CHILDREN)
        self.duration = self.usage_end.ru_utime - self.usage_start.ru_utime
        # in Kb
        self.rss_usage = self.usage_end.ru_maxrss - self.usage_start.ru_maxrss
        self.meta_data['Duration'] = self.duration
        self.meta_data['RSS (in kB)'] = self.rss_usage

    def to_csv(self, output_file):
        import csv
        with open(output_file, 'wb') as f:
            w = csv.DictWriter(f, self.meta_data.keys())
            w.writeheader()
            w.writerow(self.meta_data)
        logger.info('Written benchmark result file {0}'.format(output_file))


class Command(hepshell.Command):
    DEFAULTS = {
        'nevents': 1000,
        'process': PROCESSES['SingleParticle_opticalphoton'],
        'processes': ','.join(['"{0}"'.format(p) for p in PROCESSES])
    }

    def __init__(self, path=__file__, doc=__doc__):
        doc = doc.format(**Command.DEFAULTS)
        super(Command, self).__init__(path, doc)

    def _write_macro(self):
        macro = MACRO.format(
            output_dir=RESULT_DIR,
            process=self.__variables['process'],
            suffix=GEANT_VERSION,
            nevents=int(self.__variables['nevents']),
        )
        macro_file = os.path.join(TMP_DIR, 'benchmark.mac')
        with open(macro_file, 'w+') as f:
            f.write(macro)
        logger.info('Written benchmark macro file {0}'.format(macro_file))
        return macro_file

    def run(self, args, variables):
        self.__prepare(args, variables)
        self.__text = "Work In Progress!\n"
        self.__variables['input_file'] = self._write_macro()
        self.__variables['nevents'] = int(self.__variables['nevents'])
        output_folder = os.path.join(RESULT_DIR, 'benchmark')
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        self.__variables['output_folder'] = output_folder

        r, b = self.work()
        if not r:
            return False

        self.output_file = r.getOutputFile()
        self.add_meta_data(b)

        print('Ouptutfile:', self.output_file)
        benchmark_file = self.output_file.replace('.bin', '.csv')
        b.to_csv(benchmark_file)
        print('Duration: {0}, RSS: {1}'.format(b.duration, b.rss_usage))

        return True

    def work(self):
        from lz_cli.commands.run.BACCARAT import Command as RunBac
        r = RunBac()
        with Benchmark() as b:
            r.run(self.__args, self.__variables)
        return r, b

    def add_meta_data(self, benchmark):
        nevents = self.__variables['nevents']
        benchmark.meta_data['Process'] = self.__variables['process']
        benchmark.meta_data['# events'] = nevents
        events_per_second = round(nevents / benchmark.duration, 1)
        benchmark.meta_data['Events/s'] = events_per_second
        file_size_in_kb = round(os.path.getsize(self.output_file) / 1024.0, 3)
        benchmark.meta_data['File size (in kb)'] = file_size_in_kb
        benchmark.meta_data['kb/event'] = round(file_size_in_kb / nevents, 3)
        benchmark.meta_data['ROOT Version'] = ROOT_VERSION
        benchmark.meta_data['GEANT Version'] = GEANT_VERSION
