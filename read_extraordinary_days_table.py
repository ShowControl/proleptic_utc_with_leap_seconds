#!/usr/bin/python3
# -*- coding: utf-8
#
# read_extraordinary_days_table is a sample program which illustrates how
# to read the table of extraordinary days.

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
from jdcal import gcal2jd, jd2gcal
import pprint
import argparse

parser = argparse.ArgumentParser (
  formatter_class=argparse.RawDescriptionHelpFormatter,
  description='Read the table of extraordinary days.',
  epilog='Copyright © 2017 by John Sauter' + '\n' +
  'License GPL3+: GNU GPL version 3 or later; ' + '\n' +
  'see <http://gnu.org/licenses/gpl.html> for the full text ' +
  'of the license.' + '\n' +
  'This is free software: you are free to change and redistribute it. ' + '\n' +
  'There is NO WARRANTY, to the extent permitted by law. ' + '\n' + '\n'
  'The input file lists the extraordinary days; ' +
  'the output summarizes the information. ' + '\n')
parser.add_argument ('input_file',
                     help='the table of extraordinary days')
parser.add_argument ('--version', action='version', 
                     version='read_extraordinary_days_table 3.0 2025-06-14',
                     help='print the version number and exit')
parser.add_argument ('--trace', metavar='trace_file',
                     help='write trace output to the specified file')
parser.add_argument ('--latex-output', metavar='latex_output_file',
                     help='write data as a LaTeX longtable')
parser.add_argument ('--latex-start-jdn', metavar='latex_start_jdn',
                     help='earliest date to put in table')
parser.add_argument ('--latex-end-jdn', metavar='latex_end_jdn',
                     help='latest date to put in table')
parser.add_argument ('--gnuplot-output', metavar='gnuplot_output_file',
                     help='write data for plotting by gnuplot')
parser.add_argument ('--gnuplot-start-jdn', metavar='gnuplot_start_jdn',
                     help='earliest date to put in the plot')
parser.add_argument ('--gnuplot-end-jdn', metavar='gnuplot_end_jdn',
                     help='latest date to put in the plot')
parser.add_argument ('--c-output', metavar='c_output_file',
                     help='write data for a C program')
parser.add_argument ('--c-start-jdn', metavar='c_start_jdn',
                     help='earliest date to put in the C file')
parser.add_argument ('--c-end-jdn', metavar='c_end_jdn',
                     help='latest date to put in the C file')
parser.add_argument ('--checksum-file', metavar='checksum_file',
                     help='write a checksum line here if needed')
parser.add_argument ('--verbose', type=int, metavar='verbosity level',
                     help='control the amount of output from the program: ' +
                     '1 is normal, 0 suppresses summary messages')

do_trace = 0
tracefile = ""
do_latex_output = 0
latex_output_file = ""
latex_start_jdn = 0
latex_end_jdn = 0
have_latex_start_jdn = 0
have_latex_end_jdn = 0
do_gnuplot_output = 0
gnuplot_start_jdn = 0
gnuplot_end_jdn = 0
have_gnuplot_start_jdn = 0
have_gnuplot_end_jdn = 0
do_c_output = 0
c_start_jdn = 0
c_end_jdn = 0
have_c_start_jdn = 0
have_c_end_jdn = 0
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

# The data is kept in dictionary extraordinary_days, indexed by Julian
# Day number.  The symbols are kept in dictionary symbol_values, indexed
# by symbol name.  The length of each extraordinary day is kept in
# dictionary day_length, indexed by Julian Day Number.
extraordinary_days = {}
symbol_values = {}
day_length = {}

# Parse the command line.
arguments = parser.parse_args ()
arguments = vars(arguments)

if (arguments ['trace'] != None):
  do_trace = 1
  trace_file_name = arguments ['trace']
  tracefile = open (trace_file_name, 'wt')

if (arguments ['latex_output'] != None):
  do_latex_output = 1
  latex_output_file_name = arguments ['latex_output']

if (arguments ['latex_start_jdn'] != None):
  have_latex_start_jdn = 1
  latex_start_jdn = int(arguments ['latex_start_jdn'])

if (arguments ['latex_end_jdn'] != None):
  have_latex_end_jdn = 1
  latex_end_jdn = int(arguments ['latex_end_jdn'])
    
