#!/usr/bin/python
# -*- coding: utf-8
#
# build the list of extraordinary days from -1000 to 2015

#   Copyright © 2016 by John Sauter <John_Sauter@systemeyescomputerstore.com>

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

import sys
import re
import hashlib
import datetime
from jdcal import gcal2jd, jd2gcal, is_leap
import pprint
import argparse

parser = argparse.ArgumentParser (
  formatter_class=argparse.RawDescriptionHelpFormatter,
  description='Build the table of extraordinary days',
  epilog='Copyright © 2016 by John Sauter' + '\n' +
  'License GPL3+: GNU GPL version 3 or later; ' + '\n' +
  'see <http://gnu.org/licenses/gpl.html> for the full text ' +
  'of the license.' + '\n' +
  'This is free software: you are free to change and redistribute it. ' + '\n' +
  'There is NO WARRANTY, to the extent permitted by law. ' + '\n' + '\n'
  'The input file lists the extraordinary days; ' +
  'the output summarizes the information. ' + '\n')
parser.add_argument ('output_file',
                     help='the list of extraordinary days')
parser.add_argument ('--version', action='version', 
                     version='build_extraordinary_days_table 1.0 2016-12-18',
                     help='print the version number and exit')
parser.add_argument ('--trace', metavar='trace_file',
                     help='write trace output to the specified file')
parser.add_argument ('--verbose', type=int, metavar='verbosity level',
                     help='control the amount of output from the program: ' +
                     '1 is normal, 0 suppresses summary messages')

do_trace = 0
tracefile = ""
verbosity_level = 1
error_counter = 0

# Subroutine to convert a Julian Day Number to its equivalent Gregorian date.
month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul",
               "Aug", "Sep", "Oct", "Nov", "Dec"] 
def greg (jdn):
  ymdf = jd2gcal (float(jdn), 0.0)
  year_no = ymdf [0]
  month_no = ymdf [1]
  day_no = ymdf [2]
  month_name = month_names [month_no-1]
  return (str(day_no) + " " + month_name + " " + str(year_no))

edays = set()
last_day = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

# subroutine to accumulate an extraordinary day
def mke (yearno, monthno, dayno, lod):
  if (do_trace == 1):
    tracefile.write ("mke: " + str(yearno) + "," + str(monthno) + "," +
                     str(dayno) + "," + str(lod) + "\n")
  # dayno == -1 means the last day of the month
  if (dayno == -1):
    if (monthno == 2):
      # worry about leap year
      if (is_leap (yearno)):
        dayno = 29          
      else:
        dayno = 28
    else:
      dayno = last_day [monthno-1]
  edays_tuple = (yearno, monthno, dayno, lod)
  edays.add (edays_tuple)
  return

# Parse the command line.
arguments = parser.parse_args ()
arguments = vars(arguments)

if (arguments ['trace'] != None):
  do_trace = 1
  trace_file_name = arguments ['trace']
  tracefile = open (trace_file_name, 'wt')

if (arguments ['verbose'] != None):
  verbosity_level = arguments ['verbose']

# Open the output file.
file_name = arguments ['output_file']
outfile = open (file_name, 'wt')

# create the set of extraordinary days from -1000 to 2015
# using the schedule in table 2.

#
# From L. V. Morrison and F. R. Stephenson
#

# This first extraordinary day gets Delta T right on January 1, -1000.
mke (-1001,12,31,86399)

for yearno in range (-1000, -800):
  for monthno in range (1, 13):
    mke (yearno, monthno, -1, 86399)
  mke (yearno, 3, 15, 86399)
  mke (yearno, 6, 15, 86399)
  mke (yearno, 9, 15, 86399)
  mke (yearno, 11, 15, 86399)
  mke (yearno, 12, 15, 86399)

for yearno in range (-800, -600):
  for monthno in range (1, 13):
    mke (yearno, monthno, -1, 86399)
  mke (yearno, 3, 15, 86399)
  mke (yearno, 6, 15, 86399)
  mke (yearno, 9, 15, 86399)
  mke (yearno, 12, 15, 86399)

for yearno in range (-600, -500):
  for monthno in range (1, 13):
    mke (yearno, monthno, -1, 86399)
  mke (yearno, 3, 15, 86399)
  mke (yearno, 6, 15, 86399)
  mke (yearno, 9, 15, 86399)
  mke (yearno, 12, 15, 86399)
  if (yearno % 10 == 0):
    mke (yearno, 11, 15, 86399)

