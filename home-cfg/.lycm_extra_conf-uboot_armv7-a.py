import os.path as p
import subprocess

DIR_OF_THIS_SCRIPT = p.abspath(p.dirname(__file__))
ARCH = 'arm'
CROSS_COMPILE = 'arm-none-linux-gnueabi-'
TARGET = 'arm-linux-gnueabi'
CC = CROSS_COMPILE + 'gcc'

TOP_DIR = p.abspath(DIR_OF_THIS_SCRIPT)

c_inc = [
    [
        '-I',
        [
        ],
    ],
]

c_inc_top = [
    [
        '-I',
        [
            'include',
        ],
    ],
]

c_extra_flags = [
    '--target=' + TARGET,
    '-isystem', subprocess.check_output( \
                        [CC, '-print-file-name=include'] \
                    ).decode('utf-8').strip(),
    '-Wall',
#    '-Werror',
#    '-pedantic',
    '-fno-strict-aliasing',
    '-fno-common',
#    '-ffixed-r8',
    '-fpic',
    '-D__KERNEL__',
    '-DTEXT_BASE=0x0C800000',
    '-fno-builtin',
    '-ffreestanding',
    '-nostdinc',
    '-pipe',
    '-DCONFIG_ARM',
    '-D__ARM__',
    '-march=armv7-a',
#    '-mno-thumb-interwork',
    '-mabi=apcs-gnu',
    '-Wstrict-prototypes',
    '-fno-stack-protector',
    '-g2',
    '-Os',
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
