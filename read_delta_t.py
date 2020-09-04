#!/usr/bin/python3
# -*- coding: utf-8
#
# read_delta_t.py reads the file of Delta T values and other files
# to estimate delta T, then creates various useful files based on
# the data.
#
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
import csv
from jdcal import gcal2jd, jd2gcal, is_leap
import numpy as np
from numpy.polynomial import Polynomial
import pandas as pd
from scipy.interpolate import interpolate
import pprint
import argparse

parser = argparse.ArgumentParser (
  formatter_class=argparse.RawDescriptionHelpFormatter,
  description='Convert the file of Delta T values into '
  'a list of extraordinary days.',
  epilog='Copyright © 2020 by John Sauter' + '\n' +
  'License GPL3+: GNU GPL version 3 or later; ' + '\n' +
  'see <http://gnu.org/licenses/gpl.html> for the full text ' +
  'of the license.' + '\n' +
  'This is free software: you are free to change and redistribute it. ' + '\n' +
  'There is NO WARRANTY, to the extent permitted by law. ' + '\n' + '\n'
  'The input file has values for Delta T at various times; ' +
  'the output summarizes the information. ' + '\n')
parser.add_argument ('input1_file',
                     help='a Delta T file, in CSV format, with year fractions')
parser.add_argument ('output_file',
                     help='the resulting list of extraordinary days')
parser.add_argument ('--version', action='version', 
                     version='read_Delta_T 7.6 2020-09-01',
                     help='print the version number and exit')
parser.add_argument ('--trace', metavar='trace_file',
                     help='write trace output to the specified file')
parser.add_argument ('--USNO-delta-t', metavar='USNO_delta_t_input_file',
                     help='Read Delta T information from the USNO')
parser.add_argument ('--USNO-delta-t-predictions',
                     metavar='USNO_delta_t_preds_input_file',
                     help='Read Delta T predictions from the USNO')
parser.add_argument ('--IERS-Bulletin-A',
                     metavar='IERS_Bulletin_A_input_file',
                     help='Read UT1-UTC projection formula from IERS Bulletin A')
parser.add_argument ('--IERS-projection-days', type=int, default=1000,
                     metavar='IERS_projection_days',
                     help='Number of days to project delta T using the IERS formula in Bulletin A')
parser.add_argument ('--IERS-final', metavar='IERS_final_input_file',
                     help='Read Delta T information from the IERS')
parser.add_argument ('--IERS-leaps', action='store_true',
                     help='Use the IERS leap seconds starting in 1972')
parser.add_argument ('--Tony-Finch-leaps', action='store_true',
                     help='Use the Tony Finch leap seconds from 1958 through 1971')
parser.add_argument ('--latex-output', metavar='latex_output_file',
                     help='write delta T data as a LaTeX longtable')
parser.add_argument ('--latex-start-jdn', metavar='latex_start_jdn',
                     help='earliest date to put in table')
parser.add_argument ('--latex-end-jdn', metavar='latex_end_jdn',
                     help='latest date to put in table')
parser.add_argument ('--csv-output', metavar='csv_output_file',
                     help='write delta T data as a CSV file')
parser.add_argument ('--csv-start-jdn', metavar='csv_start_jdn',
                     help='earliest date to put in CSV file')
parser.add_argument ('--csv-end-jdn', metavar='csv_end_jdn',
                     help='latest date to put in CSV file')
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
parser.add_argument ('--UT1UTC-output', metavar='UT1UTC_output_file',
                     help='write UT1-UTC values')
parser.add_argument ('--UT1UTC-start-jdn', metavar='UT1UTC_start_jdn',
                     help='earliest date to put in the UT1-UTC file')
parser.add_argument ('--UT1UTC-end-jdn', metavar='UT1UTC_end_jdn',
                     help='latest date to put in the UT1-UTC file')
parser.add_argument ('--verbose', type=int, metavar='verbosity level',
                     help='control the amount of output from the program: ' +
                     '1 is normal, 0 suppresses summary messages')

do_trace = 0
tracefile = ""
do_USNO_delta_t_input = 0
USNO_delta_t_input_file = ""
do_IERS_projections = 0
IERS_Bulletin_A_input_file = ""
do_USNO_delta_t_preds_input = 0
USNO_delta_t_preds_input_file = ""
do_IERS_final_input = 0
IERS_final_input_file = ""
do_IERS_leaps = 0
do_Tony_Finch_leaps = 0
do_latex_output = 0
latex_output_file = ""
latex_start_jdn = 0
latex_end_jdn = 0
have_latex_start_jdn = 0
have_latex_end_jdn = 0
do_csv_output = 0
csv_output_file = ""
csv_start_jdn = 0
csv_end_jdn = 0
have_csv_start_jdn = 0
have_csv_end_jdn = 0
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
do_UT1UTC_output = 0
UT1UTC_start_jdn = 0
UT1UTC_end_jdn = 0
have_UT1UTC_start_jdn = 0
have_UT1UTC_end_jdn = 0
verbosity_level = 1
error_counter = 0

# Subroutine to convert a Julian Day Number to its equivalent Gregorian date.
# format_no == 0: 01-Jan-2000
# format_no == 1: double the "-' on negative years for LaTeX
# format_no == 2: =date(2000,1,1) for a spreadsheet
month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul",
               "Aug", "Sep", "Oct", "Nov", "Dec"] 
def greg (jdn, separator, format_no):
  ymdf = jd2gcal (float(jdn), 0.5)
  year_no = ymdf [0]
  month_no = ymdf [1]
  day_no = ymdf [2]
  month_name = month_names [month_no-1]
  if (format_no == 2):
    return ("=date(" + str(year_no) + "," + str(month_no) + "," +
            str(day_no) + ")")
  if ((format_no == 1) & (year_no < 0)):
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

# Subroutine to do the reverse:
def ymd_from_JDN (this_JDN):
  ymdf = jd2gcal (float(this_JDN), 0.5)
  year_no = ymdf [0]
  month_no = ymdf [1]
  mday_no = ymdf [2]
  return (year_no, month_no, mday_no)

# Parse the command line.
arguments = parser.parse_args ()
arguments = vars(arguments)

if (arguments ['trace'] != None):
  do_trace = 1
  trace_file_name = arguments ['trace']
  tracefile = open (trace_file_name, 'wt')

if (arguments ['USNO_delta_t'] != None):
  do_USNO_delta_t_input = 1
  USNO_delta_t_file_name = arguments ['USNO_delta_t']

if (arguments ['USNO_delta_t_predictions'] != None):
  do_USNO_delta_t_preds_input = 1
  USNO_delta_t_preds_file_name = arguments ['USNO_delta_t_predictions']

if (arguments ['IERS_final'] != None):
  do_IERS_final_input = 1
  IERS_final_file_name = arguments ['IERS_final']

if (arguments ['IERS_Bulletin_A'] != None):
  do_IERS_projections = 1
  IERS_Bulletin_A_file_name = arguments ['IERS_Bulletin_A']

if (arguments ['IERS_projection_days'] != None):
    IERS_projection_days = arguments ['IERS_projection_days']
    
if (arguments ['IERS_leaps']):
  do_IERS_leaps = 1

if (arguments ['Tony_Finch_leaps']):
  do_Tony_Finch_leaps = 1

if (arguments ['latex_output'] != None):
  do_latex_output = 1
  latex_output_file_name = arguments ['latex_output']

if (arguments ['latex_start_jdn'] != None):
  have_latex_start_jdn = 1
  latex_start_jdn = int(arguments ['latex_start_jdn'])

if (arguments ['latex_end_jdn'] != None):
  have_latex_end_jdn = 1
  latex_end_date = int(arguments ['latex_end_jdn'])
    
if (arguments ['csv_output'] != None):
  do_csv_output = 1
  csv_output_file_name = arguments ['csv_output']

if (arguments ['csv_start_jdn'] != None):
  have_csv_start_jdn = 1
  csv_start_jdn = int(arguments ['csv_start_jdn'])

