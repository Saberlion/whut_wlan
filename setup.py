import sys
 
from cx_Freeze import setup, Executable
 
copyDependentFiles=True
silent = True
buildOptions = dict(
  packages = [], excludes = [],
  includes = ["lxml", "lxml.etree", "gzip", "encodings.cp949", "encodings.utf_8", "encodings.ascii"],
)
 
name = 'lancher'
 
if sys.platform == 'win32':
  name = name + '.exe'
 
base = None
#if sys.platform == "win32":
#    base = "Win32GUI"
 
executables = [
  Executable('lancher.py', base = base, targetName = name,
             compress = True,
            )
]
 
setup(name='wwl',
      version = '0.1',
      description = 'whut wlan lancher',
      options = dict(build_exe = buildOptions),
      executables = executables)