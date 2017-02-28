import os
from lz_cli import LZ_ROOT

opj = os.path.join
WORKSPACE = opj(LZ_ROOT, 'workspace')
RESULT_DIR = opj(WORKSPACE, 'results')
LOG_DIR = opj(WORKSPACE, 'log')
TMP_DIR = opj(WORKSPACE, 'tmp')

DEV_DIR = opj(LZ_ROOT, 'DEV')
BACCARAT_DIR = opj(DEV_DIR, 'BACCARAT')
DER_DIR = opj(DEV_DIR, 'DER')
PHOTON_DETECTION_DIR = opj(DEV_DIR, 'PhotonDetection')

LZ_LUXSIM_PATH = os.environ['LZ_LUXSIM_PATH']
