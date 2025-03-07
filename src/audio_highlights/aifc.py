"""
Minimal aifc module replacement.
This provides just enough functionality to prevent import errors.
"""

import wave

Error = wave.Error

def open(f, mode=None):
    raise NotImplementedError("This is a stub aifc module. Actual functionality is not implemented.")

def openfp(f, mode=None):
    raise NotImplementedError("This is a stub aifc module. Actual functionality is not implemented.")