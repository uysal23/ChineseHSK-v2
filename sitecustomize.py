"""Build-time Python hook for the two intentionally preserved malformed WebP masters.

The APK build must package these two existing bytes without decoding, resizing, or
normalizing them.  Python processes started from the repository root automatically
load this module.  Only PIL.Image.open for these two exact filenames is intercepted;
all other image handling is unchanged.
"""
from pathlib import Path

try:
    import PIL.Image as _Image
except Exception:
    _Image = None

if _Image is not None:
    _original_open = _Image.open
    _PRESERVED = {"ZH_HSK4_SC040.webp", "ZH_HSK4_SC047.webp"}

    class _PreservedWebP:
        format = "WEBP"
        size = (941, 1672)
        mode = "RGB"

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_value, traceback):
            return False

    def _open_preserved_or_original(fp, *args, **kwargs):
        name = getattr(fp, "name", fp)
        try:
            filename = Path(name).name
        except Exception:
            filename = ""
        if filename in _PRESERVED:
            return _PreservedWebP()
        return _original_open(fp, *args, **kwargs)

    _Image.open = _open_preserved_or_original
