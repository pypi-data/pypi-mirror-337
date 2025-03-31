import os as _os
_thispath = _os.path.dirname(_os.path.realpath(__file__))

#==============================================================================

def get(path='.'):
    """Get file path in the JunPy dataset."""
    return f'{_thispath}/{path}'

#==============================================================================
