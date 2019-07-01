from os.path import dirname, realpath
from os.path import join as pathjoin

_VERSION_PATH = 'version.txt'


def _version():
    here = dirname(realpath(__file__))
    vpath = pathjoin(here, _VERSION_PATH)
    with open(vpath) as f:
        version = f.read().strip()
    return version


version = _version()