if (arguments ['csv_end_jdn'] != None):
  have_csv_end_jdn = 1
  csv_end_date = int(arguments ['csv_end_jdn'])
    
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
    
if (arguments ['UT1UTC_output'] != None):
  do_UT1UTC_output = 1
  UT1UTC_output_file_name = arguments ['UT1UTC_output']

if (arguments ['UT1UTC_start_jdn'] != None):
  have_UT1UTC_start_jdn = 1
  UT1UTC_start_jdn = int(arguments ['UT1UTC_start_jdn'])

if (arguments ['UT1UTC_end_jdn'] != None):
  have_UT1UTC_end_jdn = 1
  UT1UTC_end_date = int(arguments ['UT1UTC_end_jdn'])
    
if (arguments ['verbose'] != None):
  verbosity_level = int(arguments ['verbose'])

# Create a function to interpolate the value of delta T.
delta_t = dict ()
# We will need to rebuild it when we change the data points we know.
def rebuild_interpolations():
  global deltaT
  delta_t_days = list(delta_t.keys())
  delta_t_values = list(delta_t.values())
  deltaT = interpolate.interp1d (delta_t_days, delta_t_values,
                               kind="slinear")
  return

# Record the source of delta T values.
delta_t_source = dict()

# Record all sources of delta T information.
# delta_t_all is a dictionary indexed source names.
# Each element is a dictionary indexed by Julian Day Number giving the
# value of delta T according to that source.
delta_t_all = dict()
source_list = list()

# Read the delta T data file into a dictionary.
# This first file is the delta T values for the past and future,
# based on old records of eclipses and lunar occulations.

file_name = arguments ['input1_file']
with open (file_name, 'rt') as csvfile:
    reader = csv.DictReader(csvfile)

    if (do_trace == 1):
      tracefile.write ("Reading " + file_name + ".\n")
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
      this_JDN = jdn (year_int, month_int, day_int)
      this_MJD = this_JDN - 2400000
      if ("MJD" in row):
        this_MJD = int(row["MJD"])
      this_delta_t = float(row['deltaT'])
      delta_t [this_JDN] = this_delta_t
      if (year_int <= 2015):
        source = "Eclipses and Lunar Occulations"
      else:
        source = "Astronomical Projection"
      delta_t_source[this_JDN] = source
      if (source not in delta_t_all):
        delta_t_all[source] = dict()
        source_list = source_list + [source]
      this_delta_t_source = delta_t_all[source]
      this_delta_t_source[this_JDN] = this_delta_t
      if (do_trace == 1):
        tracefile.write ("JDN " + str(this_JDN) + ": " +
                         "Year " + str(year_int) + " " +
                         "Month " + str(month_int) + " " +
                         "Day of month " + str(day_int) + " " +
                         "MJD " + str(this_MJD) + " " +
                         "deltaT " + str(delta_t[this_JDN]) + ".\n")
      # Track the limits of the date
      new_year = float(row['year'])
      if ((min_year == -1.0) | (min_year > new_year)):
        min_year = new_year
        start_date = this_JDN
      if ((max_year == -1.0) | (max_year < new_year)):
        max_year = new_year
        end_date = this_JDN

# Adjust the values of delta_t so January 1, 1058, is 32.184.
DTAI_base_date = jdn(1958, 1, 1)
DTAI_base_dt = delta_t [DTAI_base_date]
for this_JDN in delta_t:
  old_delta_t = delta_t[this_JDN]
  delta_t[this_JDN] = old_delta_t + 32.184 - DTAI_base_dt

for source in source_list:
  this_delta_t_source = delta_t_all[source]
  for this_JDN in this_delta_t_source:
    old_delta_t = this_delta_t_source[this_JDN]
    this_delta_t_source[this_JDN] = old_delta_t + 32.184 - DTAI_base_dt
    
DTAI_base_dt = delta_t [DTAI_base_date]

rebuild_interpolations()

# Optionally, include the near-future estimates of Delta T from the
# U. S. Naval Observatory, overriding the predictions based on historical
# data.
if (do_USNO_delta_t_preds_input):
  source = "USNO delta T projection"
  if (do_trace == 1):
    tracefile.write ("Delta T predictions from USNO:\n")
  with open (USNO_delta_t_preds_file_name, 'rt') as csvfile:
    reader = csv.DictReader(csvfile,delimiter=';')
    for row in reader:
      year_float = float(row['YEAR'])
      year_int = int (year_float)
      month_int = (int ((year_float - float(year_int)) * 12.0) + 1)
      day_int = 1
      this_JDN = jdn (year_int, month_int, day_int)
      new_delta_t = float(row['TT-UT Pred']) 
      if (this_JDN in delta_t):
        old_delta_t = delta_t[this_JDN]
        difference = new_delta_t - old_delta_t
        if (do_trace == 1):
          tracefile.write (greg(this_JDN, " ", 0) + ": Delta T changes" +
                           " from " + str(old_delta_t) +
                           " by " + str(difference) +
                           " to " + str(new_delta_t) + ".\n")
      else:
        old_delta_t = deltaT(this_JDN)
        difference = new_delta_t - old_delta_t
        if (do_trace == 1):
          tracefile.write (greg(this_JDN, " ", 0) + ": Delta T changes" +
                           " from " + str(old_delta_t) + " (interpolated)" +
                           " by " + str(difference) +
                           " to " + str(new_delta_t) + ".\n")
      delta_t[this_JDN] = new_delta_t
      delta_t_source[this_JDN] = source
      if (source not in delta_t_all):
        delta_t_all[source] = dict()
        source_list = source_list + [source]
      this_delta_t_source = delta_t_all[source]
      this_delta_t_source[this_JDN] = new_delta_t

    rebuild_interpolations()
      
# Optionally, override the Delta T values from historical data and from
# the USNO's own predictions with observed data from USNO.
if (do_USNO_delta_t_input):
  source = "USNO delta T records"
  if (do_trace == 1):
    tracefile.write ("Delta T values from USNO:\n")
  with open (USNO_delta_t_file_name, 'rt') as csvfile:
    reader = csv.DictReader(csvfile,delimiter=';')
    # Overwrite the data from the first file with the data from this
    # file, where they conflict.
    for row in reader:
      # Convert year into Julian Day Numbers and populate our dictionary.
      year_float = float(row['year'])
      year_int = int (year_float)
      month_int = int(row['month'])
      day_int = int(row['day'])
      this_JDN = jdn (year_int, month_int, day_int)
      new_delta_t = float(row['delta_T'])
      if (this_JDN in delta_t):
        old_delta_t = delta_t[this_JDN]
        difference = new_delta_t - old_delta_t
        if (do_trace == 1):
          tracefile.write (greg(this_JDN, " ", 0) + ": Delta T changes" +
                           " from " + str(old_delta_t) +
                           " by " + str(difference) +
                           " to " + str(new_delta_t) + ".\n")
      else:
        old_delta_t = deltaT(this_JDN)
        difference = new_delta_t - old_delta_t
        if (do_trace == 1):
          tracefile.write (greg(this_JDN, " ", 0) + ": Delta T changes" +
                           " from " + str(old_delta_t) + " (interpolated)" +
                           " by " + str(difference) +
                           " to " + str(new_delta_t) + ".\n")
      delta_t[this_JDN] = new_delta_t
      delta_t_source[this_JDN] = source
      if (source not in delta_t_all):
        delta_t_all[source] = dict()
        source_list = source_list + [source]
      this_delta_t_source = delta_t_all[source]
      this_delta_t_source[this_JDN] = new_delta_t

  rebuild_interpolations()

  #
  # Tell the trace file the resulting delta T and delta T source information.
  #
  if (do_trace == 1):
    tracefile.write ("After " + source + ":\n")
    tracefile.write ("delta_t:\n")
    pprint.pprint (delta_t, tracefile)
    tracefile.write ("delta_t_source:\n")
    pprint.pprint (delta_t_source, tracefile)
  
