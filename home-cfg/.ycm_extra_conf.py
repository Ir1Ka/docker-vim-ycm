# This file is NOT licensed under the GPLv3, which is the license for the rest
# of YouCompleteMe.
#
# Here's the license text for this file:
#
# This is free and unencumbered software released into the public domain.
#
# Anyone is free to copy, modify, publish, use, compile, sell, or
# distribute this software, either in source code form or as a compiled
# binary, for any purpose, commercial or non-commercial, and by any
# means.
#
# In jurisdictions that recognize copyright laws, the author or authors
# of this software dedicate any and all copyright interest in the
# software to the public domain. We make this dedication for the benefit
# of the public at large and to the detriment of our heirs and
# successors. We intend this dedication to be an overt act of
# relinquishment in perpetuity of all present and future rights to this
# software under copyright law.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# For more information, please refer to <http://unlicense.org/>

from distutils.sysconfig import get_python_inc
import platform
import os.path as p
import subprocess
import ycm_core
import sys
import random
import string

DIR_OF_THIS_SCRIPT = p.abspath( p.dirname( __file__ ) )
C_SOURCE_EXTENSIONS = [ '.c' ]
CPP_SOURCE_EXTENSIONS = [ '.cpp', '.cxx', '.cc', '.m', '.mm' ]
L_YCM_EXTRA_CONF = '.lycm_extra_conf.py'

# These are the compilation flags that will be used in case there's no
# compilation database set (by default, one is not set).
# CHANGE THIS LIST OF FLAGS. YES, THIS IS THE DROID YOU HAVE BEEN LOOKING FOR.
c_base_flags = [
'-Wall',
'-Wextra',
'-Werror',
'-Wno-long-long',
'-Wno-variadic-macros',
'-fexceptions',
'-DNDEBUG',
# THIS IS IMPORTANT! Without the '-x' flag, Clang won't know which language to
# use when compiling headers. So it will guess. Badly. So C++ headers will be
# compiled as C headers. You don't want that so ALWAYS specify the '-x' flag.
# For a C project, you would set this to 'c' instead of 'c++'.
'-x',
'c',
]

cpp_base_flags = [
'-Wall',
'-Wextra',
'-Werror',
'-Wno-long-long',
'-Wno-variadic-macros',
'-fexceptions',
'-DNDEBUG',
# THIS IS IMPORTANT! Without the '-x' flag, Clang won't know which language to
# use when compiling headers. So it will guess. Badly. So C++ headers will be
# compiled as C headers. You don't want that so ALWAYS specify the '-x' flag.
# For a C project, you would set this to 'c' instead of 'c++'.
'-x',
'c++',
]

# Set this to the absolute path to the folder (NOT the file!) containing the
# compile_commands.json file to use that instead of 'flags'. See here for
# more details: http://clang.llvm.org/docs/JSONCompilationDatabase.html
#
# You can get CMake to generate this file for you by adding:
#   set( CMAKE_EXPORT_COMPILE_COMMANDS 1 )
# to your CMakeLists.txt file.
#
# Most projects will NOT need to set this to anything; you can just change the
# 'flags' list of compilation flags. Notice that YCM itself uses that approach.
compilation_database_folder = ''

if p.exists( compilation_database_folder ):
  database = ycm_core.CompilationDatabase( compilation_database_folder )
else:
  database = None


def IsHeaderFile( filename ):
  extension = p.splitext( filename )[ 1 ]
  return extension in [ '.h', '.hxx', '.hpp', '.hh' ]


def FindCorrespondingSourceFile( filename ):
  if IsHeaderFile( filename ):
    basename = p.splitext( filename )[ 0 ]
    for extension in CPP_SOURCE_EXTENSIONS + C_SOURCE_EXTENSIONS:
      replacement_file = basename + extension
      if p.exists( replacement_file ):
        return replacement_file
  return filename


def PathToPythonUsedDuringBuild():
  try:
    filepath = p.join( DIR_OF_THIS_SCRIPT, 'PYTHON_USED_DURING_BUILDING' )
    with open( filepath ) as f:
      return f.read().strip()
  # We need to check for IOError for Python 2 and OSError for Python 3.
  except ( IOError, OSError ):
    return None

def FindFile( l_ycm_extra_conf , dir ):
  conf = p.join( dir, l_ycm_extra_conf )
  if p.isfile( conf ):
    return True, dir
  elif dir == '/':
    return False, None
  else:
    dir = p.abspath( p.dirname( dir ) )
    return FindFile( l_ycm_extra_conf, dir )

