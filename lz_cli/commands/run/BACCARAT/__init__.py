"""
    run BACCARAT:
        Runs the BACCARATExecutable wit the given macro

    Usage:
        run BACCARAT --input_file <path to .mac file> [--output_folder]

    Parameters:
        input_file:
            path to BACCARAT macro file
        output_folder:
            Optional output folder. Default = {RESULT_DIR}
"""
import logging
import hepshell
from lz_cli.setup import BACCARAT_DIR, RESULT_DIR
import os

logger = logging.getLogger(__name__)


def parseOutputFile(stdout):
    token_start = 'Output saved to'
    token_end = '.bin'
    if token_start not in stdout:
        logging.error('Stdout does not contain outputfile information')
        return None
    start = stdout.find(token_start)
    substr = stdout[start:]
    print(substr, stdout[-500:])
    end = substr.find(token_end)
    output = substr[:end + len(token_end)]
    print(output)
    output_file = output.split()[-1]
    print(output_file)
    if './' in output_file:
        output_file = output_file.replace('./', BACCARAT_DIR + '/')
    logger.debug('Found "{0} output file'.format(output_file))
    return output_file


def moveOutputfile(output_file, destination=RESULT_DIR):
    '''
        Moves the BACCARAT output file to the result directory
    '''
    if not os.path.exists(output_file):
        # something went wrong, try to glob
        import glob
        logger.warn(
            'Could not find {0}, looking for {0}*'.format(output_file))
        output_file = glob.glob(output_file + '*')[0]
        if not os.path.exists(output_file):
            logger.error('No output file found.')
            logger.error('Was looking for {0}'.format(output_file))
            return False, None
        logger.warn('Found {0}'.format(output_file))
    import shutil
    new_file = output_file.replace(BACCARAT_DIR, destination)
    if new_file.endswith('.tmp'):
        new_file = new_file.replace('.tmp', '')
    if output_file != new_file:
        logger.debug('Moving output file {0} to {1}'.format(
            output_file, new_file))
        shutil.move(output_file, new_file)
    return True, new_file


def runBACCARAT(input_file):
    BAC_EXE = './BACCARATExecutable'
    commands = [
        'cd {BACCARAT_DIR}',
        '{BAC_EXE} {input_file}',
    ]
    all_in_one = ' && '.join(commands)
    all_in_one = all_in_one.format(
        BACCARAT_DIR=BACCARAT_DIR, BAC_EXE=BAC_EXE, input_file=input_file)
    from hepshell.interpreter import call
    code, stdout, stderr = call(
        [all_in_one], logger, stdout_log_level=logging.INFO, shell=True)
    return code, stdout, stderr


def runBACCARATwithPb(input_file):
    import plumbum
    BAC_EXE = './BACCARATExecutable'
    local = plumbum.local
    s = ''
    with local.cwd(BACCARAT_DIR):
        try:
            s = local[BAC_EXE](input_file)
        except plumbum.commands.processes.ProcessExecutionError as err:
            logger.error('Could not run BACCARAT: {0}'.format(err))
            return -1, s

    return 0, s


class Command(hepshell.Command):
    DEFAULTS = {
        'input_file': '',
        'output_folder': RESULT_DIR,
    }

    def __init__(self, path=__file__, doc=__doc__):
        doc = doc.format(RESULT_DIR=RESULT_DIR)
        super(Command, self).__init__(path, doc)
        self._output_file = None

    def run(self, args, variables):
        self.__prepare(args, variables)
        BAC_EXE = './BACCARATExecutable'

        input_file = self.__variables['input_file']
        if not os.path.exists(input_file):
            self.__text += 'File {0} does not exist'.format(input_file)
            return False
        input_file = os.path.abspath(input_file)
        logger.debug('using input file: %s', input_file)

        # code, stdout = runBACCARATwithPb(input_file)
        code, stdout, _ = runBACCARAT(input_file)

        if code != 0:
            return False

        output_file = parseOutputFile(stdout)
        output_folder = self.__variables['output_folder']
        r, output_file = moveOutputfile(output_file, output_folder)
        if r:
            self._output_file = output_file

        return r

    def getOutputFile(self):
        return self._output_file