#
# The most accurate source of delta T information available is the
# daily UT1-UTC values kept by the IERS.  However, to convert
# UT1-UTC to delta T, we must know how many leap seconds have been
# counted up to the specified date.  Create a dictionary to hold
# that information.
#
leap_dates = dict ()
leap_count = 10

# Record a leap second.
def record_leap (year, month, day):
  global leap_count
  leap_count = leap_count + 1
  this_JDN = jdn (year, month, day)
  leap_dates[this_JDN] = leap_count
  return

# Compute the number of leap seconds before the specified day.
def leaps_since (this_JDN):
  test_jdn = this_JDN - 1
  while (test_jdn not in leap_dates):
    test_jdn = test_jdn - 1
  return leap_dates [test_jdn]

#
# The official leap seconds table from IERS,
# last updated July 7, 2016, to include December 31, 2016.
#
record_leap(1972,6,30)
record_leap(1972,12,31)
record_leap(1973,12,31)
record_leap(1974,12,31)
record_leap(1975,12,31)
record_leap(1976,12,31)
record_leap(1977,12,31)
record_leap(1978,12,31)
record_leap(1979,12,31)
record_leap(1981,6,30)
record_leap(1982,6,30)
record_leap(1983,6,30)
record_leap(1985,6,30)
record_leap(1987,12,31)
record_leap(1989,12,31)
record_leap(1990,12,31)
record_leap(1992,6,30)
record_leap(1993,6,30)
record_leap(1994,6,30)
record_leap(1995,12,31)
record_leap(1997,6,30)
record_leap(1998,12,31)
record_leap(2005,12,31)
record_leap(2008,12,31)
record_leap(2012,6,30)
record_leap(2015,6,30)
record_leap(2016,12,31)

#
# If requested, project values of Delta T based on a formula from
# the latest IERS Bulletin A.
#

def UT2_seasonal (target_JDN):
  target_MJD = target_JDN - 2400000
  # Target_T is the Besselian year.
  target_T = 2000.000 + ((float(target_MJD) - 51544.03) / 365.2422)
  return (0.022 * np.sin(2.0*np.pi*target_T)
          - 0.012 * np.cos(2.0*np.pi*target_T)
          - 0.006 * np.sin(4.0*np.pi*target_T)
          + 0.007 * np.cos(4.0*np.pi*target_T))

if (do_IERS_projections):
  
  if (do_trace== 1):
    tracefile.write ("Delta T based on the IERS projection for UT1-UTC:\n")

  # Project UT1-UTC and thus deltaT using formulas from the IERS Bulletin A.
  
  source = "IERS UT1-UTC projection"
  future_source = "Astronomical Projection"

  # Scan the text of IERS Bulletin A, downloaded from their web site, to
  # extract the formula for projecting UT1-UTC.
  
  line_number = 0
  with open (IERS_Bulletin_A_file_name, 'rt') as infile:
    text_line = infile.readline()
    while (text_line != ''):
      line_number = line_number + 1
      if (line_number == 8):
        left_side = text_line[0:40]
        left_side = left_side.rstrip()
        left_side = left_side.lstrip()
        datetime_object = datetime.datetime.strptime (left_side, '%d %B %Y')
        date_object = datetime_object.date()
        if (verbosity_level > 0):
          print ('IERS Bulletin A is dated ' +
                 date_object.strftime('%A %B %d, %Y') + ".")
        if (do_trace == 1):
          tracefile.write ("IERS Bulletin A is dated " +
                           date_object.strftime('%A %B %d, %Y') + ".\n")
      if (text_line[0:19] == '         UT1-UTC = '):
        UT2_offset = text_line[19:26]
        UT2_offset = float(UT2_offset)
        UT2_slope = text_line[27] + text_line[29:36]
        UT2_slope = float(UT2_slope)
        UT2_base_MJD = text_line[44:49]
        UT2_base_MJD = int(UT2_base_MJD)
      text_line = infile.readline()

  UT2_base_JDN = UT2_base_MJD + 2400000
  start_MJD = UT2_base_MJD
  end_MJD = start_MJD + IERS_projection_days
  if (verbosity_level > 0):
    print ("UT2_base_MJD = " + str(UT2_base_MJD) +
           ", UT2_slope = " + format(UT2_slope, ".5f") +
           ", UT2_offset = " + str(UT2_offset) + "\n" +
           "  projected for " + str(IERS_projection_days) + " days: " +
           " from " + greg (UT2_base_JDN, "-", 0) +  " to " +
           greg (end_MJD + 2400000, "-", 0) + ".")
        
  if (do_trace == 1):
    tracefile.write ("UT2_base_MJD = " + str(UT2_base_MJD) +
                     ", UT2_slope = " + str(UT2_slope) +
                     ", UT2_offset = " + str(UT2_offset) +
                     ", projected for " + str(IERS_projection_days) +
                     " days: from " + greg (UT2_base_JDN, "-", 0) +
                     " to " + greg (end_MJD + 2400000, "-", 0) +
                     ".\n")
  leap_offset = 0

  for target_MJD in range(start_MJD, end_MJD):
    target_JDN = target_MJD + 2400000

    # Estimate UT1-UTC (ignoring future leap seconds) using the formula
    # provided by the IERS.
    ut1_minus_utc = (UT2_offset + (UT2_slope * (target_MJD - UT2_base_MJD)) -
                     UT2_seasonal (target_JDN))
    
    # We must deduce Delta T from UT1-UTC, which requires
    # knowing how many leap seconds have passed.
    # The projection ignores future leap seconds, so we do too.
    leaps_since_JDN = leaps_since (UT2_base_JDN)
    new_delta_t = 32.184 - ut1_minus_utc + leaps_since_JDN
    if (do_trace == 1):
      tracefile.write (" ut1_minus_utc = " + str(ut1_minus_utc) +
                       " leaps since = " + str(leaps_since_JDN) + ".\n")
    if (target_JDN in delta_t):
      old_delta_t = delta_t[target_JDN]
      difference = new_delta_t - old_delta_t
      if (do_trace == 1):
        tracefile.write (greg(target_JDN, " ", 0) + ": Delta T changes" +
                         " from " + str(old_delta_t) +
                         " by " + str(difference) +
                         " to " + str(new_delta_t) + ".\n")
    else:
      old_delta_t = deltaT(target_JDN)
      difference = new_delta_t - old_delta_t
      if (do_trace == 1):
        tracefile.write (greg(target_JDN, " ", 0) + ": Delta T changes" +
                         " from " + str(old_delta_t) + " (interpolated)" +
                         " by " + str(difference) +
                         " to " + str(new_delta_t) + ".\n")
    delta_t [target_JDN] = new_delta_t
    delta_t_source[target_JDN] = source
    delta_t_source[target_JDN+1] = future_source
    delta_t[target_JDN] = new_delta_t
    delta_t_source[target_JDN] = source
    if (source not in delta_t_all):
      delta_t_all[source] = dict()
      source_list = source_list + [source]
    this_delta_t_source = delta_t_all[source]
    this_delta_t_source[target_JDN] = new_delta_t

  #
  # Tell the trace file the resulting delta T and delta T source information.
  #
  if (do_trace == 1):
    tracefile.write ("After " + source + ":\n")
    tracefile.write ("delta_t:\n")
    pprint.pprint (delta_t, tracefile)
    tracefile.write ("delta_t_source:\n")
    pprint.pprint (delta_t_source, tracefile)

#
# If requested, read the latest information about Earth orientation
# from the IERS, and extract Delta T information from it.
#
last_delta_T_from_IERS = 0
last_delta_T_from_IERS_date = 0