def LoadLocalYcmExtraConf( filename ):
  found, conf_dir = FindFile( L_YCM_EXTRA_CONF, \
    p.dirname( p.abspath( filename ) ) )
  if not found:
    return None

  sys.path.insert( 0, conf_dir )
  old_dont_write_bytecode = sys.dont_write_bytecode
  sys.dont_write_bytecode = True
  try:
    random_name = ''.join( random.choice( string.ascii_lowercase ) \
      for x in range( 15 ) )
    import importlib
    lmodule = importlib.machinery.SourceFileLoader( \
      random_name, conf_dir + '/' + L_YCM_EXTRA_CONF ).load_module()
  finally:
    sys.dont_write_bytecode = old_dont_write_bytecode
    del sys.path[ 0 ]
  return lmodule

def CFlagsFromFilename( filename ):
  flags = []
  lmodule = LoadLocalYcmExtraConf( filename )
  extension = p.splitext( filename )[1]
  if extension in CPP_SOURCE_EXTENSIONS:
    flags.extend( cpp_base_flags )
    if lmodule and hasattr( lmodule, 'CppFlags' ):
      try:
        _cppflags = lmodule.CppFlags( filename )
        try:
            iter(_cppflags)
        except TypeError:
          raise TypeError( 'Return value of CppFlags must be a iter!' )

        for _cppflag in _cppflags:
          if not isinstance( _cppflag, str ):
            raise Exception( 'Elements of return value of CppFlags',    \
                             'must be str!' )

        flags = _cppflags
      except Exception as e:
        print( 'Invalid CppFlags in',                                   \
               conf_dir + '/' + L_YCM_EXTRA_CONF,                       \
               ':',                                                     \
               e.value,                                                 \
          file=sys.stderr )
  else:
    flags.extend( c_base_flags )
    if lmodule and hasattr( lmodule, 'CFlags' ):
      try:
        _cflags = lmodule.CFlags( filename )
        try:
            iter(_cflags)
        except TypeError:
          raise TypeError( 'Return value of CFlags must be a iter!' )

        for _cflag in _cflags:
          if not isinstance( _cflag, str ):
            raise Exception( 'Elements of return value of CFlags must be str!' )

        flags = _cflags
      except Exception as e:
        print( 'Invalid CFlags in',                                     \
               conf_dir + '/' + L_YCM_EXTRA_CONF,                       \
               ':',                                                     \
               e.value,                                                 \
          file=sys.stderr )

  return flags + [ '-iquote', p.dirname( p.abspath( filename ) ) ]

def DatabaseFromFilename( filename ):
  folder = p.abspath( p.dirname( filename ) )
  found, folder = FindFile( 'compile_commands.json', folder )
  if found:
    return ycm_core.CompilationDatabase( folder )
  else:
    return None

def Settings( **kwargs ):
  language = kwargs[ 'language' ]

  if language == 'cfamily':
    # If the file is a header, try to find the corresponding source file and
    # retrieve its flags from the compilation database if using one. This is
    # necessary since compilation databases don't have entries for header files.
    # In addition, use this source file as the translation unit. This makes it
    # possible to jump from a declaration in the header file to its definition
    # in the corresponding source file.
    filename = FindCorrespondingSourceFile( kwargs[ 'filename' ] )

    global database
    if not database:
      database = DatabaseFromFilename( filename )

    if not database:
      return {
        'flags': CFlagsFromFilename( filename ),
        'include_paths_relative_to_dir': DIR_OF_THIS_SCRIPT,
        'override_filename': filename
      }

    compilation_info = database.GetCompilationInfoForFile( filename )
    if not compilation_info.compiler_flags_:
      return {}

    # Bear in mind that compilation_info.compiler_flags_ does NOT return a
    # python list, but a "list-like" StringVec object.
    final_flags = list( compilation_info.compiler_flags_ )

    return {
      'flags': final_flags,
      'include_paths_relative_to_dir': compilation_info.compiler_working_dir_,
      'override_filename': filename
    }

  if language == 'python':
    return {
      'interpreter_path': PathToPythonUsedDuringBuild()
    }

  return {}


def GetStandardLibraryIndexInSysPath( sys_path ):
  for index, path in enumerate( sys_path ):
    if p.isfile( p.join( path, 'os.py' ) ):
      return index
  raise RuntimeError( 'Could not find standard library path in Python path.' )


def PythonSysPath( **kwargs ):
  sys_path = kwargs[ 'sys_path' ]

  interpreter_path = kwargs[ 'interpreter_path' ]
  major_version = subprocess.check_output( [
    interpreter_path, '-c', 'import sys; print( sys.version_info[ 0 ] )' ]
  ).rstrip().decode( 'utf8' )

  return sys_path
