# File: edit_UT2_slope_gnuplot_file.sh, author: John Sauter,
#  date: January 9, 2021.
# Edit the date of the last IERS Bulletin A into the chart.

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

latest_date=$(cat latest_date_A.txt)
sed -e "s/[@]latest_date[@]/${latest_date}/" \
plot_UT2_slope.gnuplot.in > plot_UT2_slope.gnuplot

# End of file edit_UT2_slope_gnuplot_file.sh
