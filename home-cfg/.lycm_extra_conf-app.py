import os.path as p
import subprocess

DIR_OF_THIS_SCRIPT = p.abspath(p.dirname(__file__))
ARCH = 'arm64'
CROSS_COMPILE = 'aarch64-linux-gnuabi64-'
TARGET = 'aarch64-linux-gnu'
CC = CROSS_COMPILE + 'gcc'

c_inc_dirs = [
]

# APP directory
APP_DIR     = p.abspath(DIR_OF_THIS_SCRIPT)
c_inc_app_dirs = [
]

# APP parent directory if app ref it.
APP_TOP_DIR = p.abspath(DIR_OF_THIS_SCRIPT + '/' + '..')
c_inc_app_top_dirs = [
]

# Project top source directory if app ref it
TOP_DIR     = p.abspath(DIR_OF_THIS_SCRIPT + '/' + '../../..')
c_inc_top_dirs = [
]

c_extra_flags = [
    '--target=' + TARGET,
    '-Werror',
    '-Wall',
    '-Wno-format-zero-length',
    '-Wno-format-security',
    '-g',
    '-c',
]

def CFlags(filename):
    c_flags = []

    c_flags.extend(c_extra_flags)

    for c_inc_dir in c_inc_dirs:
        abs_c_inc_dir = p.abspath(DIR_OF_THIS_SCRIPT + '/' + c_inc_dir)
        c_flags.extend(['-I', abs_c_inc_dir])

    for c_inc_dir in c_inc_app_dirs:
        abs_c_inc_dir = p.abspath(APP_DIR + '/' + c_inc_dir)
        c_flags.extend(['-I', abs_c_inc_dir])

    for c_inc_dir in c_inc_app_top_dirs:
        abs_c_inc_dir = p.abspath(APP_TOP_DIR + '/' + c_inc_dir)
        c_flags.extend(['-I', abs_c_inc_dir])

    for c_inc_dir in c_inc_top_dirs:
        abs_c_inc_dir = p.abspath(TOP_DIR + '/' + c_inc_dir)
        c_flags.extend(['-I', abs_c_inc_dir])

    return c_flags