if (arguments ['gnuplot_output'] != None):
  do_gnuplot_output = 1
  gnuplot_output_file_name = arguments ['gnuplot_output']

if (arguments ['gnuplot_start_jdn'] != None):
  have_gnuplot_start_jdn = 1
  gnuplot_start_jdn = int(arguments ['gnuplot_start_jdn'])

if (arguments ['gnuplot_end_jdn'] != None):
  have_gnuplot_end_jdn = 1
  gnuplot_end_date = int(arguments ['gnuplot_end_jdn'])
    
if (arguments ['c_output'] != None):
  do_c_output = 1
  c_output_file_name = arguments ['c_output']

if (arguments ['c_start_jdn'] != None):
  have_c_start_jdn = 1
  c_start_jdn = int(arguments ['c_start_jdn'])

if (arguments ['c_end_jdn'] != None):
  have_c_end_jdn = 1
  c_end_date = int(arguments ['c_end_jdn'])
    
if (arguments ['verbose'] != None):
  verbosity_level = int(arguments ['verbose'])

# Read the data file into memory.
file_name = arguments ['input_file']
infile = open (file_name, 'rb')
# Read the file into memory as a list of byte strings.
file_data = infile.readlines()
infile.close()

# Classify each line as either an empty line, a symbol=value line, or a
# data line.  Remember the value associated with each symbols and the data.
line_number = 0
previous_jdn = 0
previous_DTAI = 0
first_data_line = 1

for byte_string in file_data:
# The file data is assumed to be coded as utf-8.  Decode it into Unicode.
  line = byte_string.decode ('utf-8')
  line_number = line_number + 1
  if (re.match ("^\\s*(#.*)?\n$", line)):
    continue;                   #  ignore empty lines.
  matchc = re.match ("^\\s*(?P<keyword>(\\w)+)\\s*=\\s*(?P<value>(\\w)+)\\s*(#.*)?\n$", line)
  if (matchc):
    # This line has the form keyword = value
    keyword = matchc.groupdict () ['keyword']
    value = matchc.groupdict() ['value']
    if keyword in symbol_values:
      print ("Keyword " + keyword + " seen more than once.")
      error_counter = error_counter + 1
    symbol_values[keyword] = value;
    if (do_trace == 1):
      tracefile.write ("Keyword " + keyword + "=" + value + "\n")
    continue

  matchd = re.match ("^\\s*(?P<jdn>(\\d)+)\\s+(?P<lod>(\\d)+)\\s+(?P<DTAI>-?(\\d)+)\\s*(#.*)?\n$", line)
  if (matchd):
    # This line has the form julian_day_number DTAI
    jdn = int(matchd.groupdict () ['jdn'])
    lod = int(matchd.groupdict () ['lod'])
    DTAI = int(matchd.groupdict () ['DTAI'])
    if jdn in extraordinary_days:
      print ("Julian Day Number " + str(jdn) + " seen more than once.")
      error_counter = error_counter + 1
    if jdn < previous_jdn:
      print ("Julian Day Number " + str(jdn) + " out of order.")
      error_counter = error_counter + 1

    if (first_data_line == 0):
      if (abs(int(DTAI) - int(previous_DTAI)) != 1):
        print ("At Julian Day Number " + str(jdn) + ", DTAI of " + str(DTAI) +
               " does not differ from the previous DTAI of " +
               str(previous_DTAI) + " by plus or minus 1." + "\n")
        error_counter = error_counter + 1
    day_length[int(jdn)] = lod
    extraordinary_days[int(jdn)] = int(DTAI)
    previous_jdn = jdn
    previous_DTAI = DTAI
    first_data_line = 0
    if (do_trace == 1):
      tracefile.write ("At Julian Day Number " + str(jdn) +
                       " DTAI was " + str(DTAI) + "." + "\n")
    continue

  # This line is not recognized
  print ("Line " + str(line_number) + " is not recognized.")
  print (line)
  error_counter = error_counter + 1

# Verify that the start, end and expiration dates are specified.
# If the checksum is missing we will print the correct value and
# ask that it be added.  Optionally we will also write the correct
# checksum line to a file, to facilitate automatic building of
# the file.
if ("START_DATE" not in symbol_values):
  print ("Start date is missing.")
  error_counter = error_counter + 1