for yearno in range (-500, -400):
  for monthno in range (1, 13):
    mke (yearno, monthno, -1, 86399)
  mke (yearno, 3, 15, 86399)
  mke (yearno, 6, 15, 86399)
  mke (yearno, 9, 15, 86399)
  mke (yearno, 12, 15, 86399)
  if (yearno % 10 in [0, 1, 3, 5, 6, 8]):
    mke (yearno, 11, 15, 86399)

for yearno in range (-400, -300):
  for monthno in range (1, 13):
    mke (yearno, monthno, -1, 86399)
  mke (yearno, 6, 15, 86399)
  mke (yearno, 12, 15, 86399)
  if (yearno % 2 == 1):
    mke (yearno, 3, 15, 86399)

for yearno in range (-300, -200):
  for monthno in range (1, 13):
    mke (yearno, monthno, -1, 86399)
    if (yearno % 10 != 0):
      mke (yearno, 6, 15, 86399)

for yearno in range (-200, -100):
  for monthno in range (1, 13):
    if (monthno == 2):
      if (yearno % 2 == 1):
        mke (yearno, monthno, -1, 86399)
    else:
      mke (yearno, monthno, -1, 86399)

for yearno in range (-100, 0):
  for monthno in [1, 3, 4, 5, 6, 8, 9, 10, 11, 12]:
    mke (yearno, monthno, -1, 86399)
  if (yearno % 10 in [0, 1, 3, 5, 7, 9]):
    mke (yearno, 7, -1, 86399)

for yearno in range (0, 100):
  for monthno in [1, 3, 4, 6, 8, 9, 10, 11, 12]:
    mke (yearno, monthno, -1, 86399)
  if (yearno % 10 not in [0, 5]):
    mke (yearno, 5, -1, 86399)

for yearno in range (100, 300):
  for monthno in [1, 3, 4, 6, 8, 9, 10, 11, 12]:
    mke (yearno, monthno, -1, 86399)
  if (yearno % 10 in [0, 1, 3, 5, 6, 8]):
    mke (yearno, 5, -1, 86399)

for yearno in range (300, 400):
  for monthno in [1, 3, 4, 6, 8, 9, 10, 11, 12]:
    mke (yearno, monthno, -1, 86399)
  if (yearno % 10 not in [0, 5]):
    mke (yearno, 5, -1, 86399)

for yearno in range (400, 500):
  for monthno in [1, 3, 4, 6, 8, 9, 10, 11, 12]:
    mke (yearno, monthno, -1, 86399)
  if (yearno % 10 != 5):
    mke (yearno, 5, -1, 86399)

for yearno in range (500, 600):
  for monthno in [1, 3, 4, 6, 8, 9, 10, 11, 12]:
    mke (yearno, monthno, -1, 86399)
  if (yearno % 10 not in [2, 5, 8]):
    mke (yearno, 5, -1, 86399)

for yearno in range (600, 700):
  for monthno in [1, 3, 4, 6, 8, 9, 10, 11, 12]:
    mke (yearno, monthno, -1, 86399)
  if (yearno % 10 in [2, 5, 8]):
    mke (yearno, 5, -1, 86399)

for yearno in range (700, 800):
  for monthno in [1, 3, 4, 6, 8, 9, 11, 12]:
    mke (yearno, monthno, -1, 86399)
  if (yearno % 2 == 1):
    mke (yearno, 10, -1, 86399)

for yearno in range (800, 900):
  for monthno in [1, 3, 6, 8, 9, 11, 12]:
    mke (yearno, monthno, -1, 86399)
  if (yearno % 10 in [0, 1, 3, 5, 6, 8]):
    mke (yearno, 4, -1, 86399)

for yearno in range (900, 1000):
  for monthno in [3, 6, 8, 9, 11, 12]:
    mke (yearno, monthno, -1, 86399)
  if (yearno % 10 in [2, 5, 8]):
    mke (yearno, 1, -1, 86399)

for yearno in range (1000, 1100):
  for monthno in [3, 6, 9, 12]:
    mke (yearno, monthno, -1, 86399)
  if (yearno % 10 not in [2, 5]):
    mke (yearno, 11, -1, 86399)

