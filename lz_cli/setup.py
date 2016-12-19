import os
from lz_cli import LZ_ROOT

opj = os.path.join
WORKSPACE = opj(LZ_ROOT, 'workspace')
RESULT_DIR = opj(WORKSPACE, 'results')
LOG_DIR = opj(WORKSPACE, 'log')
