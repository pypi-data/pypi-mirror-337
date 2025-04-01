from importlib import metadata

from .decompilers.ida import Ida


__version__ = metadata.version("ludi")
