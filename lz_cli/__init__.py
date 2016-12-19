import os
import logging

LZ_LUXSIM_PATH = os.environ['LZ_LUXSIM_PATH']
LZ_ROOT = os.environ['HEP_PROJECT_ROOT']

LOG = logging.getLogger(__name__)
LOG.setLevel(logging.DEBUG)
# logging to a file
formatter = logging.Formatter(
    '%(asctime)s [%(name)s]  %(levelname)s: %(message)s')

logfile = '/tmp/hepshell_{0}.log'.format(os.geteuid())
if os.path.exists(LZ_ROOT + '/workspace/log'):
    logfile = LZ_ROOT + '/workspace/log/lz.log'
fh = logging.FileHandler(logfile)
fh.setFormatter(formatter)
fh.setLevel(logging.DEBUG)
LOG.addHandler(fh)

# logging to the console
formatter = logging.Formatter('%(message)s')
ch = logging.StreamHandler()
if not os.environ.get("DEBUG", False):
    ch.setLevel(logging.INFO)
else:
    ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
LOG.addHandler(ch)
