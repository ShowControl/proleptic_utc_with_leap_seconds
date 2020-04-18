#!/usr/bin/python3
# -*- coding: utf-8
#
# read_delta_t.py reads the file of Delta T values and
# reformats the information into a LaTeX table.
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

import sys
import re
import hashlib
import datetime
import csv
from jdcal import gcal2jd, jd2gcal, is_leap
from scipy.interpolate import interpolate
import pprint
import argparse

parser = argparse.ArgumentParser (
  formatter_class=argparse.RawDescriptionHelpFormatter,
  description='Reformat the file of Delta T values into '
  'a LaTeX table',
  epilog='Copyright © 2019 by John Sauter' + '\n' +
  'License GPL3+: GNU GPL version 3 or later; ' + '\n' +
  'see <http://gnu.org/licenses/gpl.html> for the full text ' +
  'of the license.' + '\n' +
  'This is free software: you are free to change and redistribute it. ' + '\n' +
  'There is NO WARRANTY, to the extent permitted by law. ' + '\n' + '\n'
  'The input file has values for Delta T at various times; ' +
  'the output is a LaTeX table. ' + '\n')
parser.add_argument ('input1_file',
                     help='a Delta T file, in CSV format, with year fractions')
parser.add_argument ('output_file',
                     help='a LaTeX table of the same information')
parser.add_argument ('--version', action='version', 
                     version='reformat_delta_T 1.1 2019-06-18',
                     help='print the version number and exit')
parser.add_argument ('--trace', metavar='trace_file',
                     help='write trace output to the specified file')
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
parser.add_argument ('--verbose', type=int, metavar='verbosity level',
                     help='control the amount of output from the program: ' +
                     '1 is normal, 0 suppresses summary messages')

do_trace = 0
tracefile = ""
latex_start_jdn = 0
latex_end_jdn = 0
have_latex_start_jdn = 0
have_latex_end_jdn = 0
do_gnuplot_output = 0
gnuplot_start_jdn = 0
gnuplot_end_jdn = 0
have_gnuplot_start_jdn = 0
have_gnuplot_end_jdn = 0
verbosity_level = 1
error_counter = 0

# Subroutine to convert a Julian Day Number to its equivalent Gregorian date.
month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul",
               "Aug", "Sep", "Oct", "Nov", "Dec"] 
def greg (jdn, separator, latex_format):
  ymdf = jd2gcal (float(jdn), 0.5)
  year_no = ymdf [0]
  month_no = ymdf [1]
  day_no = ymdf [2]
  month_name = month_names [month_no-1]
  if ((latex_format == 1) & (year_no < 0)):
    return  (str(day_no) + separator + month_name + separator +
            "-" + str(year_no))
  else:
    return (str(day_no) + separator + month_name + separator + str(year_no))

# Subroutine to convert a Gregorian year, month and day to its
# Julian Day Number.

def jdn (year_no, month_no, day_no):
  seq = gcal2jd (year_no, month_no, day_no)
  val = seq[0] + seq[1] - 0.5
  return (int(val))

# Parse the command line.
arguments = parser.parse_args ()
arguments = vars(arguments)

if (arguments ['trace'] != None):
  do_trace = 1
  trace_file_name = arguments ['trace']
  tracefile = open (trace_file_name, 'wt')

if (arguments ['latex_start_jdn'] != None):
  have_latex_start_jdn = 1
  latex_start_jdn = int(arguments ['latex_start_jdn'])

if (arguments ['latex_end_jdn'] != None):
  have_latex_end_jdn = 1
  latex_end_date = int(arguments ['latex_end_jdn'])
    
if (arguments ['gnuplot_output'] != None):
  do_gnuplot_output = 1
  gnuplot_output_file_name = arguments ['gnuplot_output']

if (arguments ['gnuplot_start_jdn'] != None):
  have_gnuplot_start_jdn = 1
  gnuplot_start_jdn = int(arguments ['gnuplot_start_jdn'])

if (arguments ['gnuplot_end_jdn'] != None):
  have_gnuplot_end_jdn = 1
  gnuplot_end_date = int(arguments ['gnuplot_end_jdn'])
    
if (arguments ['verbose'] != None):
  verbosity_level = int(arguments ['verbose'])

# Read the data files into a dictionary and process the data.
delta_t = dict ()

