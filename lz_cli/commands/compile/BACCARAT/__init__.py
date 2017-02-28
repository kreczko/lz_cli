"""
    compile BACCARAT:
        Compiles BACCARAT

    Usage:
        compile BACCARAT
"""
import logging
import hepshell
import os
from lz_cli.setup import BACCARAT_DIR
from plumbum import local
import sys

LOG = logging.getLogger(__name__)


class Command(hepshell.Command):

    DEFAULTS = {'clean': False}

    def __init__(self, path=__file__, doc=__doc__):
        super(Command, self).__init__(path, doc)

    def run(self, args, variables):
        self.__prepare(args, variables)
        BAC_EXE = 'BACCARATExecutable'
        from lz_cli.tasks.compile import run
        run(code_location=BACCARAT_DIR, target=BAC_EXE,
            clean=self.__variables['clean'])

        # self.__text = "Work In Progress!\n"
        # bacc_folder = BACCARAT_DIR
        # if not os.path.exists(bacc_folder):
        #     self.__text('Folder {0} does not exist'.format(bacc_folder))
        #     return False
        # cwd = local.cwd
        # local.cwd.chdir(bacc_folder)
        # if self.__variables['clean']:
        #     (local['make'] > sys.stdout)('clean')
        # (local['make'] > sys.stdout)('-j2')
        # local.cwd.chdir(cwd)

        self.__text += "BACCARAT is now ready to use"

        return True
