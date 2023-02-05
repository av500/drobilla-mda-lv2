# Copyright 2020-2022 David Robillard <d@drobilla.net>
# SPDX-License-Identifier: 0BSD OR MIT

# Project-specific warning suppressions.
#
# This should be used in conjunction with the generic "warnings" sibling that
# enables all reasonable warnings for the compiler.  It lives here just to keep
# the top-level meson.build more readable.

#######
# C++ #
#######

if is_variable('cpp')
  cpp_suppressions = []

  if get_option('strict')
    if cpp.get_id() in ['clang', 'emscripten']
      cpp_suppressions = [
        '-Wno-cast-align',
        '-Wno-cast-qual',
        '-Wno-comma',
        '-Wno-deprecated-copy-dtor',
        '-Wno-documentation-unknown-command',
        '-Wno-double-promotion',
        '-Wno-float-equal',
        '-Wno-implicit-float-conversion',
        '-Wno-nullability-extension',
        '-Wno-old-style-cast',
        '-Wno-padded',
        '-Wno-reserved-id-macro',
        '-Wno-shorten-64-to-32',
        '-Wno-sign-conversion',
        '-Wno-suggest-destructor-override',
        '-Wno-suggest-override',
        '-Wno-unused-parameter',
        '-Wno-weak-vtables',
        '-Wno-zero-as-null-pointer-constant',
      ]

      if host_machine.system() == 'windows'
        cpp_suppressions += [
          '-Wno-deprecated-declarations',
        ]
      endif

    elif cpp.get_id() == 'gcc'
      cpp_suppressions = [
        '-Wno-cast-align',
        '-Wno-cast-qual',
        '-Wno-conversion',
        '-Wno-deprecated-copy-dtor',
        '-Wno-double-promotion',
        '-Wno-duplicated-branches',
        '-Wno-effc++',
        '-Wno-float-conversion',
        '-Wno-float-equal',
        '-Wno-format-overflow',
        '-Wno-old-style-cast',
        '-Wno-padded',
        '-Wno-strict-overflow',
        '-Wno-suggest-attribute=const',
        '-Wno-suggest-attribute=pure',
        '-Wno-suggest-final-methods',
        '-Wno-suggest-final-types',
        '-Wno-suggest-override',
        '-Wno-switch-default',
        '-Wno-unused-const-variable',
        '-Wno-unused-parameter',
        '-Wno-useless-cast',
      ]

    elif cpp.get_id() == 'msvc'
      cpp_suppressions = [
        '/wd4100', # unreferenced formal parameter
        '/wd4244', # conversion with possible loss of data
        '/wd4365', # signed/unsigned mismatch
        '/wd4464', # relative include path contains '..'
        '/wd4514', # unreferenced inline function has been removed
        '/wd4706', # assignment within conditional expression
        '/wd4710', # function not inlined
        '/wd4711', # function selected for automatic inline expansion
        '/wd4820', # padding added after construct
        '/wd4996', # POSIX name for this item is deprecated
        '/wd5045', # will insert Spectre mitigation for memory load
        '/wd5219', # implicit conversion to float with possible loss of data
        '/wd5264', # const variable is not used
      ]
    endif
  endif

  cpp_suppressions = cpp.get_supported_arguments(cpp_suppressions)
endif
