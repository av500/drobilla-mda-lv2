/*
  Copyright 2008-2011 David Robillard <http://drobilla.net>
  Copyright 1999-2000 Paul Kellett (Maxim Digital Audio)

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

#ifndef _mdaSpecMeterGUI_h_
#define _mdaSpecMeterGUI_h_

#include "vstgui.h"


class CDraw : public CControl
{
public:
	CDraw(CRect& size, float x, CBitmap* background);
	~CDraw();

	void draw(CDrawContext *pContext);
	LvzInt32 x2pix(float x);
	LvzInt32 x22pix(float x);

	float Lpeak, Lrms, Lmin, Rpeak, Rrms, Rmin, Corr;
	float band[2][16];
	LvzInt32 temp;

protected:
	CBitmap* bitmap;
};


class mdaSpecMeterGUI : public AEffGUIEditor
{
public:
	mdaSpecMeterGUI(AudioEffect* effect);
	~mdaSpecMeterGUI();

	long open(void* ptr);
	void idle();
	void close();

private:
	CDraw*   draw;
	CBitmap* background;
	LvzInt32 xtimer;
};


#endif // _mdaSpecMeterGUI_h_