if (do_IERS_final_input):

  if (do_trace == 1):
    tracefile.write ("Delta T deduced from IERS values of UT1-UTC:\n")

  # Read the values of UT1-UTC provided by the IERS.  These are daily
  # values since 1973 up to the present, and predicted for the next
  # year.
  finals_fieldnames = ["MJD", "Year", "Month", "Day",
                       "type_pole", "x_pole", "sigma_x_pole",
                       "y_pole", "sigma_y_pole",
                       "type_UT1-UTC", "UT1-UTC", "sigma_UT1-UTC",
                       "LOD", "sigma_LOD"]
  with open (IERS_final_file_name, 'rt', newline="") as csvfile:
    reader = csv.DictReader(csvfile,delimiter=';',
                            fieldnames=finals_fieldnames, restkey="remainder")
    for row in reader:
      if (row["MJD"] != "MJD"):
        # Convert year month and day into Julian Day Numbers
        # and populate our dictionary.
        year_float = float(row['Year'])
        year_int = int (year_float)
        month_int = (int ((year_float - float(year_int)) * 12.0) + 1)
        if ('Month' in row):
          month_int = int(row['Month'])
          day_int = 1
        if ('Day' in row):
          day_int = int(row['Day'])
        this_JDN = jdn (year_int, month_int, day_int)
        this_MJD = this_JDN - 2400000
        if ("MJD" in row):
          this_MJD = int(row["MJD"])
        if (do_trace == 1):
          tracefile.write ("JDN " + str(this_JDN) + ": " +
                           "Year " + str(year_int) + " " +
                           "Month " + str(month_int) + " " +
                           "Day of month " + str(day_int) + " " +
                           "MJD " + str(this_MJD) + " " +
                           "UT1-UTC " + str(row["UT1-UTC"]) +
                           ".\n")
        if (row['UT1-UTC'] != ''):
          ut1_minus_utc = float(row['UT1-UTC'])
          # We must deduce Delta T from UT1-UTC, which requires
          # knowing how many leap seconds have passed.
          leaps_since_jdn = leaps_since (this_JDN)
          new_delta_t = 32.184 - ut1_minus_utc + leaps_since_jdn
          source = "IERS UT1-UTC " + row["type_UT1-UTC"]
          last_delta_T_from_IERS = new_delta_t
          last_delta_T_from_IERS_date = this_JDN
          if (do_trace == 1):
            tracefile.write (" ut1_minus_utc = " + str(ut1_minus_utc) +
                             " leaps since = " + str(leaps_since_jdn) +
                             " source = " + source + ".\n")
          if (this_JDN in delta_t):
            old_delta_t = delta_t[this_JDN]
            difference = new_delta_t - old_delta_t
            if (do_trace == 1):
              tracefile.write (greg(this_JDN, " ", 0) + ": Delta T changes" +
                               " from " + str(old_delta_t) +
                               " by " + str(difference) +
                               " to " + str(new_delta_t) + ".\n")
          else:
            old_delta_t = deltaT(this_JDN)
            difference = new_delta_t - old_delta_t
            if (do_trace == 1):
              tracefile.write (greg(this_JDN, " ", 0) + ": Delta T changes" +
                               " from " + str(old_delta_t) +
                               " (interpolated)" +
                               " by " + str(difference) +
                               " to " + str(new_delta_t) + ".\n")
          delta_t [this_JDN] = new_delta_t
          delta_t_source[this_JDN] = source
          if (source not in delta_t_all):
            delta_t_all[source] = dict()
            source_list = source_list + [source]
          this_delta_t_source = delta_t_all[source]
          this_delta_t_source[this_JDN] = new_delta_t

          # Track the limits of the date
          new_year = float(row['Year'])
          if ((min_year == -1.0) | (min_year > new_year)):
            min_year = new_year
            start_date = this_JDN
          if ((max_year == -1.0) | (max_year < new_year)):
            max_year = new_year
            end_date = this_JDN

  rebuild_interpolations()
  #
  # Tell the trace file the resulting delta T and delta T source information.
  #
  if (do_trace == 1):
    tracefile.write ("After IERS UT1-UTC final and prediction:\n")
    tracefile.write ("delta_t:\n")
    pprint.pprint (delta_t, tracefile)
    tracefile.write ("delta_t_source:\n")
    pprint.pprint (delta_t_source, tracefile)

