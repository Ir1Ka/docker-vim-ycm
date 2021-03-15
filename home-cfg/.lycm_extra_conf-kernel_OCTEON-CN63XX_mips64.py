import os.path as p
import subprocess

DIR_OF_THIS_SCRIPT = p.abspath(p.dirname(__file__))
ARCH = 'mips'
CROSS_COMPILE = 'mips64-linux-gnuabi64-'
TARGET = 'mips64-linux-gnu'
CC = CROSS_COMPILE + 'gcc'

KDIR_NAME = p.basename(DIR_OF_THIS_SCRIPT)
KERNEL_DIR = p.abspath(DIR_OF_THIS_SCRIPT)
KBUILD_DIR = p.abspath(DIR_OF_THIS_SCRIPT + '/../../../build_dir/linux-octeon/' + KDIR_NAME)

c_inc_dirs = [
]

c_inc_kdirs = [
    'arch/' + ARCH + '/include',
    'include',
    'arch/' + ARCH + '/include/asm/mach-cavium-octeon',
    'arch/' + ARCH + '/include/asm/mach-generic',
]

c_extra_flags = [
    '--target=' + TARGET,
    '-Wno-sign-compare',
    '-std=gnu89',
    '-nostdinc',
    '-isystem', subprocess.check_output( \
                        [CC, '-print-file-name=include'] \
                    ).decode('utf-8').strip(),
    '-include', p.abspath(KBUILD_DIR + '/include/linux/kconfig.h'),
    '-include', p.abspath(KBUILD_DIR + '/include/linux/compiler_types.h'),
    '-include', p.abspath(KBUILD_DIR + '/include/linux/autoconf.h'),
    '-D__KERNEL__',
    '-D"VMLINUX_LOAD_ADDRESS=0xffffffff80100000"',
    '-D"DATAOFFSET=0"',
    '-Wall',
    '-Wundef',
    '-Wstrict-prototypes',
    '-Wno-trigraphs',
    '-fno-strict-aliasing',
    '-fno-common',
    '-Werror-implicit-function-declaration',
    '-Wno-format-security',
    '-fno-delete-null-pointer-checks',
    '-mlong-calls',
    '-O2',
    '-mno-check-zero-division',
    '-mabi=64',
    '-G',
    '0',
    '-mno-abicalls',
    '-fno-pic',
    '-pipe',
    '-msoft-float',
    '-ffreestanding',
    '-march=octeon',
    '-Wa,--trap',
#    '-Wno-unused-but-set-parameter',
    '-Wno-unused-parameter',
#    '-Wno-unused-but-set-variable',
    '-Wno-unused-variable',
    '-Wa,-mfix-cn63xxp1',
    '-DCVMX_BUILD_FOR_LINUX_KERNEL=1',
    '-DUSE_RUNTIME_MODEL_CHECKS=1',
    '-DCVMX_ENABLE_PARAMETER_CHECKING=0',
    '-DCVMX_ENABLE_CSR_ADDRESS_CHECKING=0',
    '-DCVMX_ENABLE_POW_CHECKS=0',
#    '-msym32',
    '-DKBUILD_64BIT_SYM32',
    '-Wframe-larger-than=2048',
    '-fno-stack-protector',
    '-fomit-frame-pointer',
    '-g',
    '-Wdeclaration-after-statement',
    '-Wno-pointer-sign',
    '-fno-strict-overflow',
    '-fno-dwarf2-cfi-asm',
#    '-fconserve-stack',
    '-D__XXX_PRODUCT__',
    '-DOCTEON_MODEL=OCTEON_CN63XX',
    '-D__SEMP_CUST__',
    '-DKBUILD_STR(s)=#s',
    '-DMODULE',
]

def CFlags(filename):
    c_flags = []

    c_flags.extend(c_extra_flags)

    for c_inc_dir in c_inc_dirs:
        abs_c_inc_dir = p.abspath(DIR_OF_THIS_SCRIPT + '/' + c_inc_dir)
        c_flags.extend(['-I', abs_c_inc_dir])

    # Add kernel include dirs
    for c_inc_dir in c_inc_kdirs:
        abs_c_inc_dir = p.abspath(KERNEL_DIR + '/' + c_inc_dir)
        c_flags.extend(['-I', abs_c_inc_dir])

    if KBUILD_DIR != KERNEL_DIR:
        # Add build_dir include dirs
        for c_inc_dir in c_inc_kdirs:
            abs_c_inc_dir = p.abspath(KBUILD_DIR + '/' + c_inc_dir)
            c_flags.extend(['-I', abs_c_inc_dir])

    name = p.basename(p.splitext(filename)[0])
    dirname = p.abspath(p.dirname(filename))

    #c_flags.append('-Wp,-MD,' + dirname + '/.' + name + '.o.d')
    c_flags.append('-DKBUILD_BASENAME=KBUILD_STR(' + name.replace('-', '_') + ')')
    c_flags.append('-DKBUILD_MODNAME=KBUILD_STR(' + name.replace('-', '_') + ')')
    c_flags.append('-c')
    c_flags.extend(['-o', dirname + '/' + name + '.o'])
    return c_flags
