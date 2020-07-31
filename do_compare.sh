# File: do_compares.sh, author: John Sauter, date: July 25, 2020.
#
# Compare the old version of exdays_05.dat and UT1UTC.csv with the new ones.

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

diff -q exdays_05_previous.dat exdays_05.dat
if [ $? -ne 0 ]; then
    cp -p exdays_05_previous.dat different/exdays_05.dat
fi

diff -q UT1UTC_previous.csv UT1UTC.csv
if [ $? -ne 0 ]; then
    cp -p UT1UTC_previous.csv different/UT1UTC.csv
fi

# End of file do_compare.sh