#
# Create a parabola based on the IERS delta T information and
# future predictions of delta T up until 2500.  Give each prediction
# a weight based on our need for a parabola which connects to the IERS data.
#
if (last_delta_T_from_IERS_date > 0):
  if (verbosity_level > 0):
    print ("last delta T from IERS date: " + str(last_delta_T_from_IERS_date) +
           ".5 = " + greg(last_delta_T_from_IERS_date, " ", 0) + ".")
    print ("last delta T from IERS value: " + str(last_delta_T_from_IERS) + ".")
    
  if (do_trace > 0):
    tracefile.write ("Parabola X point from IERS data: " +
                     str(last_delta_T_from_IERS_date) + " = " +
                     greg(last_delta_T_from_IERS_date, " ", 0) + ".\n")
    tracefile.write ("Parabola Y point from IERS data: " +
                     str(last_delta_T_from_IERS) + ".\n")
  #
  # A parabola can be apporximated from three or more known points.
  # Use the delta T values for the last date for which we have an estimate
  # from the IERS and some additional past and future values.

  x_vals = [
    start_date,
    jdn(1895,1,1),
    last_delta_T_from_IERS_date,
#    jdn(2030,1,1),
#    jdn(2040,1,1),
#    jdn(2050,1,1),
#    jdn(2100,1,1),
#    jdn(2200,1,1),
#    jdn(2300,1,1),
#    jdn(2400,1,1),
    end_date
  ]
  weights = [
    1.0,
    1.0,
    1048576.0,
#    256.0,
#    128.0,
#    64.0,
#    32.0,
#    16.0,
#    8.0,
#    4.0,
    2.0
  ]

  # Rather than use the important points, use them all.
  x_vals=list()
  weights=list()
  for jdn_val in range(start_date, end_date+1):
    x_vals.append(jdn_val)
    weights.append(1.0)
    
  y_vals=list()
  for pos_index in range(len(x_vals)):
    y_vals.append(deltaT(x_vals[pos_index]))
    
  if (do_trace > 0):
    tracefile.write ("Parabola: dates, delta T and weights:\n")
    for pos_index in range(len(x_vals)):
      tracefile.write (" " + greg(x_vals[pos_index], "-", 0) +
                       " is " + str(y_vals[pos_index]) +
                       " weight " + str(weights[pos_index]) + "\n")
    
  # Calculate the unknowns of the equation y=ax^2+bx+c
  p = Polynomial.fit(x_vals, y_vals, 2)
  pnormal = p.convert(domain=(-1, 1))
  a = pnormal.coef[2]
  b = pnormal.coef[1]
  c = pnormal.coef[0]
  
  if (do_trace > 0):
    tracefile.write ("Parabola a,b,c = " + str(a) + ", " +
                     str(b) + ", " +
                     str(c) + ".\n")

  # Calculate the points of the parabola into a dictionary,
  # adding the annual fluctuation.
  y_pos=dict()
  for this_JDN in range (start_date, end_date+1):
    y_pos[this_JDN] = ((a*(this_JDN**2))+(b*this_JDN)+c +
                       UT2_seasonal (this_JDN))
    
  parabola_offset = (last_delta_T_from_IERS -
                     y_pos[last_delta_T_from_IERS_date])
  if (verbosity_level > 0):
    print ("Parabola offset: " + str(parabola_offset) + ".")

  # Compress the parabola so it matches the current value of delta T.
  parabola_max_found = 0
  parabola_min_found = 0
  for this_JDN in range (start_date, end_date+1):
    if (parabola_max_found == 0):
      parabola_max = y_pos[this_JDN]
      parabola_max_found = 1
    if (y_pos[this_JDN] > parabola_max):
      parabola_max = y_pos[this_JDN]
    if (parabola_min_found == 0):
      parabola_min = y_pos[this_JDN]
      parabola_min_found = 1
    if (y_pos[this_JDN] < parabola_min):
      parabola_min = y_pos[this_JDN]
  parabola_height = parabola_max - parabola_min
  parabola_stretch = ((last_delta_T_from_IERS - parabola_height) /
                      (y_pos[last_delta_T_from_IERS_date] - parabola_height))
  if (verbosity_level > 0):
    print ("Parabola max: " + str(parabola_max) + ".")
    print ("Parabola min: " + str(parabola_min) + ".")
    print ("Parabola height: " + str(parabola_height) + ".")
    print ("Parabola at " + str(last_delta_T_from_IERS_date) + ".5: " +
           str(y_pos[last_delta_T_from_IERS_date]) + ".")
    print ("Parabola stretch: " + str(parabola_stretch) + ".")
  
  for this_JDN in range (start_date, end_date+1):
    y_pos[this_JDN] = ((parabola_stretch * (y_pos[this_JDN] - parabola_height))
                        + parabola_height)

  if (do_trace > 0):
    tracefile.write ("Parabola results:\n")
    tracefile.write (" Max: " + str(parabola_max) + ".\n")
    tracefile.write (" Min: " + str(parabola_min) + ".\n")
    tracefile.write (" Meight: " + str(parabola_height) + ".\n")
    tracefile.write (" Offset: " + str(parabola_offset) + ".\n")
    tracefile.write (" Stretch: " + str(parabola_stretch) + ".\n")
    tracefile.write (" Values:\n")
    pprint.pprint (y_pos, tracefile)
    
  # Place the computed values in the delta T dictionary.
  source = "Parabola"
  for this_JDN in y_pos:
    if (source not in delta_t_all):
      delta_t_all[source] = dict()
      source_list = source_list + [source]
    this_delta_t_source = delta_t_all[source]
    this_delta_t_source[this_JDN] = y_pos[this_JDN]

  # Fade from the IERS projections to the astronomical projection.
  # There is code here to use the parabola if it seems necessary.

  source = "IERS UT1-UTC projection"
  projection_delta_t_dict = delta_t_all[source]
  source = "Parabola"
  parabola_delta_t_dict = delta_t_all[source]
  source = "Astronomical Projection"
  astro_delta_t_dict = delta_t_all[source]

  if (do_trace > 0):
    tracefile.write ("Astronomical Projections:\n")
    pprint.pprint (astro_delta_t_dict, tracefile)

  # Subroutine to do a linear interpolation between two points
  # in the astronomical projection.
  def astro_interpolate (the_JDN):
    global astro_delta_t_dict
    if (the_JDN in astro_delta_t_dict):
      return astro_delta_t_dict[the_JDN]
    # Fill in missing values using linear interpolation.
    if (do_trace > 0):
      tracefile.write ("Interpolating: ")
      tracefile.write ("the_JDN " + str(the_JDN) + ".5.\n")
    for probe_JDN in astro_delta_t_dict:
      if (probe_JDN < the_JDN):
        prev_JDN = probe_JDN
      if (probe_JDN > the_JDN):
        next_JDN = probe_JDN
        break
    prev_delta_t = astro_delta_t_dict [prev_JDN]
    next_delta_t = astro_delta_t_dict [next_JDN]
    JDN_range = next_JDN - prev_JDN
    if (do_trace > 0):
      tracefile.write ("prev JDN: " + str(prev_JDN) + ".5 -> " +
                       str(prev_delta_t) + ".\n" +
                       "next JDN: " + str(next_JDN) + ".5 -> " +
                       str(next_delta_t) + ".\n")
    this_delta_t = prev_delta_t + (((the_JDN - prev_JDN) / JDN_range) *
                                        (next_delta_t - prev_delta_t))
    if (do_trace > 0):
      tracefile.write ("the_JDN " + str(the_JDN) + ".5 -> " +
                       str(this_delta_t) + ".\n")
    return (this_delta_t)
      
  fade_time = UT2_base_JDN + IERS_projection_days - last_delta_T_from_IERS_date
  if (verbosity_level > 0):
    print ("On " + greg(last_delta_T_from_IERS_date, "-", 0) +
           " predicted delta T = " +
           format(deltaT(last_delta_T_from_IERS_date), ".7f") + "," +
           " parabola = " +
           format(parabola_delta_t_dict[last_delta_T_from_IERS_date], ".7f") +
           ", astronomical projection = " +
           format(astro_interpolate(last_delta_T_from_IERS_date), ".7f")
           + ".")
    print ("On " + greg(last_delta_T_from_IERS_date + fade_time, "-", 0) +
           " projected delta T = " +
           format(deltaT(last_delta_T_from_IERS_date + fade_time), ".7f") +
           ", parabola = " +
           format(parabola_delta_t_dict[last_delta_T_from_IERS_date +
                                        fade_time], ".7f") +
           ", astronomical projection = " +
           format(astro_interpolate(last_delta_T_from_IERS_date +
                                     fade_time), ".7f") + ".")
    print ("Fade in is from " +
           greg(last_delta_T_from_IERS_date, "-", 0) +
           " to " +
           greg(last_delta_T_from_IERS_date + fade_time, "-", 0) +
           " : " +
           str(fade_time) + " days.")
  for this_JDN in range (last_delta_T_from_IERS_date, end_date+1):
    the_fraction = (this_JDN - last_delta_T_from_IERS_date) / fade_time
    if (the_fraction > 1.0):
      the_fraction = 1.0
    if ((the_fraction < 1.0) and (this_JDN in projection_delta_t_dict)):
      projection_delta_t = projection_delta_t_dict [this_JDN]
      parabola_delta_t = parabola_delta_t_dict [this_JDN]
      astro_delta_t = astro_interpolate(this_JDN)
      new_delta_t = ((the_fraction * astro_delta_t) +
                     ((1.0 - the_fraction) * projection_delta_t))
      if (do_trace > 0):
        tracefile.write ("At " + greg(this_JDN, "-", 0) + ", " +
                         "fade fraction = " + str(the_fraction) + ", " +
                         "projection = " + str(projection_delta_t) + ", " +
                         "parabola = " + str(parabola_delta_t) + ", " +
                         "astro = " + str(astro_delta_t) + ", " +
                         "new delta T = " + str(new_delta_t) + ".\n")
    else:
      new_delta_t = astro_interpolate(this_JDN)
      fraction = 1.0
    if (the_fraction == 1.0):
      source = "Astronomical Projection"
    else:
      source = "IERS UT1-UTC projection + Astronomical projection"
    delta_t [this_JDN] = new_delta_t
    delta_t_source[this_JDN] = source
    if (source not in delta_t_all):
      delta_t_all[source] = dict()
      source_list = source_list + [source]
    this_delta_t_source = delta_t_all[source]
    this_delta_t_source[this_JDN] = new_delta_t
    
  rebuild_interpolations()
  #
  # Tell the trace file the resulting delta T and delta T source information.
  #
  if (do_trace == 1):
    tracefile.write ("After fade:\n")
    tracefile.write ("delta_t:\n")
    pprint.pprint (delta_t, tracefile)
    tracefile.write ("delta_t_source:\n")
    pprint.pprint (delta_t_source, tracefile)
    
min_year_int = int(min_year)
max_year_int = int(max_year + 0.5)

if (do_trace > 0):
  tracefile.flush()
  
if (verbosity_level > 0):
  print ("Start date is " + str(start_date) + ".5 = " +
         greg (start_date, " ", 0))
if (have_latex_start_jdn == 0):
  latex_start_jdn = int(start_date)
if (have_csv_start_jdn == 0):
  csv_start_jdn = int(start_date)
if (have_gnuplot_start_jdn == 0):
  gnuplot_start_jdn = int(start_date)
if (have_c_start_jdn == 0):
  c_start_jdn = int(start_date)
if (have_UT1UTC_start_jdn == 0):
  UT1UTC_start_jdn = int(start_date)
    
if (verbosity_level > 0):
  print ("End date is " + str(end_date) + ".5 = " + greg (end_date, " ", 0))
if (have_latex_end_jdn == 0):
  latex_end_jdn = int(end_date)
if (have_csv_end_jdn == 0):
  csv_end_jdn = int(end_date)
if (have_gnuplot_end_jdn == 0):
  gnuplot_end_jdn = int(end_date)
if (have_c_end_jdn == 0):
  c_end_jdn = int(end_date)
