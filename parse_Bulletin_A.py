#!/usr/bin/python3
# -*- coding: utf-8
#
# Parse the text file of IERS Bulletin A.

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

import sys
import re
import hashlib
import datetime
from jdcal import gcal2jd, jd2gcal, is_leap
import pprint
import argparse

parser = argparse.ArgumentParser (
  formatter_class=argparse.RawDescriptionHelpFormatter,
  description='Parse IERS Bulletin A',
  epilog='Copyright © 2019 by John Sauter' + '\n' +
  'License GPL3+: GNU GPL version 3 or later; ' + '\n' +
  'see <http://gnu.org/licenses/gpl.html> for the full text ' +
  'of the license.' + '\n' +
  'This is free software: you are free to change and redistribute it. ' + '\n' +
  'There is NO WARRANTY, to the extent permitted by law. ' + '\n' + '\n'
  'The input file is the IERS Bulletin A text file; ' +
  'the output is an extraction of the information. ' + '\n')
parser.add_argument ('input_file',
                     help='IERS Bulletin A as a text file')
parser.add_argument ('--version', action='version', 
                     version='parse_bulletin_A 2.0 2019-12-12',
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

# Parse the command line.
arguments = parser.parse_args ()
arguments = vars(arguments)

if (arguments ['trace'] != None):
  do_trace = 1
  trace_file_name = arguments ['trace']
  tracefile = open (trace_file_name, 'wt')

if (arguments ['verbose'] != None):
  verbosity_level = arguments ['verbose']

# Process the input file.
input_file_name = arguments ['input_file']
line_number = 0
with open (input_file_name, 'rt') as infile:
  text_line = infile.readline()
  while (text_line != ''):
    line_number = line_number + 1
    if (line_number == 8):
      left_side = text_line[0:40]
      left_side = left_side.rstrip()
      left_side = left_side.lstrip()
      datetime_object = datetime.datetime.strptime (left_side, '%d %B %Y')
      date_object = datetime_object.date()
      date_string = date_object.strftime ('%B %d, %Y')
      print ('Date of IERS Bulletin A is ' + date_string)
    if (text_line[0:19] == '         UT1-UTC = '):
      print (text_line, end='')
      param_1 = text_line[19:26]
      param_1 = float(param_1)
      param_2 = text_line[27] + text_line[29:36]
      param_2 = float(param_2)
      param_3 = text_line[44:49]
      param_3 = int(param_3)
      print ('         UT1-UTC = ' + str(param_1) + ' + (' + str(param_2) +
             ' ⨯ (MJD - ' + str(param_3) + ')) - (UT2-UT1)')
      print ('MJD ' + str(param_3) + ' is ' + greg(param_3 + 2400000.5))
    text_line = infile.readline()

if (do_trace == 1):
  tracefile.close()

if (error_counter > 0):
  print ("Encountered " + str(error_counter) + " errors.")