file_name = arguments ['input1_file']
with open (file_name, 'rt') as csvfile:
    reader = csv.DictReader(csvfile)

    # Compute the limits of the data and store it in a list and a dictionary.
    min_year = -1.0
    max_year = -1.0
    for row in reader:
      # Convert year into Julian Day Numbers and populate our dictionary.
      year_float = float(row['year'])
      year_int = int (year_float)
      month_int = (int ((year_float - float(year_int)) * 12.0) + 1)
      if ('month' in row):
        month_int = int(row['month'])
      day_int = 1
      if ('day' in row):
        day_int = int(row['day'])
      this_jdn = jdn (year_int, month_int, day_int)
      delta_t [this_jdn] = float(row['deltaT'])
      # Compute the limits of the date
      new_year = float(row['year'])
      if ((min_year == -1.0) | (min_year > new_year)):
        min_year = new_year
        start_date = this_jdn
      if ((max_year == -1.0) | (max_year < new_year)):
        max_year = new_year
        end_date = this_jdn

min_year_int = int(min_year)
max_year_int = int(max_year + 0.5)

if (verbosity_level > 0):
  print ("Start date is " + str(start_date) + ".5 = " +
         greg (start_date, " ", 0))
if (have_latex_start_jdn == 0):
  latex_start_jdn = int(start_date)
if (have_gnuplot_start_jdn == 0):
  gnuplot_start_jdn = int(start_date)
    
if (verbosity_level > 0):
  print ("End date is " + str(end_date) + ".5 = " + greg (end_date, " ", 0))
if (have_latex_end_jdn == 0):
  latex_end_jdn = int(end_date)
if (have_gnuplot_end_jdn == 0):
  gnuplot_end_jdn = int(end_date)

#
# Output the dates for which we have the value of Delta T
# as LaTeX source, suitable for making a table.
#
latex_file_name = arguments ['output_file']
latex_output_file = open (latex_file_name, 'wt')
latex_output_file.write ("\\begin{longtable}" +
                         "{|r|S[table-number-alignment=right," +
                         "table-figures-integer=5," +
                         "table-figures-decimal=4]|r|}" + "\n")
latex_output_file.write ("\\caption{Values of $\\Delta$T ")
latex_output_file.write ("from " + greg (latex_start_jdn, " ", 1) +
                         " to " +
                         greg (latex_end_jdn, " ", 1) + "} \\\\" + "\n")
latex_output_file.write ("\\hline Date &" +
                         "{$\\Delta$T} &" +
                         " Julian Day \\endhead \\hline " + "\n")
latex_output_file.write ("\\label{table:delta_t}" + "\n")
  
for day_no in sorted(delta_t.keys()):
  if ((day_no >= latex_start_jdn) & (day_no <= latex_end_jdn)):
    delta_t_val = delta_t [day_no]
    latex_output_file.write (greg (day_no, " ", 1) + " & " +
                             str(round(delta_t_val,4)) + "& " +
                             "\\num{" + str(day_no) + ".5}" +
                             "\\\\\\hline" + "\n")
      
latex_output_file.write ("\\end{longtable}" + "\n")
latex_output_file.close()

#
# Optionally, write a file that can be parsed and plotted
# using gnuplot.  The plot will show the change in delta T over time.
#
if ((do_gnuplot_output == 1) & (error_counter == 0)):
  gnuplot_output_file = open (gnuplot_output_file_name, 'wt')
  first_point_plotted = 0
  for day_no in sorted(delta_t.keys()):
    if ((day_no >= gnuplot_start_jdn) & (day_no <= gnuplot_end_jdn)):
      delta_t_val = delta_t [day_no]
      if (first_point_plotted == 0):
        if (day_no > gnuplot_start_jdn):
          gnuplot_output_file.write (str (gnuplot_start_jdn) + ".5 " +
                                     str (delta_t_val) + "\n")
          first_point_plotted = 1
      gnuplot_output_file.write (str (day_no) + ".5 " +
                                 str (delta_t_val) + "\n")

    gnuplot_output_file.write (str (gnuplot_end_jdn) + ".5 " +
                               str (delta_t_val) + "\n")
    gnuplot_output_file.close()

if (do_trace == 1):
  tracefile.close()

if (error_counter > 0):
  print ("Encountered " + str(error_counter) + " errors.")
