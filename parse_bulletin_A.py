#!/usr/bin/python3
# -*- coding: utf-8
#
# Parse the text file of IERS Bulletin A.

#   Copyright © 2024 by John Sauter <John_Sauter@systemeyescomputerstore.com>

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
from pathlib import Path
import argparse

parser = argparse.ArgumentParser (
  formatter_class=argparse.RawDescriptionHelpFormatter,
  description='Parse IERS Bulletin A',
  epilog='Copyright © 2024 by John Sauter' + '\n' +
  'License GPL3+: GNU GPL version 3 or later; ' + '\n' +
  'see <http://gnu.org/licenses/gpl.html> for the full text ' +
  'of the license.' + '\n' +
  'This is free software: you are free to change and redistribute it. '
  + '\n' +
  'There is NO WARRANTY, to the extent permitted by law. ' + '\n' + '\n'
  'The input file is the IERS Bulletin A text file; ' +
  'the output is an extraction of the information. ' + '\n')
parser.add_argument ('input_file',
                     help='IERS Bulletin A as a text file')
parser.add_argument ('--csv-output_file', metavar='csv_output_file',
                     help='write CSV output to the specified file')
parser.add_argument ('--latest-date-output_file',
                     metavar='latest_date_output_file',
                     help='write the latest Bulletin A date to the specified file')
parser.add_argument ('--version', action='version', 
                     version='parse_bulletin_A 3.7 2024-12-26',
                     help='print the version number and exit')
parser.add_argument ('--trace', metavar='trace_file',
                     help='write trace output to the specified file')
parser.add_argument ('--verbose', type=int, metavar='verbosity level',
                     help='control the amount of output from the program: ' +
                     '1 is normal, 0 suppresses summary messages')

do_trace = 0
tracefile = ""
do_csv_output = 0
do_latest_date_output = 0
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
  tracefile = open (trace_file_name, 'at')

if (arguments ['verbose'] != None):
  verbosity_level = arguments ['verbose']

bull_info = dict()

def process_file (file_name):
  global bull_info
  line_number = 0
  date_found = 0
  next_line_is_DUT1 = 0
  DUT1 = 0.0
  with open (file_name, 'rt') as infile:
    text_line = infile.readline()
    while (text_line != ''):
      line_number = line_number + 1
      left_side = text_line[0:40]
      left_side = left_side.rstrip()
      left_side = left_side.lstrip()
      right_side = text_line[41:]
      right_side = right_side.lstrip()
      right_side = right_side[0:5]
      stripped_text_line = text_line.lstrip()
      stripped_text_line = stripped_text_line.rstrip()
      if (do_trace == 1):
        if (date_found == 0):
          tracefile.write ('Looking for date: ' + right_side + '\n')
      if ((date_found == 0) and (right_side == 'Vol. ')):
        date_found = 1
        datetime_object = datetime.datetime.strptime (left_side, '%d %B %Y')
        date_object = datetime_object.date()
        date_string = date_object.strftime ('%B %d, %Y')
        if (verbosity_level > 0):
          print ('Date of IERS Bulletin A is ' + date_string)
        if (do_trace == 1):
          tracefile.write ('date = ' + date_string + '.\n')
      if (next_line_is_DUT1 == 1):
        find_DUT1 = stripped_text_line[1:8];
        if (do_trace == 1):
          tracefile.write ("finding DUT1 in " + find_DUT1 + ".\n");
        if (find_DUT1[-1] != " "):
          find_DUT1 = stripped_text_line[1:7]
          if (do_trace == 1):
            tracefile.write ("finding DUT1 in " + find_DUT1 + ".\n");
        if (find_DUT1[-1] != " "):
          find_DUT1 = stripped_text_line[1:6]
          if (do_trace == 1):
            tracefile.write ("finding DUT1 in " + find_DUT1 + ".\n");
        DUT1 = float(find_DUT1)
        next_line_is_DUT1 = 0
      if (stripped_text_line=='DUT1= (UT1-UTC) transmitted with time signals'):
        next_line_is_DUT1 = 1
      if (text_line[0:19] == '         UT1-UTC = '):
        if (verbosity_level > 0):
          print (text_line, end='')
        param_1 = text_line[19:26]
        if (do_trace == 1):
          tracefile.write ('param_1 = "' + param_1 + '".\n')
        param_1 = float(param_1)
        param_2 = text_line[27] + text_line[29:36].lstrip()
        if (do_trace == 1):
          tracefile.write ('param_2 = "' + param_2 + '".\n')
        param_2 = float(param_2)
        param_3 = text_line[44:49]
        param_3 = int(param_3)
        if (verbosity_level > 0):
          print ('         UT1-UTC = ' + str(param_1) + ' + (' +
                 format(param_2, ".5f") +
                 ' ⨯ (MJD - ' + str(param_3) + ')) - (UT2-UT1)')
          print ('MJD ' + str(param_3) + ' is ' + greg(param_3 + 2400000.5))
        bull_info [date_object] = (param_1, param_2, param_3, DUT1)
      text_line = infile.readline()

# Process the input file.  If it is a directory, process all .txt files
# within it.
input_file_name = arguments ['input_file']
if (do_trace == 1):
  tracefile.write ('input file name = ' + input_file_name + '.\n')
input_file_path = Path(input_file_name)
if (input_file_path.is_dir()):
  for file_name in list(input_file_path.glob('*.txt')):
    process_file (file_name)
else:
  process_file (input_file_name)
  
if (arguments ['csv_output_file'] != None):
  do_csv_output = 1
  csv_output_file_name = arguments ['csv_output_file']
  csvoutputfile = open (csv_output_file_name, 'wt')

if (do_csv_output == 1):
  csvoutputfile.write ('date1,date2,UT2_slope,DUT1\n')
  for the_date in sorted(bull_info):
    csvoutputfile.write ('"=date(' + str(the_date.year) + ',' +
                         str(the_date.month) + ',' +
                         str(the_date.day) + ')",' +
                         str(the_date.year) + '-' +
                         str(the_date.month) + '-' +
                         str(the_date.day) + ',' +
                         format(bull_info[the_date][1], ".5f") + "," +
                         format(bull_info[the_date][3], ".5f") + '\n')

if (arguments ['latest_date_output_file'] != None):
  do_latest_date_output = 1
  latest_date_output_file_name = arguments ['latest_date_output_file']
  latest_dateoutputfile = open (latest_date_output_file_name, 'wt')

if (do_latest_date_output == 1):
  latest_date = sorted(bull_info)[-1]
  date_string = latest_date.strftime ('%B %d, %Y')
  latest_dateoutputfile.write (date_string)
  
if (do_csv_output == 1):
  csvoutputfile.close()

if (do_latest_date_output == 1):
  latest_dateoutputfile.close()
  
if (do_trace == 1):
  tracefile.close()

if (error_counter > 0):
  print ("Encountered " + str(error_counter) + " errors.")

# End of file parse_bulletin_A.py
  
