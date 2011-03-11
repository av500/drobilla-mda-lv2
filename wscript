#!/usr/bin/env python
import autowaf
import os

# Version of this package (even if built as a child)
MDALA_VERSION = '0.0.0'

# Variables for 'waf dist'
APPNAME = 'mdala.lv2'
VERSION = MDALA_VERSION

# Mandatory variables
top = '.'
out = 'build'

def options(opt):
	autowaf.set_options(opt)
	opt.tool_options('compiler_cxx')

def configure(conf):
	autowaf.configure(conf)
	autowaf.display_header('Mdala Configuration')
	conf.check_tool('compiler_cxx')

	autowaf.check_header(conf, 'lv2/lv2plug.in/ns/lv2core/lv2.h')

	conf.env.append_value('CFLAGS', '-std=c99')

	# Set env['pluginlib_PATTERN']
	pat = conf.env['cshlib_PATTERN']
	if pat[0:3] == 'lib':
		pat = pat[3:]
	conf.env['pluginlib_PATTERN'] = pat

	print('')

def build_plugin(bld, lang, bundle, name, source, cflags=[], libs=[]):
	# Build plugin library
	penv = bld.env.copy()
	penv['cshlib_PATTERN']   = bld.env['pluginlib_PATTERN']
	penv['cxxshlib_PATTERN'] = bld.env['pluginlib_PATTERN']
	obj              = bld(features = '%s %sshlib' % (lang,lang))
	obj.env          = penv
	obj.source       = source + ['lvz/wrapper.cpp']
	obj.includes     = [ '.', './lvz', './src' ]
	obj.name         = name
	obj.target       = os.path.join(bundle, name)
	if cflags != []:
		obj.cxxflags = cflags
	if libs != []:
		autowaf.use_lib(bld, obj, libs)
	obj.install_path = '${LV2DIR}/' + bundle

	# Install data file
	data_file = '%s.ttl' % name
	bld.install_files('${LV2DIR}/' + bundle, os.path.join(bundle, data_file))

def build(bld):
	# Copy data files to build bundle (build/mdala.lv2)
	for i in bld.path.ant_glob('mdala.lv2/*.ttl'):
		bld(rule   = 'cp ${SRC} ${TGT}',
		    source = i,
		    target = bld.path.get_bld().make_node('mdala.lv2/%s' % i),
		    install_path = '${LV2DIR}/mdala.lv2')

	plugins = '''
		Ambience
		Bandisto
		BeatBox
		Combo
		DeEss
		Degrade
		Delay
		Detune
		Dither
		DubDelay
		Dynamics
		Image
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
#		DX10
#		EPiano
#		JX10
#		Looplex

	# Build plugin libraries
	for i in plugins:
		build_plugin(bld, 'cxx', 'mdala.lv2', i, ['src/mda%s.cpp' % i],
					 ['-DPLUGIN_CLASS=mda%s' % i,
					  '-DURI_PREFIX=\"http://drobilla.net/plugins/mdala/\"',
					  '-DPLUGIN_URI_SUFFIX="%s"' % i,
					  '-DPLUGIN_HEADER="src/mda%s.h"' % i])

	bld.install_files('${LV2DIR}/mdala.lv2', 'mdala.lv2/manifest.ttl')

