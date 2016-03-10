import warnings as _warnings
import os as _os
import shutil

from tempfile import mkdtemp


class TemporaryDirectory(object):
    def __init__(self, suffix="", prefix="tmp", dir=None):
        self._closed = False
        self.name = None
        self.name = mkdtemp(suffix, prefix, dir)

    def __repr__(self):
        return "<{} {!r}>".format(self.__class__.__name__, self.name)

    def __enter__(self):
        return self.name

    def __exit__(self, exc, value, tb):
        shutil.rmtree(self.name)

    _listdir = staticmethod(_os.listdir)
    _path_join = staticmethod(_os.path.join)
    _isdir = staticmethod(_os.path.isdir)
    _islink = staticmethod(_os.path.islink)
    _remove = staticmethod(_os.remove)
    _rmdir = staticmethod(_os.rmdir)
    _warn = _warnings.warn
