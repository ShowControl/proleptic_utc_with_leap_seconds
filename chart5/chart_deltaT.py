#!/usr/bin/python3
# -*- coding: utf-8
#
# chart_deltaT plots Delta T.
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


import pandas as pd
from jdcal import gcal2jd, jd2gcal
import matplotlib.colors as colors
colors_list = list(colors._colors_full_map.values())

import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
plt.ioff()

import seaborn as sns
# Use seaborn style defaults and set the default figure size
sns.set_style('whitegrid')
sns.set(rc={'figure.figsize':(12, 12)})

import argparse

parser = argparse.ArgumentParser (
  formatter_class=argparse.RawDescriptionHelpFormatter,
  description='Chart the values of Delta T over time',
  epilog='Copyright © 2020 by John Sauter' + '\n' +
  'License GPL3+: GNU GPL version 3 or later; ' + '\n' +
  'see <http://gnu.org/licenses/gpl.html> for the full text ' +
  'of the license.' + '\n' +
  'This is free software: you are free to change and redistribute it. ' + '\n' +
  'There is NO WARRANTY, to the extent permitted by law. ' + '\n' + '\n'
  'The input file has values for Delta T at various times; ' +
  'the output is a LaTeX table. ' + '\n')
parser.add_argument ('input1_file',
                     help='The values of Delta T in CSV format')
parser.add_argument ('--output-file', metavar='output_file',
                     help='A picture of Delta T over time')
parser.add_argument ('--version', action='version', 
                     version='chart_delta_T 2.0 2020-06-05',
                     help='print the version number and exit')
parser.add_argument ('--trace', metavar='trace_file',
                     help='write trace output to the specified file')
parser.add_argument ('--start-JDN', metavar='start_JDN',
                     help='earliest date to put in chart')
parser.add_argument ('--end-JDN', metavar='end_JDN',
                     help='latest date to put in chart')
parser.add_argument ('--verbose', type=int, metavar='verbosity level',
                     help='control the amount of output from the program: ' +
                     '1 is normal, 0 suppresses summary messages')

do_trace = 0
tracefile = ""
do_output = 0
output_file_name = ""
have_start_JDN = 0
start_JDN = 0
have_end_JDN = 0
end_JDN = 0
verbosity_level = 1
error_counter = 0

# Parse the command line.
arguments = parser.parse_args ()
arguments = vars(arguments)

if (arguments['output_file'] != None):
  do_output = 1
  output_file_name = arguments ['output_file']
  
if (arguments ['trace'] != None):
  do_trace = 1
  trace_file_name = arguments ['trace']
  tracefile = open (trace_file_name, 'wt')

if (arguments ['start_JDN'] != None):
  have_start_JDN = 1
  start_JDN = int(arguments ['start_JDN'])

if (arguments ['end_JDN'] != None):
  have_end_JDN = 1
  end_JDN = int(arguments ['end_JDN'])

# Subroutine to convert a Julian Day Number to its equivalent Gregorian date.
month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul",
               "Aug", "Sep", "Oct", "Nov", "Dec"] 
def greg (JDN, separator):
  ymdf = jd2gcal (float(JDN), 0.5)
  year_no = ymdf [0]
  month_no = ymdf [1]
  mday_no = ymdf [2]
  month_name = month_names [month_no-1]
  return (str(mday_no) + separator + month_name + separator + str(year_no))

def just_year (JDN):
  ymdf = jd2gcal (float(JDN), 0.5)
  year_no = ymdf [0]
  month_no = ymdf [1]
  day_no = ymdf [2]
  return (str(year_no))

def month_and_year (JDN, separator):
  ymdf = jd2gcal (float(JDN), 0.5)
  year_no = ymdf [0]
  month_no = ymdf [1]
  day_no = ymdf [2]
  month_name = month_names [month_no-1]
  return (month_name + separator + str(year_no))

def day_month_and_year (JDN, separator):
  ymdf = jd2gcal (float(JDN), 0.5)
  year_no = ymdf [0]
  month_no = ymdf [1]
  day_no = ymdf [2]
  month_name = month_names [month_no-1]
  return (str(day_no) + separator + month_name + separator + str(year_no))

input_file_name = arguments["input1_file"]
data = pd.read_csv(input_file_name, sep=';',
                   converters={"JDN": int, "Year": int, "Month": int,
                               "Day": int})
data.set_index(["JDN"], inplace=True)

last_JDN = data.index[-1]
first_JDN = data.index[0]
print ("JDN range is " + str(first_JDN) + ".5 to " + str(last_JDN) + ".5.")

if (have_start_JDN == 0):
  start_JDN = first_JDN
if (have_end_JDN == 0):
  end_JDN = last_JDN

print ("Range limited to " + str(start_JDN) + ".5 and " + str(end_JDN) + ".5.")
bottom_deltaT = 69
top_deltaT = 70
print ("Domain is " + str(bottom_deltaT) + " to " + str(top_deltaT) + ".")

# X-axis formatter to translate JDN into Gregorian dates.
def format_func(value, tick_number):
  full_date = greg(value, "-")
  return (day_month_and_year(value, " "))

# Make the source column a category.
data["Delta_T_source"] = data["source"].astype("category")

colors_list = ["Black", "Green", "Yellow", "Orange", "Red",
               "Blue"] + colors_list

# Plot all categories.
fig, ax = plt.subplots(1, 1)
ax.set_title("Delta T")
lineno = 0
for source_name, source_data in \
    data["delta_t"].groupby(data["Delta_T_source"]):
  ax.plot(source_data,
          color=colors_list[lineno], linewidth=1.0,
          label=source_name)
  lineno = lineno + 1

ax.set_xlim(left=start_JDN,right=end_JDN)
ax.set_xlabel("Date")
ax.xaxis.set_major_formatter(plt.FuncFormatter(format_func))
ax.set_ylim(bottom=bottom_deltaT,top=top_deltaT)
ax.set_ylabel("Seconds")
#ax.yaxis.set_ticks(np.arange(-1.0, 1.1, 0.1))
ax.legend(loc="best", bbox_to_anchor=(0.5, 0.0, 0.5, 0.5), framealpha=0.5)

if (do_output != 0):
  plt.savefig(output_file_name, dpi=120, format="png", bbox_inches="tight")
plt.show()

if (do_trace == 1):
  tracefile.close()

if (error_counter > 0):
  print ("Encountered " + str(error_counter) + " errors.")

