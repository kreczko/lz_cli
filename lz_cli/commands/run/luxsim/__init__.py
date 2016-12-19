'''
    run:
        Just an example run for luxsim.

    Usage:
        run luxsim <config file>

'''
import hepshell
import os
from lz_cli.setup import LZ_LUXSIM_PATH
import logging
LOG = logging.getLogger(__name__)

LUX_SIM_EXE = 'LUXSimExecutable'
LUX_ROOT_CONVERTER = 'tools/LUXRootConverter'
LUX_MCTRUTH = 'tools/LUXMCTruth'


class Command(hepshell.Command):

    def __init__(self, path=__file__, doc=__doc__):
        super(Command, self).__init__(path, doc)

    def run(self, args, variables):
        '''
            cd /cvmfs/lz.opensciencegrid.org/LUXSim/release-4.4.6/
            ./LUXSimExecutable /scratch/phxlk/lz/test.mac
            tools/LUXRootConverter /scratch/phxlk/lz/SourceTube_all_AmLi_100_791235223.bin
            tools/LUXMCTruth /scratch/phxlk/lz/SourceTube_all_AmLi_100_791235223.root
        '''
        input_file = os.path.abspath(args[0])

        output_folder = os.path.dirname(input_file)
        output_file = self._get_outputfile(input_file)
        LOG.info('Using simulation config: {0}'.format(input_file))
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
        call(all_commands, LOG, shell=True)

    def _get_outputfile(self, input_file):
        '''
            Search for /LUXSim/io/outputName in input_file
        '''
        output_file = ''
        with open(input_file) as f:
            for line in f.readlines():
                if '/LUXSim/io/outputName' in line:
                    output_file = line.split(' ')[1]
        return output_file
