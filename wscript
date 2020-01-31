#! /usr/bin/env python

def configure(ctx):
    pass

def build(ctx):
    DEPS = ['default']
    THIS_LIB = 'apriltag3'

    # NOTE: Asan build has a known bug that sometimes causes it to take a VERY long
    #       time to compile when optimizations are turned on. AprilTag seems to trigger
    #       this, so these flags limit the amount of work asan will do on these files.
    #       This probably means asan's analysis of AprilTag won't be perfect.
    #       See https://llvm.org/bugs/show_bug.cgi?id=17409#c11 for more information.
    FLAGS = []
    if ctx.env.usingSanitizers and ctx.env.CLANG_VERSION > (3, 4):
        FLAGS = '-mllvm -asan-instrumentation-with-call-threshold=1000'

    ctx.stlib(target = THIS_LIB,
              use    = DEPS,
              cflags = FLAGS,
              includes = '.',
              export_includes = '..',
              source = ctx.path.ant_glob('*.c common/*.c', excl = 'apriltag_pywrap.c'))
