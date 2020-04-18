#!/usr/bin/python3
# -*- coding: utf-8
#
# write a file to be loaded by gnuplot which defines x-axis labels
# for Julian Day Numbers.

#   Copyright © 2020 by John Sauter <John_Sauter@systemeyescomputerstore.com>

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
from jdcal import gcal2jd, jd2gcal
import pprint
import argparse

parser = argparse.ArgumentParser (
  formatter_class=argparse.RawDescriptionHelpFormatter,
  description='Build an xtic labels file.',
  epilog='Copyright © 2020 by John Sauter' + '\n' +
  'License GPL3+: GNU GPL version 3 or later; ' + '\n' +
  'see <http://gnu.org/licenses/gpl.html> for the full text ' +
  'of the license.' + '\n' +
  'This is free software: you are free to change and redistribute it. ' + '\n' +
  'There is NO WARRANTY, to the extent permitted by law. ' + '\n' + '\n'
  'The output file defines xtic labels for GNUplot; ' + '\n')
parser.add_argument ('output-file', metavar='output_file',
                     help='output file')
parser.add_argument ('--version', action='version', 
                     version='build_xtic_monthly_labels 1.0 2020-04-17',
                     help='print the version number and exit')
parser.add_argument ('--trace', metavar='trace_file',
                     help='write trace output to the specified file')
parser.add_argument ('--interval',type=int,metavar='interval',
                     help='years between ticks, default is 1')
parser.add_argument ('--start-year',type=int,metavar='start_year',
                     help='earliest year, default is -2000')
parser.add_argument ('--end-year',type=int,metavar='end_year',
                     help='last year, default is 2500')
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
def greg (jdn, separator):
  ymdf = jd2gcal (float(jdn), 0.5)
  year_no = ymdf [0]
  month_no = ymdf [1]
  day_no = ymdf [2]
  month_name = month_names [month_no-1]
  return (str(day_no) + separator + month_name + separator + str(year_no))

# Subroutine to convert a Gregorian year, month and day to its
# Julian Day Number.

def jdn (year_no, month_no, day_no):
  seq = gcal2jd (year_no, month_no, day_no)
  val = seq[0] + seq[1] - 0.5
  return (int(val))

# Subroutine to determine the year (in the Gregorian calendar) of a
# Julian Day Number
def yearno (jdn):
  ymdf = jd2gcal (float(jdn), 0.5)
  return (ymdf [0])

# Subroutine to determine the month (in the Gregorian calendar) of a
# Julian Day Number.
def monthno (jdn):
  ymdf = jd2gcal (float(jdn), 0.5)
  return (ymdf [1])

#
# Parse the command line.
#

arguments = parser.parse_args ()
arguments = vars(arguments)

if (arguments ['output-file'] != None):
  output_file_name = arguments ['output-file']
  
if (arguments ['trace'] != None):
  do_trace = 1
  trace_file_name = arguments ['trace']
  tracefile = open (trace_file_name, 'wt')

if (arguments ['verbose'] != None):
  verbosity_level = int(arguments ['verbose'])

if (arguments ['interval'] != None):
  interval = int (arguments['interval'])
else:
  interval = 1

if (arguments ['start_year'] != None):
  start_year = int (arguments['start_year'])
else:
  start_year = -2000

if (arguments ['end_year'] != None):
  end_year = int (arguments['end_year'])
else:
  end_year = 2500
  
#
# Write a file which can be loaded by GNUplot which labels the
# x-axis, assumed to be Julian Day Numbers.
#
output_file = open (output_file_name, 'wt')
output_file.write ("set xtics (\\\n")
first_line = 1
last_yearmonth = 0
start_JDN = jdn(start_year, 1, 1)
end_JDN = jdn(end_year,12,31)

for the_JDN in range (start_JDN, end_JDN + 1):
  yearmonth = (yearno(the_JDN) * 12) + (monthno(the_JDN) -1)
  if ((yearmonth - last_yearmonth) >= interval):
    output_file.write ("  ")
    if (first_line == 0):
      output_file.write (",")
    first_line = 0
    output_file.write ("\"" + greg(the_JDN, "-") +
                               "\" " + str(the_JDN) + "\\\n")
    last_yearmonth = yearmonth
  
output_file.write (")\n")
output_file.close()

if (do_trace == 1):
  tracefile.close()

if (error_counter > 0):
  print ("Encountered " + str(error_counter) + " errors.")
