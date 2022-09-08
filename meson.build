# Copyright 2021-2022 David Robillard <d@drobilla.net>
# SPDX-License-Identifier: 0BSD OR MIT

project('mda-lv2', ['cpp'],
        version: '1.2.10',
        license: 'GPLv2+',
        meson_version: '>= 0.56.0',
        default_options: [
          'b_ndebug=if-release',
          'buildtype=release',
          'cpp_std=c++11',
        ])

#######################
# Compilers and Flags #
#######################

# Load build tools
cpp = meson.get_compiler('cpp')

# Set global warning flags
if get_option('strict') and not meson.is_subproject()
  subdir('meson/warnings')
endif
subdir('meson/suppressions')

################
# Dependencies #
################

m_dep = cpp.find_library('m', required: false)

lv2_dep = dependency('lv2', version: '>= 1.16.0', fallback: ['lv2', 'lv2_dep'])

#########
# Paths #
#########

lv2dir = get_option('lv2dir')
if lv2dir == ''
  prefix = get_option('prefix')
  if target_machine.system() == 'darwin' and prefix == '/'
    lv2dir = '/Library/Audio/Plug-Ins/LV2'
  elif target_machine.system() == 'haiku' and prefix == '/'
    lv2dir = '/boot/common/add-ons/lv2'
  elif target_machine.system() == 'windows' and prefix == 'C:/'
    lv2dir = 'C:/Program Files/Common/LV2'
  else
    lv2dir = prefix / get_option('libdir') / 'lv2'
  endif
endif

#################
# Plugin Bundle #
#################

subdir('mda.lv2')

#########
# Tests #
#########

if not get_option('tests').disabled() and not meson.is_subproject()
  if get_option('strict')
    # Check release metadata
    autoship = find_program('autoship', required: get_option('tests'))
    if autoship.found()
      test(
        'autoship',
        autoship,
        args: ['test', meson.current_source_dir()],
        suite: 'data',
      )
    endif
  endif

  # Check licensing metadata
  reuse = find_program('reuse', required: get_option('tests'))
  if reuse.found()
    test('REUSE', reuse,
         args: ['--root', meson.current_source_dir(), 'lint'],
         suite: 'data')
  endif
endif
