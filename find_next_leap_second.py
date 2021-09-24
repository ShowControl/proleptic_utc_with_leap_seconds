#!/usr/bin/python3
# -*- coding: utf-8
#
# Find the next leap second in the UT1-UTC.csv file.
#
#   Copyright © 2021 by John Sauter <John_Sauter@systemeyescomputerstore.com>

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

import datetime
import calendar
import pandas as pd

from jdcal import gcal2jd, jd2gcal
import pprint

import argparse

parser = argparse.ArgumentParser (
  formatter_class=argparse.RawDescriptionHelpFormatter,
  description='Find the next leap second.',
  epilog='Copyright © 2021 by John Sauter' + '\n' +
  'License GPL3+: GNU GPL version 3 or later; ' + '\n' +
  'see <http://gnu.org/licenses/gpl.html> for the full text ' +
  'of the license.' + '\n' +
  'This is free software: you are free to change and redistribute it. ' + '\n' +
  'There is NO WARRANTY, to the extent permitted by law. ' + '\n' + '\n' +
  'The input file is the CSV file with UT1-UTC.' + '\n')
parser.add_argument ('input1_file',
                     help='The values of UT1-UTC in CSV format')
parser.add_argument ('--version', action='version', 
                     version='find_next_leap_second 1.0 2021-09-12',
                     help='print the version number and exit')
parser.add_argument ('--trace', metavar='trace_file',
                     help='write trace output to the specified file')
parser.add_argument ('--verbose', type=int, metavar='verbosity_level',
                     help='control the amount of output from the program: ' +
                     '1 is normal, 0 suppresses summary messages')

do_trace = 0
tracefile = ""
verbosity_level = 1
error_counter = 0

# Parse the command line.
arguments = parser.parse_args ()
arguments = vars(arguments)

if (arguments ['trace'] != None):
  do_trace = 1
  trace_file_name = arguments ['trace']
  tracefile = open (trace_file_name, 'wt')

# Subroutine to convert a Julian Day Number to its equivalent Gregorian date.
month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul",
               "Aug", "Sep", "Oct", "Nov", "Dec"] 
def greg (JDN, separator):
  ymdf = jd2gcal (float(JDN), 0.5)
  year_no = ymdf [0]
  month_no = ymdf [1]
  day_no = ymdf [2]
  month_name = month_names [month_no-1]
  return (str(day_no) + separator + month_name + separator + str(year_no))

# Subroutine to convert a Gregorian date to its equivalnet Julian day number.
def Julian (the_year, the_month, the_day):
  float_1, float_2 = gcal2jd (the_year, the_month, the_day)
  Julian_day_number = int(float_1 + float_2 - 0.5)
  return (Julian_day_number)

# Parse a date into a Pandas Timestamp
def dateparse (y, m, d):
  the_Timestamp = pd.Timestamp(year = int(y), month = int(m), day = int(d))
  return the_Timestamp

# Convert a Julian Day Number into a Pandas Timestamp.
def JDN_to_Timestamp (the_JDN):
  ymdf = jd2gcal (float(the_JDN), 0.5)
  year_no = ymdf [0]
  month_no = ymdf [1]
  mday_no = ymdf [2]
  return (dateparse(year_no, month_no, mday_no))

# Read the CSV file into a Pandas dataframe.
input1_file_name = arguments["input1_file"]
data = pd.read_csv (input1_file_name, sep=';')
if (do_trace > 0):
  tracefile.write ("CSV file:\n")
  pprint.pprint (data, tracefile)

# index the dataframe by date.
data['Date'] = data.apply(lambda x:
                          dateparse (x['Year'], x['Month'], x['Day']),
                          axis='columns')
data = data.set_index('Date')
if (do_trace > 0):
  tracefile.write ("after indexing by date:\n")
  pprint.pprint (data, tracefile)

# Make the source column a category.
data["UT1-UTC_source"] = data["source"].astype("category")
data = data.drop("source", axis="columns")

# Find the first and last date in the CSV file.
last_line = data.tail(1)
last_JDN = int(last_line["JDN"].values[0])
first_line = data.head(1)
first_JDN = int(first_line["JDN"].values[0])
if (verbosity_level > 1):
  print ("JDN range of CSV file is " +
         str(first_JDN) + ".5=" + greg(first_JDN, "-") + " to " +
         str(last_JDN) + ".5=" + greg(last_JDN, "-") + ".")

start_JDN = first_JDN
end_JDN = last_JDN

# Display the chart limits.
if (verbosity_level > 1):
  print ("Chart start date is " + greg (start_JDN, "-"))
  print ("Chart end date is " + greg (end_JDN, "-"))

# Remove the data we aren't going to chart.
data_to_chart = data[((data["JDN"] >= start_JDN))]
data_to_chart = data_to_chart[((data_to_chart["JDN"] <= end_JDN))]

if (do_trace > 0):
  tracefile.write ("data to chart from CSV file:\n")
  pprint.pprint (data_to_chart, tracefile)
  tracefile.flush()

# Compute today's date.
today = pd.Timestamp.now(None)
today = today.replace(hour = 0, minute=0, second=0, microsecond=0)

# Find the row corresponding to today's date in the dataframe.
today_row = data.loc[today]
if (do_trace > 0):
  tracefile.write ("Today:\n")
  pprint.pprint (today_row, tracefile)

# We will sequence through the dataframe one day at a time.
one_day = datetime.timedelta(days=1)

# Find the next leap second.
today_leap = today_row.leap
this_date = today
while (today_leap == data.loc[this_date].leap):
  this_date = this_date + one_day
this_date = this_date - one_day

next_leap_year = int(data.loc[this_date].Year)
next_leap_month = int(data.loc[this_date].Month)
next_leap_mday = int(data.loc[this_date].Day)
next_leap_date = pd.Timestamp(year = next_leap_year,
                               month = next_leap_month,
                               day = next_leap_mday)
next_leap_UT1UTC = data.loc[this_date]["UT1-UTC"]
if (verbosity_level > 1):
  print ("UT1-UTC at next leap is " + format (next_leap_UT1UTC, ".3f") + ".")
next_leap_value = data.loc[this_date + one_day].leap
if (do_trace > 0):
  tracefile.write ("next leap value: " + str(next_leap_value) + ".\n")
  tracefile.write ("today leap: " + str(today_leap) + ".\n")
if (next_leap_value > today_leap):
  next_leap_direction = "positive"
if (next_leap_value < today_leap):
  next_leap_direction = "negative"

if (verbosity_level > 0):
  print ("The next leap second will be a " + next_leap_direction +
         " leap second on " + next_leap_date.strftime ("%B %d, %Y") + ".")

if (do_trace == 1):
  tracefile.close()

if (error_counter > 0):
  print ("Encountered " + str(error_counter) + " errors.")