if (have_UT1UTC_end_jdn == 0):
  UT1UTC_end_jdn = int(end_date)

if (verbosity_level > 0):
  print ("Base for calculating DTAI is " + str(DTAI_base_date) +
         ".5 = " + greg(DTAI_base_date, "-", 0) + " with delta T " +
         str(DTAI_base_dt))

#
# Optionally, output the dates for which we have the value of Delta T
# as LaTeX source, suitable for making a table.
#
if ((do_latex_output == 1) & (error_counter == 0)):
  latex_output_file = open (latex_output_file_name, 'wt')
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
    if ((day_no >= latex_start_jdn) and (day_no <= latex_end_jdn)):
      delta_t_val = delta_t [day_no]
      latex_output_file.write (greg (day_no, " ", 1) + " & " +
                               str(round(delta_t_val,4)) + "& " +
                               "\\num{" + str(day_no) + ".5}" +
                               "\\\\\\hline" + "\n")
      
  latex_output_file.write ("\\end{longtable}" + "\n")
  latex_output_file.close()

#
# Optionally, output the dates for which we have a value of delta T
# as a CSV file.  Include all sources and sort by date.
#
delta_t_all_data = dict()
if ((do_csv_output == 1) & (error_counter == 0)):
  csv_output_file = open (csv_output_file_name, 'wt')
  csv_output_file.write ("JDN;Year;Month;Day;date;delta_t;source\n")
  for source in source_list:
    this_delta_t_source = delta_t_all[source]
    for this_JDN in this_delta_t_source:
      delta_t_val = this_delta_t_source [this_JDN]
      if (this_JDN not in delta_t_all_data):
        delta_t_all_data[this_JDN] = list()
      old_list = delta_t_all_data[this_JDN]
      delta_t_all_data[this_JDN] = old_list + [(source, delta_t_val)]
  for this_JDN in range (start_date, end_date+1):
    if (this_JDN in delta_t_all_data):
      data_list = delta_t_all_data[this_JDN]
      for data_item in data_list:
        (source, delta_t_val) = data_item
        (year_no, month_no, mday_no) = ymd_from_JDN (this_JDN)
        if ((this_JDN >= csv_start_jdn) and (this_JDN <= csv_end_jdn)):
          csv_output_file.write (str(this_JDN) + ";" + str(year_no) + ";" +
                                 str(month_no) + ";" + str(mday_no) + ";" +
                                 greg (this_JDN, " ", 2) + ";" +
                                 str(delta_t_val) + ";" + source + "\n")
  csv_output_file.close()

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
          gnuplot_output_file.write (str (gnuplot_start_jdn) + " " +
                                     str (delta_t_val) + "\n")
          first_point_plotted = 1
      gnuplot_output_file.write (str (day_no) + " " +
                                 str (delta_t_val) + "\n")

    gnuplot_output_file.write (str (gnuplot_end_jdn) + " " +
                               str (delta_t_val) + "\n")
    gnuplot_output_file.close()

#
# Convert the values of Delta T into a a series of one-second steps,
# to keep UTC within 0.9 seconds of the rotation of the Earth.
# The result is a dictionary of days with 86,399 or 86,401 seconds.
#
jdn_priority = dict()
last_day = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

# Subroutine to mark a high-priority date for an extraordinary day.
# A date's priority will not be lowered.
def mke (yearno, monthno, dayno, priority):
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
  this_JDN = jdn (yearno, monthno, dayno)
  if (this_JDN not in jdn_priority):
    jdn_priority [this_JDN] = priority
    if (do_trace > 1):
      tracefile.write ("mke: JDN " + str(this_JDN) + " = " +
                       greg (this_JDN, "-", 0) + " = " +
                       str(yearno) + "-" + str(monthno) + "-" +
                       str(dayno) + " has priority " + str(priority) + ".\n")
  return

# Open the output file.
file_name = arguments ['output_file']
outfile = open (file_name, 'wt')

# Return the difference between TAI, which always counts SI seconds,
# and UT1, which measures the rotation of the Earth.
def deltaTAI (this_JDN):
  if (do_trace > 1):
    tracefile.write ("deltaTAI of " + greg(this_JDN, " ", 0) + ".\n")
    tracefile.flush ()
  if (this_JDN < jdn(-2000,1,1)):
      return (deltaTAI (jdn(-2000,1,1)))

  if (this_JDN > jdn(2500,1,1)):
    base_date = jdn(2500,1,1)
    base_deltaTAI = deltaTAI (base_date)
    increment = base_deltaTAI - deltaTAI (base_date - 1)
    numdays = this_JDN - base_date
    return_val = base_deltaTAI + (increment * numdays)
    if (do_trace > 0):
      tracefile.write ("base_date = " + str(base_date) +
                       ", base_deltaTAI = " + str(base_deltaTAI) +
                       ", increment = " + str(increment) +
                       ", numdays = " + str(numdays) +
                       ", return_val = " + str(return_val) + ".\n")
  else:
    return_val = deltaT (this_JDN) - DTAI_base_dt
  if (do_trace > 1):
    tracefile.write ("deltaTAI of " + greg(this_JDN, " ", 0) + " is " +
                     str(return_val) + ".\n")  
  return return_val

#
# For debugging, tell the trace file all the values of deltaTAI.
#
if (do_trace > 1):
  tracefile.write ("All values of deltaTAI:\n")
  for this_JDN in range(jdn(-2000,1,1), jdn(2500,1,5)):
    tracefile.write (" " + greg (this_JDN, " ", 0) + "=" +
                     str(deltaTAI(this_JDN)) + ".\n")

#
# Check for and report big changes in deltaTAI.
#
prev_DTAI = deltaTAI(jdn(-2000,1,1))
max_change_dict = dict()

for this_JDN in range(jdn(-2000,1,1), jdn(2500,1,5)):
  this_DTAI = deltaTAI(this_JDN)
  this_change = abs(this_DTAI - prev_DTAI)
  max_change_dict[this_change] = this_JDN
  prev_DTAI = this_DTAI
  
line_count = 0
for this_change in sorted(max_change_dict, reverse=True):
  if (line_count < 5):
    this_JDN = max_change_dict[this_change]
    max_change_signed = deltaTAI(this_JDN) - deltaTAI(this_JDN-1)
    print ("Max " + str(line_count) + " day-to-day change in DTAI is " +
       format(max_change_signed, ".12f") +
       " at " + greg(this_JDN, "-", 0) + ".")
    line_count = line_count + 1
    
if (do_trace == 1):
  pprint.pprint (max_change_dict, tracefile)
  
#
# As we go through the timeline, there will be some choice as to
# when we schedule an extraordinary day.  We use a priority system,
# as follows:
#
# priority 1 days are those designated by the IERS, starting in 1972.
# priority 2 days are those chosen by Tony Finch, from 1958 through 1971.
# priority 3 days are December 31 and June 30 of any year, except
#  those days with higher priority.
# priority 4 days are March 31 and September 30 of any year.
# priority 5 days are the last day of any month, except those days
#  with higher priority.
# priority 6 days are the 15th of any month.
# priority 7 days are all days without a higher priority.
#

# We record the priority 1-6 days in a dictionary; any day not in
# the dictionary is a priority 7.

#
# Priority 1 from the IERS,
# last updated July 7, 2016, to include December 31, 2016.
#
mke(1972,6,30,1)
mke(1972,12,31,1)
mke(1973,12,31,1)
mke(1974,12,31,1)
mke(1975,12,31,1)
mke(1976,12,31,1)
mke(1977,12,31,1)
mke(1978,12,31,1)
mke(1979,12,31,1)
mke(1981,6,30,1)
mke(1982,6,30,1)
mke(1983,6,30,1)
mke(1985,6,30,1)
mke(1987,12,31,1)
mke(1989,12,31,1)
mke(1990,12,31,1)
mke(1992,6,30,1)
mke(1993,6,30,1)
mke(1994,6,30,1)
mke(1995,12,31,1)
mke(1997,6,30,1)
mke(1998,12,31,1)
mke(2005,12,31,1)
mke(2008,12,31,1)
mke(2012,6,30,1)
mke(2015,6,30,1)
mke(2016,12,31,1)

