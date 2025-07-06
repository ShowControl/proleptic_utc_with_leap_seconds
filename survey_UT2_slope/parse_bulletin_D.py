#!/usr/bin/python3
# -*- coding: utf-8
#
# Parse the text file of IERS Bulletin D.

#   Copyright © 2025 by John Sauter <John_Sauter@systemeyescomputerstore.com>

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
  description='Parse IERS Bulletin D',
  epilog='Copyright © 2025 by John Sauter' + '\n' +
  'License GPL3+: GNU GPL version 3 or later; ' + '\n' +
  'see <http://gnu.org/licenses/gpl.html> for the full text ' +
  'of the license.' + '\n' +
  'This is free software: you are free to change and redistribute it. ' +
  '\n' +
  'There is NO WARRANTY, to the extent permitted by law. ' + '\n' + '\n'
  'The input file is the IERS Bulletin D text file; ' +
  'the output is an extraction of the information. ' + '\n')
parser.add_argument ('input_file',
                     help='IERS Bulletin D as a text file')
parser.add_argument ('--csv-output_file', metavar='csv_output_file',
                     help='write CSV output to the specified file')
parser.add_argument ('--latest-date-output_file',
                     metavar='latest_date_output_file',
                     help='write the latest Bulletin D date ' +
                     'to the specified file')
