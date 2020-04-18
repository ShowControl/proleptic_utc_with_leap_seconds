#!/usr/bin/python
# -*- coding: utf-8
#
# Parse the text file of IERS Bulletin C.

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
from jdcal import gcal2jd, jd2gcal, is_leap
import pprint
import argparse

parser = argparse.ArgumentParser (
  formatter_class=argparse.RawDescriptionHelpFormatter,
  description='Parse IERS Bulletin C',
  epilog='Copyright © 2020 by John Sauter' + '\n' +
  'License GPL3+: GNU GPL version 3 or later; ' + '\n' +
  'see <http://gnu.org/licenses/gpl.html> for the full text ' +
  'of the license.' + '\n' +
  'This is free software: you are free to change and redistribute it. ' + '\n' +
  'There is NO WARRANTY, to the extent permitted by law. ' + '\n' + '\n'
  'The input file is the IERS Bulletin C text file; ' +
  'the output is an extraction of the information. ' + '\n')
parser.add_argument ('input_file',
                     help='IERS Bulletin C as a text file')
parser.add_argument ('--version', action='version', 
                     version='parse_bulletin_C 2.0 2020-01-11',
                     help='print the version number and exit')
parser.add_argument ('--trace', metavar='trace_file',
                     help='write trace output to the specified file')
parser.add_argument ('--expiration-date-file', metavar='expiraton_date_file',
                     help='write the IERS Bulletin C expiraton date here')
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
def Gregorian (jdn):
  ymdf = jd2gcal (float(jdn), 0.5)
  year_no = ymdf [0]
  month_no = ymdf [1]
  day_no = ymdf [2]
  month_name = month_names [month_no-1]
  return (str(day_no) + " " + month_name + " " + str(year_no))

# Subroutine to convert a Gregorian date to its equivalnet Julian day number.
def Julian (the_year, the_month, the_day):
  float_1, float_2 = gcal2jd (the_year, the_month, the_day)
  Julian_day_number = int(float_1 + float_2 - 0.5)
  return (Julian_day_number)

# Parse the command line.
arguments = parser.parse_args ()
arguments = vars(arguments)

if (arguments ['trace'] != None):
  do_trace = 1
  trace_file_name = arguments ['trace']
  tracefile = open (trace_file_name, 'wt')

if (arguments ['verbose'] != None):
  verbosity_level = arguments ['verbose']

# If it is not found in the file, the expiration date is today.
expiration_date = datetime.date.today()

# Process the input file.
input_file_name = arguments ['input_file']
line_number = 0
with open (input_file_name, 'rt') as infile:
  text_line = infile.readline()
  while (text_line != ''):
    line_number = line_number + 1
    right_side = text_line
    right_side = right_side.lstrip()
    if (right_side[0:7] == 'Paris, '):
      Paris_line_number = line_number
      right_side = right_side[7:]
      right_side = right_side.rstrip()
      datetime_object = datetime.datetime.strptime (right_side, '%d %B %Y')
      date_object = datetime_object.date()
      date_string = date_object.strftime ('%B %d, %Y')
      print ('Date of IERS Bulletin C is ' + date_string + '.')
    if (right_side[0:11] == 'Bulletin C '):
      right_side = right_side.rstrip()
      print ('This is IERS ' + right_side + '.')
    if (text_line[0:49] == ' NO leap second will be introduced at the end of '):
      print (text_line, end='')
      right_side = text_line[49:]
      right_side = right_side.rstrip()
      right_side = right_side[:-1]
      datetime_object = datetime.datetime.strptime (right_side, '%B %Y')
      date_object = datetime_object.date()
      date_object = date_object.replace(day=15)
      about_six_months = datetime.timedelta(days=180)
      date_object = date_object + about_six_months
      date_object = date_object.replace(day=28)
      date_string = date_object.strftime ('%B %d, %Y')
      print ('Expiration date is ' + date_string + '.')
      expiration_date = date_object
    if ((text_line[0:57] ==
         ' A positive leap second will be introduced at the end of ') or
        (text_line[0:57] ==
         ' A negative leap second will be introduced at the end of ')):
      print (text_line, end='')
      right_side = text_line[57:]
      right_side = right_side.rstrip()
      right_side = right_side[:-1]
      datetime_object = datetime.datetime.strptime (right_side, '%B %Y')
      date_object = datetime_object.date()
      date_object = date_object.replace(day=15)
      about_six_months = datetime.timedelta(days=180)
      date_object = date_object + about_six_months
      date_object = date_object.replace(day=28)
      date_string = date_object.strftime ('%B %d, %Y')
      print ('Expiration date is ' + date_string + '.')
      expiration_date = date_object
    text_line = infile.readline()

if (arguments['expiration_date_file'] != None):
  expiration_date_file_name = arguments ['expiration_date_file']
  expiration_date_file = open (expiration_date_file_name, 'wt')
  expiration_date_Julian = Julian(expiration_date.year, expiration_date.month,
                                  expiration_date.day)
  expiration_date_Gregorian = Gregorian(expiration_date_Julian)
  expiration_date_file.write ("EXPIRATION_DATE=" + str(expiration_date_Julian) +
                              " # " + expiration_date_Gregorian + '\n')
  expiration_date_file.close()
      
if (do_trace == 1):
  tracefile.close()

if (error_counter > 0):
  print ("Encountered " + str(error_counter) + " errors.")
