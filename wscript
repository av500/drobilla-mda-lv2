#!/usr/bin/env python

import os
import re
import shutil

from waflib.extras import autowaf

MDA_VERSION = '1.2.4'

# Mandatory waf variables
APPNAME = 'mda-lv2'    # Package name for waf dist
VERSION = MDA_VERSION  # Package version for waf dist
top     = '.'          # Source directory
out     = 'build'      # Build directory

# Release variables
title        = 'MDA.lv2'
uri          = 'http://drobilla.net/sw/mda.lv2'
dist_pattern = 'http://download.drobilla.net/mda-lv2-%d.%d.%d.tar.bz2'
post_tags    = ['LV2', 'MDA.lv2']

def options(opt):
    opt.load('compiler_cxx')
    opt.load('lv2')

def configure(conf):
    conf.load('compiler_cxx', cache=True)
    conf.load('lv2', cache=True)
    conf.load('autowaf', cache=True)
    autowaf.set_c_lang(conf, 'c99')
    conf.check_pkg('lv2 >= 1.16.0', uselib_store='LV2')
    conf.run_env.append_unique('LV2_PATH', [conf.build_path('lv2')])
    autowaf.display_summary(conf, {'LV2 bundle directory': conf.env.LV2DIR})

def build(bld):
    bundle = 'mda.lv2'

    for i in bld.path.ant_glob('mda.lv2/[A-Z]*.ttl'):
        bld(features     = 'subst',
            is_copy      = True,
            source       = i,
            target       = 'lv2/mda.lv2/%s' % i.name,
            install_path = '${LV2DIR}/mda.lv2')

    # Build manifest by substitution
    bld(features     = 'subst',
        source       = 'mda.lv2/manifest.ttl.in',
        target       = 'lv2/mda.lv2/manifest.ttl',
        LIB_EXT      = bld.env.LV2_LIB_EXT,
        install_path = '${LV2DIR}/mda.lv2')

    plugins = '''
            Ambience
            Bandisto
            BeatBox
            Combo
            DX10
            DeEss
            Degrade
            Delay
            Detune
            Dither
            DubDelay
            Dynamics
            EPiano
            Image
            JX10
            Leslie
            Limiter
            Loudness
            MultiBand
            Overdrive
            Piano
            RePsycho
            RezFilter
            RingMod
            RoundPan
            Shepard
            Splitter
            Stereo
            SubSynth
            TalkBox
            TestTone
            ThruZero
            Tracker
            Transient
            VocInput
            Vocoder
    '''.split()

    for p in plugins:
        # Build plugin library
        obj = bld(features     = 'cxx cxxshlib lv2lib',
                  source       = ['src/mda%s.cpp' % p, 'lvz/wrapper.cpp'],
                  includes     = ['.', './lvz', './src'],
                  name         = p,
                  target       = os.path.join('lv2', bundle, p),
                  install_path = '${LV2DIR}/' + bundle,
                  uselib       = ['LV2'],
                  defines      = ['PLUGIN_CLASS=mda%s' % p,
                                  'URI_PREFIX="http://drobilla.net/plugins/mda/"',
                                  'PLUGIN_URI_SUFFIX="%s"' % p,
                                  'PLUGIN_HEADER="src/mda%s.h"' % p])

        # Install data file
        bld.install_files('${LV2DIR}/' + bundle, os.path.join(bundle, p + '.ttl'))
