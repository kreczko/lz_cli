
import luigi
import os
from plumbum import local
import sys
from . import ExternalFileTask

class CompileTask(luigi.Task):
    code_location = luigi.Parameter()
    target = luigi.Parameter()
    clean = luigi.BoolParameter(
        default=False,
        significant=False,
    )

    def initialized(self):
        if self.clean:
            self.make_clean()
        return True

    def output(self):
        target = os.path.join(self.code_location, self.target)
        return luigi.LocalTarget(target)

    def requires(self):
        return [ExternalFileTask(path=self.code_location)]

    def run(self):
        with local.cwd(self.code_location):
            (local['make'] > sys.stdout)('-j2')

    def make_clean(self):
        with local.cwd(self.code_location):
            (local['make'] > sys.stdout)('clean')


def run(code_location, target, clean=False):
    import logging
    logger = logging.getLogger('luigi-interface')
    logger.setLevel(logging.ERROR)
    parameters = ['--code-location', code_location, '--target',
                  target]
    if clean:
        parameters.append('--clean')
    luigi.run(parameters, local_scheduler=True, main_task_cls=CompileTask)
