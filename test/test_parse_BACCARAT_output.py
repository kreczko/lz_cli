import unittest
import os
PROJECT_ROOT = os.environ['PROJECT_ROOT']
os.environ['HEP_PROJECT_ROOT'] = PROJECT_ROOT

from lz_cli.setup import BACCARAT_DIR, RESULT_DIR

from lz_cli.commands.run.BACCARAT import parseOutputFile


class TestParseBaccaratOutput(unittest.TestCase):

    def test_parseOutputFile_in_BACCARAT_DIR(self):
        stdout = """

Output saved to ./xenon_photon_4.10.2_1313701282.bin

"""
        output_file = parseOutputFile(stdout)
        self.assertEqual(
            output_file, '{0}/xenon_photon_4.10.2_1313701282.bin'.format(BACCARAT_DIR))

    def test_parseOutputFile_in_RESULT_DIR(self):
        stdout = """

Output saved to {0}/xenon_photon_4.10.2_1313701282.bin

""".format(RESULT_DIR)
        output_file = parseOutputFile(stdout)
        self.assertEqual(
            output_file, '{0}/xenon_photon_4.10.2_1313701282.bin'.format(RESULT_DIR))
