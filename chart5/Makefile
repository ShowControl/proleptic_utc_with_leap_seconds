# File: Makefile, author: John Sauter, date: October 28, 2023.
# Chart Delta T.

#   Copyright © 2023 by John Sauter <John_Sauter@systemeyescomputerstore.com>

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

all: deltaT.png 
.PHONEY: all

deltaT.png : chart_deltaT.py ../delta_T.csv
	python3 chart_deltaT.py ../delta_T.csv \
--output-file deltaT.png --start-JDN=2458119 --end-JDN=2462520

# As is customary, "make clean" deletes all files except those needed
# to create the target.
.PHONEY: clean
clean:
	rm -f deltaT.png

# End of file Makefile