else:
  start_date = symbol_values ["START_DATE"]
  if (verbosity_level > 0):
    print ("Start date is " + str(start_date) + ".5 = " +
           greg (start_date, " "))
  if (have_latex_start_jdn == 0):
    latex_start_jdn = int(start_date)
  if (have_gnuplot_start_jdn == 0):
    gnuplot_start_jdn = int(start_date)
  if (have_c_start_jdn == 0):
    c_start_jdn = int(start_date)
    
if ("END_DATE" not in symbol_values):
  print ("End date is missing.")
  error_counter = error_counter + 1
else:
  end_date = symbol_values ["END_DATE"]
  if (verbosity_level > 0):
    print ("End date is " + str(end_date) + ".5 = " + greg (end_date, " "))
  if (have_latex_end_jdn == 0):
    latex_end_jdn = int(end_date)
  if (have_gnuplot_end_jdn == 0):
    gnuplot_end_jdn = int(end_date)
  if (have_c_end_jdn == 0):
    c_end_jdn = int(end_date)
    
if ("EXPIRATION_DATE" not in symbol_values):
  print ("Expiration date is missing.")
  error_counter = error_counter + 1
else:
  expiration_date = int(symbol_values ["EXPIRATION_DATE"])
  if (verbosity_level > 0):
    print ("Expiration date is " + str(expiration_date) + ".5 = " + 
           greg (expiration_date, " "))
  today = datetime.datetime.now()
  today_jdn_pair = gcal2jd (today.year, today.month, today.day)
  today_jdn = int(today_jdn_pair [0] + today_jdn_pair [1] - 0.5)
  if (verbosity_level > 1):
    print ("Today, " + greg (today_jdn, " ") + ", " +
           " expressed as a Julian Day Number, is " + str(today_jdn) + ".5.")
  if (today_jdn > expiration_date):
    print ("This file has expired.  You should find a later version," +
           " or update it yourself" + "\n" +
           "using leap second information from the IERS.")
    error_counter = error_counter + 1

 # If no errors have been detected yet, look for out-of-range data values.
if (error_counter == 0):
  for extraordinary_day in extraordinary_days:
    if (extraordinary_day < int(symbol_values["START_DATE"])):
      print ("Julian Day Number " + str(extraordinary_day) +
             " is before the start date of " + symbol_values["START_DATE"])
      error_counter = error_counter + 1
      if (extraordinary_day > int(symbol_values["END_DATE"])):
        print ("Julian Day NUmber " + str(extraordinary_day) +
               " is after the end date of " + symbol_values["END_DATE"])
        error_counter = error_counter + 1

# If there are still no errors, compute the checksum.
if (error_counter == 0):
  hash_function = hashlib.new('sha256')
  for byte_string in file_data:
    # Don't include the checksum line.
    omit_checksum = 0
    line = byte_string.decode ('utf-8')
    matchc = re.match ("^\\s*(?P<keyword>(\\w)+)\\s*=\\s*(?P<value>(\\w)+)\\s*(#.*)?\n$", line)
    if (matchc):
      # This line has the form keyword = value
      keyword = matchc.groupdict () ['keyword']
      value = matchc.groupdict() ['value']
      if (keyword == "CHECKSUM"):
        omit_checksum = 1
    if (omit_checksum == 0):
      hash_function.update (byte_string)
  computed_checksum = hash_function.hexdigest()
  if ("CHECKSUM" in symbol_values):
    if (symbol_values ["CHECKSUM"] != computed_checksum):
      print ("Checksum is incorrect.\n" +
             "Value in file is " + symbol_values ["CHECKSUM"] + ", " + "\n" +
             "but computed value is " + computed_checksum + "\n")
    else:
      if (verbosity_level > 0):
        print ("Checksum is correct.")
  else:
    print ("No checksum value in file.  Please add this line:\n" +
           "CHECKSUM=" + computed_checksum )
    if (arguments ['checksum_file'] != None):
      checksum_file_name = arguments ['checksum_file']
      checksumfile = open (checksum_file_name, 'wt')
      checksumfile.write ("CHECKSUM=" + computed_checksum + "\n")
      checksumfile.close()