#
# Priority 2 from Tony Finch
# DTAI was 0 on January 1, 1958, by definition,
# and 10 on January 1, 1972, so there were 10
# leap seconds between those dates.
#
mke(1959,6,30,2)

mke(1961,6,30,2)
mke(1963,6,30,2)
mke(1964,12,31,2)
mke(1966,6,30,2)
mke(1967,6,30,2)
mke(1968,6,30,2)
mke(1969,6,30,2)

mke(1970,6,30,2)
mke(1971,6,30,2)

#
# Priority 3: the last day of June and December in any year:
#
for yearno in range (min_year_int, max_year_int+1):
  mke (yearno, 6, -1, 3)
  mke (yearno, 12, -1, 3)

#
# Priority 4: the last day of March and September in any year:
#
for yearno in range (min_year_int, max_year_int+1):
  mke (yearno, 3, -1, 4)
  mke (yearno, 9, -1, 4)

#
# Priority 5: the last day of all other months:
#
for yearno in range (min_year_int, max_year_int+1):
  for monthno in range (1, 13):
    mke (yearno, monthno, -1, 5)

#
# Priority 6: the 15th of any month:
#
for yearno in range (min_year_int, max_year_int+1):
  for monthno in range (1, 13):
    mke (yearno, monthno, 15, 6)

if (do_trace == 1):
  tracefile.flush()
#
# Subroutine to determine if the current difference between UTC
# and UT1 is within a specified interval.
# Sign == -1 means the interval is below 0, and so the comparisons
# are reversed.
def in_interval (val, base_val, low_limit, high_limit, sign):
  if ((base_val - val) > 1):
    print ("in_interval: " + str(val) + " " + str(base_val))
    if (do_trace == 1):
      tracefile.write ("in_interval high: val " + str(val) +
                       " base_val " + str(base_val) +
                       " low_limit " + str(low_limit) +
                       " high_limit " + str(high_limit) +
                       " sign " + str(sign) + ".\n")
  if ((base_val - val) < -1):
    print ("in_interval: " + str(val) + " " + str(base_val))
    if (do_trace == 1):
      tracefile.write ("in_interval low: val " + str(val) +
                       " base_val " + str(base_val) +
                       " low_limit " + str(low_limit) +
                       " high_limit " + str(high_limit) +
                       " sign " + str(sign) + ".\n")
  if (sign == 1):
    if (val < base_val + low_limit):
      return False
    if (val > base_val + high_limit):
      return False
    return True
  if (sign == -1):
    if (val > base_val - low_limit):
      return False
    if (val < base_val - high_limit):
      return False
    return True
  return False

#
# Subroutine to choose the better day for a leap second.
# Both days have the same priority.
#
def choose_jdn (date1_jdn, date2_jdn, base_jdn, sign):
  # Choose the date whose deltaTAI is closer to half a second from the base.
  base_dt = deltaTAI (base_jdn)
  date1_dt = deltaTAI (date1_jdn)
  date2_dt = deltaTAI (date2_jdn)
  if (sign == 1):
    date1_diff = date1_dt - base_dt
    date2_diff = date2_dt - base_dt
  if (sign == -1):
    date1_diff = base_dt - date1_dt
    date2_diff = base_dt - date2_dt
  if (date1_diff > 0.5):
    date1_diff = 1.0 - date1_diff
  if (date2_diff > 0.5):
    date2_diff = 1.0 - date2_diff
  if (date1_diff > date2_diff):
    return (date1_jdn)
  return (date2_jdn)

#
# Run through the timeline, adjusting leap by +1 or -1 to keep UTC
# within 0.9 seconds of UT1.
#
leap = deltaTAI (start_date)
print ("Initial value of leap is " + str(leap) + ".")
jdn_edays = dict ()

#
# Subroutine to scan an interval of time, inserting a leap second
# if necessary.  The return value is the start of the next interval
# to scan.
#
def scan_interval (base_jdn, limit_jdn):
  global leap
  base_dt = deltaTAI (base_jdn)
  if (do_trace > 1):
    tracefile.write (" scan_interval: " + greg(base_jdn, " ", 0) +
                     " (" + str(deltaTAI(base_jdn)) + ").\n")
  current_jdn = base_jdn
  # If UT1 differs from UTC by less than 0.1 seconds, look ahead
  # to a time when it doesn't.  We can't issue a leap second when
  # UT1 is already within 0.1 seconds of UTC.
  if (abs(leap - deltaTAI(current_jdn)) <= 0.1):
    # Look ahead to when UT1 differs from UTC by at least 0.1 seconds.
    while ((abs(leap - deltaTAI(current_jdn)) <= 0.1) and
           (current_jdn <= limit_jdn)):
      current_jdn = current_jdn + 1
    if (do_trace > 1):
      tracefile.write (" no leap possible from " + greg(base_jdn, " ", 0) +
                       " (" + str(deltaTAI(base_jdn)) + ")" +
                       " to " + greg(current_jdn-1, " ", 0) +
                       " (" + str(deltaTAI(current_jdn-1)) + ").\n")
    return current_jdn
  # We are at the beginning of an interval which might need a leap second.
  anchor_jdn = current_jdn
  anchor_dt = deltaTAI (anchor_jdn)
  sign = 0
  if ((anchor_dt - leap) < 0):
    sign = -1
  if ((anchor_dt - leap) > 0):
    sign = 1
  # Now look ahead to when UT1 differs from UTC by 0.9 seconds
  # in the same direction.  If the difference declines to 0.1,
  # stop looking.
  while (in_interval (deltaTAI (current_jdn), leap, 0.1, 0.9, sign) &
         (current_jdn <= limit_jdn)):
    current_jdn = current_jdn + 1
  if (current_jdn >= limit_jdn):
    return current_jdn
  # If the difference between UTC and UT1 has decreased to below 0.1
  # seconds, this interval does not need a leap second.
  if (abs(leap - deltaTAI (current_jdn)) <= 0.1):
    if (do_trace > 1):
      tracefile.write (" no leap needed from " + greg(base_jdn, " ", 0) +
                       " (" + str(deltaTAI(base_jdn)) + ")" +
                       " to " + greg(current_jdn, " ", 0) +
                       " (" + str(deltaTAI(current_jdn)) + ").\n")
    return (current_jdn)
  # Otherwise we have reached a time when the difference between
  # UTC and UT1 has reached 0.9 seconds, and has not decreased below
  # 0.1 seconds since anchor_jdn.  We must issue a leap second.
  # Find the best time to do that.
  future_jdn = current_jdn
  best_jdn = anchor_jdn
  best_priority = jdn_priority.get(best_jdn, 7)
  for current_jdn in range (anchor_jdn, future_jdn):
    current_priority = jdn_priority.get(current_jdn, 7)
    if (current_priority == best_priority):
      best_jdn = choose_jdn (best_jdn, current_jdn, anchor_jdn, sign)
    if (current_priority < best_priority):
      best_jdn = current_jdn
      best_priority = current_priority
  # The best date in the interval becomes an extraordinary day
  jdn_edays[best_jdn] = 86400 + sign
  if (do_trace > 1):
    tracefile.write (" leap " + str(sign) + " (" +
                     str(leap+sign) + ") at " +
                     greg(best_jdn, " ", 0) +
                     " (" + str(deltaTAI(best_jdn)) + ")" +
                     " priority " + str(best_priority) +
                     " from " + greg(base_jdn, " ", 0) +
                     " (" + str(deltaTAI(base_jdn)) + ")" +
                     " to " + greg (future_jdn, " ", 0) +
                     " (" + str(deltaTAI(future_jdn)) + ")" +
                     ".\n")
  leap = leap + sign
  # Continue scanning from the next day
  return (best_jdn + 1)

