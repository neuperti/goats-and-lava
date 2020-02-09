"""Setup to pack python. Supposed to be run on Linux."""

import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.

for base in ("Win32GUI",):

    buildOptions = dict(packages=[], excludes=[])

    if sys.platform == "win32":
        base = 'win32'
    else:
        base = None

    executables = [
        Executable('main.py', base=base, icon="images/goat_icon.png", targetName='goats&lava')
    ]

    setup(name='Goats & Lava',
          version='0.1',
          description='A fun little variant of battleships, done for a class in university in 2\
    days (and some afterfixes)',
          options=dict(build_exe=buildOptions),
          executables=executables)