#
# Now do something useful with the data, as an example.
# Here we output the list of extraordinary days and the value of DTAI at the
# end of the day as LaTeX source, suitable for making a table.
#
if ((do_latex_output == 1) & (error_counter == 0)):
  latex_output_file = open (latex_output_file_name, 'wt')
  latex_output_file.write ("\\begin{longtable}{|c|c|r|l|}" + "\n")
  latex_output_file.write ("\\caption{Extraordinary days ")
  latex_output_file.write ("from " + greg (latex_start_jdn, " ") + " to " +
                           greg (latex_end_jdn, " ") + "} \\\\" + "\n")
  latex_output_file.write ("\\hline Julian Day Number &" +
                           " length in seconds &" +
                           " DTAI &" +
                           " Day Month Year \\endhead \\hline " + "\n")
  latex_output_file.write ("\\label{table:JDN_DTAI}" + "\n")

  for extraordinary_day in sorted(extraordinary_days.keys()):
    if ((extraordinary_day >= latex_start_jdn) and
        (extraordinary_day <= latex_end_jdn)):
      DTAI = extraordinary_days [extraordinary_day]
      if extraordinary_day in day_length:
        jdn_length = day_length [extraordinary_day]
      else:
        jdn_length = 86400
      latex_output_file.write ("\\num{" +
                               str(extraordinary_day) + ".5} & " +
                               "\\num{" + str(jdn_length) + "} & " +
                               "\\num{" + str(DTAI) + "} & " +
                               "\\# " + greg (extraordinary_day, " ") +
                               "\\\\\\hline" + "\n")

  latex_output_file.write ("\\end{longtable}" + "\n")
  latex_output_file.close()

#
# Here is another example: write a file that can be parsed and plotted
# using gnuplot.  The plot will show the change in DTAI over time.
#
if ((do_gnuplot_output == 1) & (error_counter == 0)):
  gnuplot_output_file = open (gnuplot_output_file_name, 'wt')
  first_point_plotted = 0
  for extraordinary_day in sorted(extraordinary_days.keys()):
    if ((extraordinary_day >= gnuplot_start_jdn) and
        (extraordinary_day <= gnuplot_end_jdn)):
      DTAI = extraordinary_days [extraordinary_day]
      if (first_point_plotted == 0):
        if (extraordinary_day > gnuplot_start_jdn):
          gnuplot_output_file.write (str (gnuplot_start_jdn) + " " +
                                     str (DTAI) + "\n")
        first_point_plotted = 1
      gnuplot_output_file.write (str (extraordinary_day) + " " +
                                 str (DTAI) + "\n")

  gnuplot_output_file.write (str (gnuplot_end_jdn) + " " +
                             str (DTAI) + "\n")
  gnuplot_output_file.close()

#
# In this example we write a file which can be used in a C program
# to initialize a two-dimensional array.  The first dimension is
# the number of entries.  The second dimension has the Julian Day
# Number of the day which starts (not ends, as in the above examples)
# with a new value of DTAI, and that new DTAI value.
#
if ((do_c_output == 1) and (error_counter == 0)):
  c_output_file = open (c_output_file_name + ".tab", 'wt')
  first_date_written = 0
  number_of_entries = 0
  for extraordinary_day in sorted(extraordinary_days.keys()):
    if ((extraordinary_day >= c_start_jdn) and
        (extraordinary_day <= c_end_jdn)):
      DTAI = extraordinary_days [extraordinary_day]
      if (first_date_written == 0):
        if (extraordinary_day > c_start_jdn):
          c_output_file.write (
            "{" + str (c_start_jdn + 1) + ", " + str (DTAI) + "}, " +
            "/* " + greg(c_start_jdn+1, " ") + " */\n")
        first_date_written = 1
        number_of_entries = number_of_entries + 1
      c_output_file.write (
        "{" + str (extraordinary_day+1) + ", " + str (DTAI) + "}, " +
        "/* " + greg(extraordinary_day+1, " ") + " */\n")
      number_of_entries = number_of_entries + 1

  c_output_file.write (
    "{" + str (c_end_jdn) + ", " + str (DTAI) + "}, " +
    "/* " + greg(c_end_jdn, " ") + " */\n")
  number_of_entries = number_of_entries + 1
  c_output_file.close()

  #
  # Also write a header file giving the size of the table.
  #
  c_output_file = open (c_output_file_name + ".h", 'wt')
  c_output_file.write (
    "#define DTAI_ENTRY_COUNT " + str(number_of_entries) + "\n")
  c_output_file.close()

if (do_trace == 1):
  tracefile.close()

if (error_counter > 0):
  print ("Encountered " + str(error_counter) + " errors.")
