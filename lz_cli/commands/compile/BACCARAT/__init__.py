"""
    compile BACCARAT:
        Compiles BACCARAT

    Usage:
        compile BACCARAT
"""
import logging
import hepshell
import os
from lz_cli import LZ_ROOT
from plumbum import local
import sys

LOG = logging.getLogger(__name__)

class Command(hepshell.Command):

    DEFAULTS = {'overwrite': False}

    def __init__(self, path=__file__, doc=__doc__):
        super(Command, self).__init__(path, doc)

    def run(self, args, variables):
        self.__prepare(args, variables)
        self.__text = "Work In Progress!"
        bacc_folder = os.path.join(LZ_ROOT, 'DEV', 'BACCARAT')
        if not os.path.exists(bacc_folder):
            self.__text('Folder {0} does not exist'.format(bacc_folder))
            return False
        cwd = local.cwd
        local.cwd.chdir(bacc_folder)
        (local['make'] > sys.stdout)('-j2')
        local.cwd.chdir(cwd)

        self.__text += "BACCARAT is now ready to use"

        return True