for yearno in range (1100, 1200):
  for monthno in [3, 6, 12]:
    mke (yearno, monthno, -1, 86399)
  if (yearno % 2 == 1):
    mke (yearno, 9, -1, 86399)

for yearno in range (1200, 1300):
  for monthno in [6, 12]:
    mke (yearno, monthno, -1, 86399)
  if (yearno % 2 == 1):
    mke (yearno, 3, -1, 86399)

for yearno in range (1300, 1400):
  mke (yearno, 12, -1, 86399)
  if (yearno % 10 not in [2, 5, 8]):
    mke (yearno, 6, -1, 86399)

for yearno in range (1400, 1500):
  mke (yearno, 12, -1, 86399)
  if (yearno % 10 in [0, 5]):
    mke (yearno, 6, -1, 86399)

mke (1501, 12,31, 86399)
mke (1502, 12,31, 86399)
mke (1504, 12,31, 86399)
mke (1505, 12,31, 86399)
mke (1507, 12,31, 86399)
mke (1508, 12,31, 86399)
mke (1510, 12,31, 86399)
mke (1511, 12,31, 86399)
mke (1513, 12,31, 86399)
mke (1514, 12,31, 86399)
mke (1516, 12,31, 86399)
mke (1517, 12,31, 86399)
mke (1519, 12,31, 86399)
mke (1520, 12,31, 86399)
mke (1522, 12,31, 86399)
mke (1523, 12,31, 86399)
mke (1525, 12,31, 86399)
mke (1526, 12,31, 86399)
mke (1528, 12,31, 86399)
mke (1529, 12,31, 86399)
mke (1531, 12,31, 86399)
mke (1532, 12,31, 86399)
mke (1534, 12,31, 86399)
mke (1535, 12,31, 86399)
mke (1537, 12,31, 86399)
mke (1538, 12,31, 86399)
mke (1540, 12,31, 86399)
mke (1541, 12,31, 86399)
mke (1543, 12,31, 86399)
mke (1544, 12,31, 86399)
mke (1546, 12,31, 86399)
mke (1547, 12,31, 86399)
mke (1549, 12,31, 86399)
mke (1550, 12,31, 86399)
mke (1552, 12,31, 86399)
mke (1553, 12,31, 86399)
mke (1555, 12,31, 86399)
mke (1556, 12,31, 86399)
mke (1558, 12,31, 86399)
mke (1559, 12,31, 86399)
mke (1561, 12,31, 86399)
mke (1562, 12,31, 86399)
mke (1564, 12,31, 86399)
mke (1565, 12,31, 86399)
mke (1566, 12,31, 86399)

for yearno in range (1567, 1600):
  mke (yearno, 12, 31, 86399)
mke (1570, 6, -1, 86399)
mke (1590, 6, -1, 86399)

for yearno in range (1600, 1700):
  mke (yearno, 12, 31, 86399)
  if (yearno in [1600, 1610, 1620, 1630, 1640, 1650, 1659, 1669, 1679,
                 1689, 1699]):
    mke (yearno, 6, -1, 86399)

mke(1705,12,31,86401)
mke(1715,12,31,86401)
mke(1735,12,31,86401)
mke(1745,12,31,86401)
mke(1753,12,31,86401)
mke(1757,12,31,86401)
mke(1765,12,31,86401)
mke(1775,12,31,86401)
mke(1793,12,31,86399)
mke(1795,12,31,86399)
mke(1798,12,31,86399)
mke(1805,12,31,86399)
mke(1815,12,31,86399)
mke(1821,12,31,86399)
mke(1823,12,31,86399)
mke(1825,12,31,86399)
mke(1828,12,31,86399)
mke(1833,12,31,86399)
mke(1837,12,31,86399)
mke(1845,12,31,86401)
mke(1855,12,31,86401)
mke(1860,12,31,86399)
mke(1862,12,31,86399)
mke(1864,12,31,86399)
mke(1865,12,31,86399)
mke(1867,12,31,86399)
mke(1869,12,31,86399)
mke(1870,12,31,86399)
mke(1871,12,31,86399)
mke(1873,12,31,86399)
mke(1874,12,31,86399)
mke(1876,12,31,86399)
mke(1877,12,31,86399)
mke(1878,12,31,86399)
mke(1885,12,31,86399)
mke(1893,12,31,86401)
mke(1896,12,31,86401)
mke(1899,12,31,86401)