#
# Scan through the timeline, generating leap seconds as needed.
#
scan_jdn = start_date
while (scan_jdn < end_date):
  scan_jdn = scan_interval (scan_jdn, end_date)

#
# If requested, replace the extraordinary days from January 1, 1958
# to December 28, 2017 with those from Tony Finch and the IERS.
# They all have 86,401 seconds.
#
if (do_Tony_Finch_leaps):
  if (do_trace == 1):
    tracefile.write ("Tony Finch leaps:\n")
  for clear_jdn in range (jdn(1958,1,1), jdn(1971,12,31)):
    if clear_jdn in jdn_edays:
      if (do_trace == 1):
        tracefile.write (" delete leap at " + greg(clear_jdn, " ", 0) +
                         ".\n")
      del jdn_edays [clear_jdn]

  for fill_jdn in range (jdn(1958,1,1), jdn(1971,12,31)):
    if fill_jdn in jdn_priority:
      if (jdn_priority [fill_jdn] < 3):
        if (do_trace == 1):
          tracefile.write (" add leap at " + greg(fill_jdn, " ", 0) +
                         ".\n")
        jdn_edays [fill_jdn] = 86401

#
# If requested, replace the extraordinary days from January 1, 1973
# to the present with the official days from the IERS.
#
if (do_IERS_leaps):
  if (do_trace == 1):
    tracefile.write ("IERS leaps:\n")
  for clear_jdn in range (jdn(1972,1,1), jdn(2019,12,31)):
    if clear_jdn in jdn_edays:
      if (do_trace == 1):
        tracefile.write (" delete leap at " + greg(clear_jdn, " ", 0) +
                         ".\n")
      del jdn_edays [clear_jdn]

  for fill_jdn in range (jdn(1972,1,1), jdn(2019,12,31)):
    if fill_jdn in jdn_priority:
      if (jdn_priority [fill_jdn] < 3):
        if (do_trace == 1):
          tracefile.write (" add leap at " + greg(fill_jdn, " ", 0) +
                         ".\n")
        jdn_edays [fill_jdn] = 86401
  
#
# Show the resulting list of extraordinary days to the trace file.
#
if (do_trace == 1):
  tracefile.write ("Extraordinary days:\n")
  pprint.pprint (jdn_edays, tracefile)
  
# Compute DTAI, based on DTAI = 0 on January 1, 1958, at UTC 00:00.
dtai_dict = {}

dtai0_jdn_tuple = gcal2jd (1957,12,31)
dtai0_jdn = int(dtai0_jdn_tuple [0] + dtai0_jdn_tuple [1] + 0.5)
oldest_jdn = dtai0_jdn
if (do_trace == 1):
  tracefile.write ("Computing extraordinary days, dtai0_jdn = " +
                   str(dtai0_jdn) + " = " + greg(dtai0_jdn, "-", 0) + ".\n")
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
  outfile.write (str(jdn) + "\t" + str(lod) + "\t" + str(dtai) + "\t" +
                 "# " + greg (jdn, " ", 0) + "\n")

outfile.close()

# Optionally, write a table of UT1-UTC.
if (do_UT1UTC_output):
  base_deltaT = deltaT (dtai0_jdn)
  if (do_trace == 1):
    tracefile.write ("Producing UT1-UTC, base_deltaT = " +
                     str(base_deltaT) + ".\n")
    pprint.pprint (delta_t_source, tracefile)
    
  leap = base_deltaT
  UT1UTC_dict = dict()
  prevous_source = "unknown"
  
  # Walk futureward from January 1, 1958, when UT1-UTC was 0.
  for this_JDN in range (dtai0_jdn, end_date):
    this_deltaT = deltaT (this_JDN)
    UT1UTC = leap - this_deltaT
    lod = 86400
    if (this_JDN in jdn_edays):
      lod = jdn_edays[this_JDN]
    leap = leap + lod - 86400
    ymdf = jd2gcal (float(this_JDN), 0.5)
    year_no = ymdf [0]
    month_no = ymdf [1]
    mday_no = ymdf [2]
    if (this_JDN in delta_t_source):
      source = delta_t_source [this_JDN]
    else:
      source = previous_source
    UT1UTC_dict [this_JDN] = (year_no, month_no, mday_no, source, leap, UT1UTC)
    if (do_trace == 1):
      tracefile.write (" JDN " + str(this_JDN) + " " +
                       " Year " + str(year_no) + " " +
                       "Month " + str(month_no) + " " +
                       "Day of month " + str(mday_no) + " " +
                       "deltaT " + str(this_deltaT) + " " +
                       "leap " + str(leap) + " " +
                       "UT1-UTC " + str(UT1UTC) +
                       " source " + source + ".\n")
    previous_source = source
      
  # Walk pastward from January 1, 1958.
  leap = base_deltaT
  previous_source = "unknown"
  for this_JDN in range(dtai0_jdn, start_date, -1):
    this_deltaT = deltaT (this_JDN)
    UT1UTC = leap - this_deltaT
    lod = 86400
    if (this_JDN in jdn_edays):
      lod = jdn_edays[this_JDN]
    leap = leap - lod + 86400
    ymdf = jd2gcal (float(this_JDN), 0.5)
    year_no = ymdf [0]
    month_no = ymdf [1]
    mday_no = ymdf [2]
    if (this_JDN in delta_t_source):
      source = delta_t_source [this_JDN]
    else:
      source = previous_source
    UT1UTC_dict [this_JDN] = (year_no, month_no, mday_no, source, leap, UT1UTC)
    if (do_trace == 1):
      tracefile.write (" JDN " + str(this_JDN) + " " +
                       " Year " + str(year_no) + " " +
                       "Month " + str(month_no) + " " +
                       "Day of month " + str(mday_no) + " " +
                       "deltaT " + str(this_deltaT) + " " +
                       "leap " + str(leap) + " " +
                       "UT1-UTC " + str(UT1UTC) +
                       " source " + source + ".\n")
    previous_source = source

  # Now that the dataa is collected, output it.
  UT1UTCfile = open (UT1UTC_output_file_name, "wt")
  UT1UTCfile.write ("JDN;Year;Month;Day;source;leap;UT1-UTC\n")

  # We wish to produce a CSV file which can be processed by pandas.
  # Limit its range to what can be handled by the pandas Timestamp
  # datatype.
  min_year = pd.Timestamp.min.year
  min_month = pd.Timestamp.min.month
  min_mday = pd.Timestamp.min.day
  min_datetime = datetime.datetime (min_year, min_month, min_mday)
  # the minimum date is the first day after the minimum instant.
  min_datetime = min_datetime + datetime.timedelta (days = 1)
  max_year = pd.Timestamp.max.year
  max_month = pd.Timestamp.max.month
  max_mday = pd.Timestamp.max.day
  max_datetime = datetime.datetime (max_year, max_month, max_mday)

  if (do_trace > 0):
    tracefile.write ("Pandas min date: ")
    pprint.pprint (pd.Timestamp.min, tracefile)
    pprint.pprint (min_datetime, tracefile)
    tracefile.write ("Pandas max date: ")
    pprint.pprint (pd.Timestamp.max, tracefile)
    pprint.pprint (max_datetime, tracefile)
    
  for this_JDN in range (UT1UTC_start_jdn, UT1UTC_end_jdn):
    (year_no, month_no, mday_no, source, leap, UT1UTC) = UT1UTC_dict[this_JDN]
    this_date = datetime.datetime(year_no, month_no, mday_no)
    if ((this_date >= min_datetime) and (this_date <= max_datetime)):
      UT1UTCfile.write (str(this_JDN) + ";" +
                        str(year_no) + ";" +
                        str(month_no) + ";" +
                        str(mday_no) + ";" +
                        str(source) + ";" +
                        str(int(round(leap - base_deltaT))) + ";" +
                        format(UT1UTC, '.7f') + "\n")
  
  UT1UTCfile.close()

if (do_trace > 0):
  tracefile.close()

if (error_counter > 0):
  print ("Encountered " + str(error_counter) + " errors.")
