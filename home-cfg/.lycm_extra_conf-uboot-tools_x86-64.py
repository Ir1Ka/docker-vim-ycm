import os.path as p
import subprocess

DIR_OF_THIS_SCRIPT = p.abspath(p.dirname(__file__))
ARCH = 'x86_64'
#CROSS_COMPILE = 'x86_64-linux-gnuabi64-'
CROSS_COMPILE=''
TARGET = 'x86_64-linux-gnu'
CC = CROSS_COMPILE + 'gcc'

TOP_DIR = p.abspath(DIR_OF_THIS_SCRIPT + '/' + '..')

c_inc = [
    [
        '-I',
        [
        ],
    ],
]

c_inc_top = [
    [
        '-idirafter',
        [
            'include',
            'include2',
        ],
    ],
]

c_extra_flags = [
    '--target=' + TARGET,
    '-Werror',
    '-Wall',
#    '-pedantic',
    '-DTEXT_BASE=0x0C800000',
    '-DUSE_HOSTCC',
    '-g',
    '-O',
    '-c',
]

def CFlags(filename):
    c_flags = []

    c_flags.extend(c_extra_flags)

    for _c_inc in c_inc:
        _flg, dirs = _c_inc
        for dir in dirs:
            abs_dir = p.abspath(DIR_OF_THIS_SCRIPT + '/' + dir)
            c_flags.extend([_flg, abs_dir])

    for _c_inc in c_inc_top:
        _flg, dirs = _c_inc
        for dir in dirs:
            abs_dir = p.abspath(TOP_DIR + '/' + dir)
            c_flags.extend([_flg, abs_dir])

    return c_flags
