from importlib.metadata import version
from .lazy_import import Libs, Lib

try:
    __version__ = version('lazyimport')
except Exception:
    __version__ = 'unknown'

del version

__all__ = [
    '__version__',
    'Libs',
    'Lib',
]
