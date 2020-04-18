#!/usr/bin/python3
# -*- coding: utf-8
#
# delta_T_projection_parameters.py is a convenient place to update
# the delta T projection paramaters when the IERS updates them.
#
#   Copyright © 2019 by John Sauter <John_Sauter@systemeyescomputerstore.com>

#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.

#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.

#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

#   The author's contact information is as follows:
#     John Sauter
#     System Eyes Computer Store
#     20A Northwest Blvd.  Ste 345
#     Nashua, NH  03063-4066
#     telephone: (603) 424-1188
#     e-mail: John_Sauter@systemeyescomputerstore.com

# According to the USNO (http://maia.usno.navy.mil/ser7/predcoef.out)
# and the text version of IERS Bulletin A
# (https://www.iers.org/IERS/EN/Publications/Bulletins/bulletins.html)
# you can predict UT1-UTC with a formula.  The formula changes each week.
# In IERS Bulletin A volume XVIII Number 001, dated January 6, 2005,
# the formula was:
#
#   UT1-UTC = -.5206 - (0.00030 * (MJD - 53381)) - (UT2 - UT1)
#
# UT2-UT1 is computed as: (http://maia.usno.navy.mil and IERS Bulletin A)
#
#   UT2-UT1 = 0.022 * sin(2*pi*T) - 0.012 * cos(2*pi*T)
#                                 - 0.006 * sin(4*pi*T) + 0.007 * cos(4*pi*T)
#
# Where T is the date in Besselian years:
#  2000.000 + ((MDJ - 51544.03) / 365.2422),
# and MJD is the Modified Julian Date,
#  which is the Julian Day Number - 2400000.5.
#
# The parts of this formula that vary from week to week are the three
# numbers in the first formula, which I will call the UT1_offset,
# the UT1_slope and the UT1_base_MJD.  We can then write the first formula
# in terms of these variables as follows:
#
#   UT1-UTC = UT1_offset + (UT1_slope * (MJD - UT1_base_MJD)) - (UT2-UT1)
#
# Each week the IERS publishes new values for the variables.
# Here are some values of the variables from IERS Bulletin A:
#
# date              UT1_offset UT1_slope UT1_base_MJD
# January 6, 2005    -0.5206   -0.00030  53376
# January 13, 2005   -0.5253   -0.00031  53388
# January 20, 2005   -0.5299   -0.00031  53395
# January 27, 2005   -0.5323   -0.00031  53402
# February 10, 2005  -0.5411   -0.00032  53416
# June 30, 2005      -0.6004   -0.00040  53556
# September 1, 2005  -0.6330   -0.00041  53619
# November 3, 2005   -0.6443   -0.00043  53682
# December 22, 2005  -0.6636   -0.00043  53731
# December 29, 2005   0.3343   -0.00042  53737
# January 5, 2006     0.3324   -0.00042  53745
# January 12, 2006    0.3329   -0.00041  53752
# January 19, 2006    0.3278   -0.00041  53759
# January 26, 2006    0.3204   -0.00040  53766
# February 2, 2006    0.3138   -0.00040  53773
# January 3, 2008    -0.2788   -0.00087  54476
# January 7, 2010     0.1075   -0.00089  55211
# December 28, 2011  -0.4316   -0.00085  55932
# January 14, 2016    0.0162   -0.00131  57409
# June 30, 2016      -0.2007   -0.00146  57577
# July 7, 2016       -0.2104   -0.00146  57584
# December 29, 2016   0.5882   -0.00130  57759
# January 4, 2018     0.2191   -0.00100  58130
# June 28, 2018       0.0929   -0.00073  58305
# January 3, 2019    -0.0515   -0.00066  58494
# May 16, 2019       -0.1248   -0.00064  58627
# May 23, 2019       -0.1295   -0.00064  58634
# May 30, 2019       -0.1353   -0.00064  58641
# June 6, 2019       -0.1388   -0.00064  58648
# June 13, 2019      -0.1447   -0.00063  58655
# June 20, 2019      -0.1507   -0.00063  58662
# June 27, 2019      -0.1542   -0.00063  58669
# July 4, 2019       -0.1558   -0.00062  58676
# July 11, 2019      -0.1570   -0.00061  58683
# July 18, 2019      -0.1598   -0.00060  58690
# July 25, 2019      -0.1628   -0.00060  58697
# August 1, 2019     -0.1677   -0.00059  58704
# August 8, 2019     -0.1703   -0.00058  58711
# August 15, 2019    -0.1707   -0.00057  58718
# August 22, 2019    -0.1733   -0.00056  58725
# August 29, 2019    -0.1748   -0.00056  58732
# September 5, 2019  -0.1747   -0.00055  58739
# September 12, 2019 -0.1720   -0.00054  58746
# September 19, 2019 -0.1688   -0.00053  58753
# September 26, 2019 -0.1645   -0.00052  58760
# October 3, 2019    -0.1592   -0.00051  58767
# October 10, 2019   -0.1564   -0.00049  58774
# October 17, 2019   -0.1555   -0.00048  58781
# October 24, 2019   -0.1547   -0.00047  58788
# October 31, 2019   -0.1521   -0.00045  58795
# November 7, 2019   -0.1548   -0.00044  58802
# November 14, 2019  -0.1551   -0.00043  58809
# November 21, 2019  -0.1551   -0.00041  58816
# November 28, 2019  -0.1565   -0.00040  58823
# December 5, 2019   -0.1561   -0.00039  58830
#
# The current values of the variables are therefore:
UT1_offset =      -0.1561
UT1_slope =       -0.00039
UT1_base_MJD = 58830

# End of file set_delta_T_projection_parameters.py

