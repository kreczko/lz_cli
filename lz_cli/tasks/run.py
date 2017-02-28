import luigi
from lz_cli.setup import BACCARAT_DIR

from .compile import CompileTask


class RunBaccaratTask(luigi.Task):
    executable = luigi.Parameter(default='BACCARATExecutable')
    input_file = luigi.Parameter()
    recompile = luigi.BoolParameter(default=False)

    def requires(self):
        return [CompileTask(code_location=BACCARAT_DIR,
                            target=self.executable,
                            clean=self.recompile),
                ]

    def output(self):
        # outputfile contains a random hash to the end
        # cannot replicate this here
        return []
