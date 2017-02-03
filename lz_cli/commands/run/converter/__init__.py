"""
    run converter:
        Runs the LUXRootConverter

    Usage:
        run converter <path to .bin file>

"""
import logging
import hepshell

LOG = logging.getLogger(__name__)


class Command(hepshell.Command):

    def __init__(self, path=__file__, doc=__doc__):
        super(Command, self).__init__(path, doc)

    def run(self, args, variables):
        '''
            tools/LUXRootConverter /scratch/phxlk/lz/SourceTube_all_AmLi_100_791235223.bin
        '''
        self.__prepare(args, variables)
        self.__text = "NOT IMPLEMENTED"

        return True
