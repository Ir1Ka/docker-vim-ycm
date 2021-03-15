import os.path as p

DIR_OF_THIS_SCRIPT = p.abspath( p.dirname( __file__ ) )

inc_dirs = [
    'system/core/include',
    'hardware/libhardware/include',
    'hardware/libhardware_legacy/include',
    'hardware/ril/include',
    'libnativehelper/include',
    'bionic/libc/arch-arm/include',
    'bionic/libc/include',
    'bionic/libc/kernel/common',
    'bionic/libc/kernel/arch-arm',
    'bionic/libstdc++/include',
    'bionic/libstdc++/include',
    'bionic/libm/include',
    'bionic/libm/include/arm',
    'bionic/libthread_db/include',
    'frameworks/native/include',
    'frameworks/native/opengl/include',
    'frameworks/av/include',
    'frameworks/base/include',
]

def CFlags(filename):
    c_flags = []
    for inc_dir in inc_dirs:
        abs_inc_dir = p.abspath( DIR_OF_THIS_SCRIPT + '/' + inc_dir )
        c_flags.append('-I' + abs_inc_dir)
    return c_flags

def CppFlags(filename):
    cpp_flags = []
    for inc_dir in inc_dirs:
        abs_inc_dir = p.abspath( DIR_OF_THIS_SCRIPT + '/' + inc_dir )
        cpp_flags.append('-I' + abs_inc_dir)
    return cpp_flags
