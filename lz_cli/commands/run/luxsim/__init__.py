'''
    run:
        Just an example run for luxsim.

    Usage:
        run luxsim <config file>

'''
import os
import shutil
import logging
import glob
from operator import itemgetter

import hepshell
from lz_cli.setup import LZ_LUXSIM_PATH, RESULT_DIR, TMP_DIR

LOG = logging.getLogger(__name__)

LUX_SIM_EXE = 'LUXSimExecutable'
LUX_ROOT_CONVERTER = 'tools/LUXRootConverter'
LUX_MCTRUTH = 'tools/LUXMCTruth'


class Command(hepshell.Command):

    def __init__(self, path=__file__, doc=__doc__):
        super(Command, self).__init__(path, doc)
        self.__output_file = None
        self.__output_dir = RESULT_DIR

    def run(self, args, variables):
        input_file = os.path.abspath(args[0])
        LOG.info('Using simulation config: {0}'.format(input_file))
        self._replace_output_dir(input_file)
        LOG.info('Snapshot at: {0}'.format(self.__input_file))

        commands = [
            'cd {LZ_LUXSIM_PATH}',
            './{LUX_SIM_EXE} {input_file}'
        ]

        all_commands = ' && '.join(commands)
        all_commands = all_commands.format(
            LZ_LUXSIM_PATH=LZ_LUXSIM_PATH,
            LUX_SIM_EXE=LUX_SIM_EXE,
            input_file=input_file,
        )
        from hepshell.interpreter import call
        code, _, _ = call(all_commands, LOG, shell=True)
        if code == 0:
            # now find the actual output file (has a random number in the end)
            output_file_prefix = self._get_parameter_from_input_file(
                '/LUXSim/io/outputName', self.__input_file
            )
            self.__output_file = self._find_output_file(output_file_prefix)
            self.__text = 'Produced file {0}'.format(self.__output_file)
            return True
        else:
            return False

    def _get_parameter_from_input_file(self, parameter, input_file):
        result = None
        with open(input_file) as f:
            for line in f.readlines():
                if parameter in line:
                    result = line.split(' ')[1].strip('\n')
        return result

    def _replace_output_dir(self, input_file):
        output_dir = self._get_parameter_from_input_file(
            '/LUXSim/io/outputDir', input_file
        )
        self.__input_file = os.path.join(TMP_DIR, os.path.basename(input_file))
        content = ""
        with open(input_file) as f:
            content = f.read()
        with open(self.__input_file, 'w') as f:
            f.write(content.replace(output_dir, RESULT_DIR))

    def _find_output_file(self, output_file_prefix):
        path = os.path.join(self.__output_dir, output_file_prefix)
        path += '*.bin'
        files = glob.glob(path)
        if len(files) == 1:
            return files[0]

        stats = [(f, os.path.getmtime(f)) for f in files]
        sorted_stats = tuple(sorted(stats, key=itemgetter(1), reverse=True))
        return sorted_stats[0][0]
