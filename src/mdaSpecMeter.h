/*
  Copyright 2008-2011 David Robillard <http://drobilla.net>
  Copyright 2002 Paul Kellett (Maxim Digital Audio)

  This is free software: you can redistribute it and/or modify it
  under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License,
  or (at your option) any later version.

  This software is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
  See the GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this software. If not, see <http://www.gnu.org/licenses/>.
*/

#include "audioeffectx.h"

#include <string.h>

#define NPROGS 4 //can hide decay settings in programs!  fast...slow...peak hold
#define SILENCE 0.00000001f

enum {
	_PARAM0, //gain
//	_PARAM0, //peak decay
//	_PARAM1, //RMS speed
//	_PARAM2, //spectrum speed
//	_PARAM3, //peak reset?

	NPARAMS
};

class mdaSpecMeter;

class mdaSpecMeterProgram
{
friend class mdaSpecMeter;
public:
	mdaSpecMeterProgram();
private:	
	float param[NPARAMS];
	char  name[24];
};


class mdaSpecMeter : public AudioEffectX
{
public:
	mdaSpecMeter(audioMasterCallback audioMaster);
	~mdaSpecMeter();

	virtual void  process(float **inputs, float **outputs, LvzInt32 sampleFrames);
	virtual void  processReplacing(float **inputs, float **outputs, LvzInt32 sampleFrames);
	virtual void  setProgram(LvzInt32 program);
	virtual void  setProgramName(char *name);
	virtual void  getProgramName(char *name);
	virtual bool  getProgramNameIndexed (LvzInt32 category, LvzInt32 index, char* name);
	virtual void  setParameter(LvzInt32 index, float value);
	virtual float getParameter(LvzInt32 index);
	virtual void  getParameterLabel(LvzInt32 index, char *label);
	virtual void  getParameterDisplay(LvzInt32 index, char *text);
	virtual void  getParameterName(LvzInt32 index, char *text);
	virtual void  setSampleRate(float sampleRate);
	virtual void  suspend();

	virtual bool getEffectName(char *name);
	virtual bool getVendorString(char *text);
	virtual bool getProductString(char *text);
	virtual LvzInt32 getVendorVersion() { return 1000; }

  //accessible from editor
  LvzInt32  counter;
  float Lpeak, Lhold, Lmin, Lrms, Rpeak, Rhold, Rmin, Rrms, Corr; // #11  #12
  float band[2][16]; //8  16  31  64  125  250  500  1k  2k  4k  8k  16k  32k

private:
	mdaSpecMeterProgram *programs;

  float iK, lpeak, lmin, lrms, rpeak, rmin, rrms, corr, den;
  float lpp[6][16], rpp[6][16];
  LvzInt32  topband, K, kmax;

  float gain;
};