for yearno in range (1900,1920):
  mke(yearno,12,31,86401)
mke(1903,6,30,86401)
mke(1906,6,30,86401)
mke(1909,6,30,86401)
mke(1915,6,30,86401)

mke(1923,12,31,86401)
mke(1926,12,31,86401)
mke(1929,12,31,86401)

mke(1941,12,31,86401)
mke(1943,12,31,86401)
mke(1945,12,31,86401)
mke(1947,12,31,86401)
mke(1949,12,31,86401)

mke(1952,12,31,86401)
mke(1955,12,31,86401)

#
# From Tony Finch
#
mke(1957,12,31,86401)
mke(1959,6,30,86401)

mke(1961,6,30,86401)
mke(1963,6,30,86401)
mke(1964,12,31,86401)
mke(1966,6,30,86401)
mke(1967,6,30,86401)
mke(1968,6,30,86401)
mke(1969,6,30,86401)

mke(1970,6,30,86401)
mke(1971,6,30,86401)

#
# from IERS, last updated July 7, 2016, to include December 31, 2016.
#
mke(1972,6,30,86401)
mke(1972,12,31,86401)
mke(1973,12,31,86401)
mke(1974,12,31,86401)
mke(1975,12,31,86401)
mke(1976,12,31,86401)
mke(1977,12,31,86401)
mke(1978,12,31,86401)
mke(1979,12,31,86401)
mke(1981,6,30,86401)
mke(1982,6,30,86401)
mke(1983,6,30,86401)
mke(1985,6,30,86401)
mke(1987,12,31,86401)
mke(1989,12,31,86401)
mke(1990,12,31,86401)
mke(1992,6,30,86401)
mke(1993,6,30,86401)
mke(1994,6,30,86401)
mke(1995,12,31,86401)
mke(1997,6,30,86401)
mke(1998,12,31,86401)
mke(2005,12,31,86401)
mke(2008,12,31,86401)
mke(2012,6,30,86401)
mke(2015,6,30,86401)
mke(2016,12,31,86401)

# determine the Julian Day Number for each extraordinary day
jdn_edays = {}
for yearno, monthno, dayno, lod in edays:
  jdn_tuple = gcal2jd (yearno, monthno, dayno)
  jdn = int(jdn_tuple [0] + jdn_tuple [1] + 0.5)
  jdn_edays [jdn] = lod

# Compute DTAI, based on DTAI = 0 on January 1, 1958, at UTC 00:00.
dtai_dict = {}

dtai0_jdn_tuple = gcal2jd (1957,12,31)
dtai0_jdn = int(dtai0_jdn_tuple [0] + dtai0_jdn_tuple [1] + 0.5)
oldest_jdn = dtai0_jdn
dtai_dict [dtai0_jdn] = 0

# Walk forward from January 1, 1958
current_dtai = 0
jdn_list = sorted(jdn_edays.keys())
for jdn in jdn_list:
  if (jdn < oldest_jdn):
    oldest_jdn = jdn
  if (jdn > dtai0_jdn):
    lod = jdn_edays [jdn]
    current_dtai = current_dtai + lod - 86400
    dtai_dict [jdn] = current_dtai

# Walk backward from January 1, 1958
jdn_list = sorted(jdn_edays.keys(), reverse=1)
prev_jdn = 0
for jdn in jdn_list:
  if (jdn < dtai0_jdn):
    lod = jdn_edays [prev_jdn]
    current_dtai = dtai_dict [prev_jdn] - lod + 86400
    dtai_dict [jdn] = current_dtai
  prev_jdn = jdn

#dtai_dict [oldest_jdn] = current_dtai - 1

# Output the resulting table
for jdn in sorted(jdn_edays.keys()):
  lod = jdn_edays [jdn]
  dtai = dtai_dict [jdn]
  date_tuple = jd2gcal (jdn, 0.0)
  yearno = date_tuple [0]
  monthno = date_tuple [1]
  dayno = date_tuple [2]
  outfile.write (str(jdn) + "\t" + str(lod) + "\t" + str(dtai) + "\t" +
                 "#" + greg (jdn) + "\n")

outfile.close()

if (do_trace == 1):
  tracefile.close()

if (error_counter > 0):
  print "Encountered " + str(error_counter) + " errors."
