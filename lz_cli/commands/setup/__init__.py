"""
    setup:
        Prepares the workspace

    Usage:
        setup [--overwrite]

    Parameters:
        overwrite: overwrite the existing workspace
"""
import logging
import hepshell
import os
from lz_cli.setup import WORKSPACE, RESULT_DIR, LOG_DIR

LOG = logging.getLogger(__name__)

def _create_directories(directories):
    for d in directories:
        if not os.path.exists(d):
            os.makedirs(d)

class Command(hepshell.Command):

    DEFAULTS = {'overwrite': False}

    def __init__(self, path=__file__, doc=__doc__):
        super(Command, self).__init__(path, doc)

    def run(self, args, variables):
        self.__prepare(args, variables)
        _create_directories([WORKSPACE, RESULT_DIR, LOG_DIR, TMP_DIR])
        self.__text = "LZ CLI is now ready to use"

        return True
