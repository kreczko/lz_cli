"""
    run:
        Executes the complete workflow. Currently
        "run luxsim", "run converter", "run luxsim"

    Usage:
        run <path to .mac file>
"""
import logging
import hepshell
from .luxsim import Command as LuxSimCmd
from .converter import Command as LUXRootConverter
from .mctruth import Command as MCTruthCmd

LOG = logging.getLogger(__name__)


class Command(hepshell.Command):

    def __init__(self, path=__file__, doc=__doc__):
        super(Command, self).__init__(path, doc)

    def run(self, args, variables):
        self.__prepare(args, variables)
        luxsim = LuxSimCmd()
        result = luxsim.run(args, variables)
        self.__text = luxsim.__text
        if not result:
            return False
        luxsim_output = luxsim.__output_file

        converter = LUXRootConverter()
        result = converter.run([luxsim_output], variables)
        self.__text += converter.__text
        # get converter output

        if not result:
            return False
        # push it through MCTruth
        mctruth = MCTruthCmd()
        mctruth.run([], variables)

        self.__text += mctruth.__text

        self.__text = luxsim.__text

        return True
