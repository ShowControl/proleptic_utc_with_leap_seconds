#!/usr/bin/python3
# -*- coding: utf-8
#
# build_download_script creates a bash script to download IERS Bulletins
# A and D.
#
#   Copyright © 2022 by John Sauter <John_Sauter@systemeyescomputerstore.com>

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

import argparse

parser = argparse.ArgumentParser (
  formatter_class=argparse.RawDescriptionHelpFormatter,
  description='Create a bash script to download IERS Bulletin A',
  epilog='Copyright © 2022 by John Sauter' + '\n' +
  'License GPL3+: GNU GPL version 3 or later; ' + '\n' +
  'see <http://gnu.org/licenses/gpl.html> for the full text ' +
  'of the license.' + '\n' +
  'This is free software: you are free to change and redistribute it. ' + '\n' +
  'There is NO WARRANTY, to the extent permitted by law. ' + '\n' + '\n'
  '\n')
parser.add_argument ('--output-file', metavar='output_file',
                     help='created bash script')
parser.add_argument ('--version', action='version', 
                     version='build_download_script 3.0 2022-11-04',
                     help='print the version number and exit')
parser.add_argument ('--trace', metavar='trace_file',
                     help='write trace output to the specified file')
parser.add_argument ('--verbose', type=int, metavar='verbosity level',
                     help='control the amount of output from the program: ' +
                     '1 is normal, 0 suppresses summary messages')

do_trace = 0
tracefile = ""
do_output = 0
output_file_name = ""
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

if (do_output == 1):
  outputfile = open (output_file_name, 'wt')
  outputfile.write ('#!/bin/bash\n')
  outputfile.write ('pushd Bulletin_A\n')

  # The IERS stores historical issues of Bulletin A on their web site,
  # with URLs containing the volume number in roman numerals.
  # Some years have 53 weeks.
  
  for yearcode in ('xviii', 'xix', 'xx', 'xxi', 'xxii', 'xxiii', 'xxiv',
                   'xxv', 'xxvi', 'xxvii', 'xxviii', 'xxix', 'xxx',
                   'xxxi', 'xxxii', 'xxxiii', 'xxxiv', 'xxxv', 'xxxvi',
                   'xxxvii', 'xxxviii', 'xxxix', 'xl'):
    for weekcode in range (1, 54):
      outputfile.write ('wget --timestamping ' +
                        'https://datacenter.iers.org/data/6/bulletina-' +
                        yearcode + '-' + str(weekcode).zfill(3) + '.txt\n')
      outputfile.write ('echo "got ' + str(yearcode) + " " +
                        str(weekcode) + '"\n')
  outputfile.write ('popd\n')

  outputfile.write ('pushd Bulletin_D\n')

  # Bulletin D is simply numbered.
  for bulletin_number in range (1,200):
    outputfile.write ('wget --timestamping ' +
                      'https://datacenter.iers.org/data/17/bulletind-' +
                      str(bulletin_number).zfill(3) + '.txt\n')
    outputfile.write ('echo "got ' + str(bulletin_number)+ '"\n')
  outputfile.write ('popd\n')
                      
  outputfile.close()
  
if (do_trace == 1):
  tracefile.close()

if (error_counter > 0):
  print ("Encountered " + str(error_counter) + " errors.")