parser.add_argument ('--version', action='version', 
                     version='parse_bulletin_D 1.3 2025-06-21',
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

# There are several issues of Bulletin D which are missing from
# the IERS web site.  Michael Deckers has reconstructed that information
# from various sources and very kindly provided it to me.
# Fill in the bull_info dictionary with that information.

def missing_date(date_text, DUT1):
  global bull_info
  datetime_object = datetime.datetime.strptime(date_text, '%Y-%m-%d')
  date_object = datetime_object.date()
  bull_info[date_object] = (date_object, DUT1)
  return

missing_date('1991-1-1', 0.6)
missing_date('1991-2-7', 0.5)
missing_date('1991-3-21', 0.4)
missing_date('1991-4-26', 0.3)
missing_date('1992-4-2', 0.4)
missing_date('1992-1-23', -0.2)
missing_date('1992-2-27', -0.3)
missing_date('1992-4-2', -0.4)
missing_date('1992-7-1', 0.4)
missing_date('1993-2-18', -0.1)
missing_date('1993-4-1', -0.2)
missing_date('1993-8-19', 0.5)
missing_date('1994-2-10', 0.1)
missing_date('1994-7-1', 0.8)
missing_date('1994-8-11', 0.7)
missing_date('1994-10-6', 0.6)
missing_date('1994-11-17', 0.5)
missing_date('1994-12-22', 0.4)
missing_date('2009-1-1', 0.4)

# Keep track of the latest date in the file, or today whichever
# is later.
latest_date = datetime.date.today()

def process_file (file_name):
  global bull_info
  global latest_date
  line_number = 0
  date_found = 0
  DUT1 = 0.0
  effective_date_line = 0
  with open (file_name, 'rt') as infile:
    text_line = infile.readline()
    while (text_line != ''):
      line_number = line_number + 1
      stripped_text_line = text_line.strip()
      if ((date_found == 0) and (verbosity_level > 0)):
        print ("'" + stripped_text_line + "'")
        
      stripped_text_line = stripped_text_line.replace('Paris,', 'Paris, ')
      stripped_text_line = stripped_text_line.replace('  ', ' ')
      # Sometimes the month name is written in French.
      stripped_text_line = stripped_text_line.replace ('Mai', 'May')
      stripped_text_line = stripped_text_line.replace ('Juin', 'June')
      stripped_text_line = stripped_text_line.replace ('juin', 'June')
      stripped_text_line = stripped_text_line.replace ('Octobre', 'October')
      stripped_text_line = stripped_text_line.replace ('Decembre', 'December')
      
      if (do_trace == 1):
        if (date_found == 0):
          tracefile.write ('Looking for date: ' + stripped_text_line + '\n')
      right_side = stripped_text_line.rsplit(" ", 5)
      if (verbosity_level > 0):
        print (str(len(right_side)))
        pprint.pprint (right_side)
      if ((date_found == 0) and
          (len(right_side) >= 4) and
          ((right_side[1][0:5] == 'Paris') or
           (right_side[-4] == 'Paris,') or
           (right_side[-4] == '\tParis,') or
           (right_side[-4] == '\t\t\t\tParis,'))):
        date_found = 1
        date_text = (right_side[-3] + " " + right_side[-2] + " " +
           right_side[-1])
        datetime_object = datetime.datetime.strptime (date_text, '%d %B %Y')
        date_object = datetime_object.date()
        if (date_object > latest_date):
          latest_date = date_object
        date_string = date_object.strftime ('%B %d, %Y')
        if (verbosity_level > 0):
          print ('Date of IERS Bulletin D is ' + date_string)
        if (do_trace == 1):
          tracefile.write ('date = ' + date_string + '.\n')
      if ((len(right_side) == 6) and (right_side[1] == '0h')):
        right_side = right_side[0].rsplit(" ", 3)
        datetime_text = (right_side[1] + ' ' + right_side[2] + ' ' +
                         right_side[3][0:4])
        datetime_object = datetime.datetime.strptime (datetime_text,
                                                      '%d %B %Y')
        effective_date_object = datetime_object.date()
        effective_date_string = effective_date_object.strftime ('%B %d, %Y')
        if (effective_date_object > latest_date):
          latest_date = effective_date_object
        if (verbosity_level > 0):
          print ('Effective date is ' + effective_date_string)        
      if ((len(right_side) == 6) and ((right_side[0] == "From the"))):
        datetime_text = (right_side[1] + ' ' + right_side[2] + ' ' +
                         right_side[3][0:4])
        datetime_object = datetime.datetime.strptime (datetime_text,
                                                      '%d %B %Y')
        effective_date_object = datetime_object.date()
        effective_date_string = effective_date_object.strftime ('%B %d, %Y')
        if (effective_date_object > latest_date):
          latest_date = effective_date_object
        if (verbosity_level > 0):
          print ('Effective date is ' + effective_date_string)
      if ((stripped_text_line == 'From the') or
          (stripped_text_line == "From")):      
        effective_date_line = line_number + 1
      if ((verbosity_level > 0) and (effective_date_line > 0)):
          print ("'" + stripped_text_line + "'")
      if (line_number == effective_date_line):
        if (stripped_text_line == ""):
          effective_date_line = effective_date_line + 1
        else:
          effective_date_line = 0
          datetime_text = stripped_text_line.split(",")[0]
          datetime_object = datetime.datetime.strptime (datetime_text,
                                                        '%d %B %Y')
          effective_date_object = datetime_object.date()
          effective_date_string = effective_date_object.strftime ('%B %d, %Y')
          if (effective_date_object > latest_date):
            latest_date = effective_date_object
          if (verbosity_level > 0):
            print ('Effective date is ' + effective_date_string)
      if ((stripped_text_line[0:6] == 'DUT1 =') or
          (stripped_text_line[0:5] == 'DUT1=')):
        right_side = stripped_text_line.split("=")[1].lstrip()
        DUT1_text = right_side[1:].lstrip()
        DUT1_text = DUT1_text.replace("s.", " ")
        DUT1_text = DUT1_text.replace("s", " ")
        DUT1_text = DUT1_text.rstrip()
        DUT1_text = right_side[0] + DUT1_text
        DUT1 = float(DUT1_text)
        if (verbosity_level > 0):
          print ('DUT1 = ' + format(DUT1, ".1f") + '\n')
        # Correct a typo.
        if ((effective_date_object.year == 1995) and
            (effective_date_object.month == 2) and
            (effective_date_object.day == 23)):
          effective_date_object.replace(year=1993)
        if (date_found == 1):
          bull_info [effective_date_object] = (date_object, DUT1)
        else:
          bull_info [effective_date_object] = (effective_date_object, DUT1)
        return
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

# The value of DUT1 extends from the effective date to the next
# effective date
prev_date = None
DUT1_values = dict()
for the_date in sorted(bull_info):
  if (prev_date != None):
    for target_date in range (prev_date.toordinal(), the_date.toordinal()):
      DUT1_values[datetime.date.fromordinal(target_date)] = (
                                                          bull_info[prev_date])
  prev_date = the_date
# And then to the latest date seen
for target_date in range (prev_date.toordinal(), latest_date.toordinal()+1):
  DUT1_values[datetime.date.fromordinal(target_date)] = bull_info[prev_date]
  
if (arguments ['csv_output_file'] != None):
  do_csv_output = 1
  csv_output_file_name = arguments ['csv_output_file']
  csvoutputfile = open (csv_output_file_name, 'wt')

if (do_csv_output == 1):
  csvoutputfile.write ('edate1,edate2,adate1,adate2,DUT1\n')
  for effective_date in sorted(DUT1_values):
    announcement_date = DUT1_values[effective_date][0]
    DUT1 = DUT1_values[effective_date][1]
    csvoutputfile.write ('"=date(' + str(announcement_date.year) + ',' +
                         str(announcement_date.month) + ',' +
                         str(announcement_date.day) + ')",' +
                         str(announcement_date.year) + '-' +
                         str(announcement_date.month) + '-' +
                         str(announcement_date.day) + ',' +
                         '"=date(' + str(effective_date.year) + ',' +
                         str(effective_date.month) + ',' +
                         str(effective_date.day) + ')",' +
                         str(effective_date.year) + '-' +
                         str(effective_date.month) + '-' +
                         str(effective_date.day) + ',' +
                         format(DUT1, ".1f") + '\n')
    
if (arguments ['latest_date_output_file'] != None):
  do_latest_date_output = 1
  latest_date_output_file_name = arguments ['latest_date_output_file']
  latest_dateoutputfile = open (latest_date_output_file_name, 'wt')

if (do_latest_date_output == 1):
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

# End of file parse_bulletin_D.py
