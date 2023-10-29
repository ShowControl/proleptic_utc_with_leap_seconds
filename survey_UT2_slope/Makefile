# File: Makefile, author: John Sauter, date: June 25, 2021.
# Chart the slope of UT2-UTC as predicted by the IERS
# and the history of DUT1

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

all: UT2_slope.pdf DUT1.pdf
.PHONEY: all

.PHONEY: download
download : download.sh
	rm -rf Bulletin_A
	mkdir -p Bulletin_A
	rm -rf Bulletin_D
	mkdir -p Bulletin_D
	touch download_time.txt
	bash download.sh
	rm -f latest_date_A.txt
	rm -f latest_date_D.txt
	rm -f UT2_slope_parsed.txt
	rm -f DUT1_parsed.txt
	rm -f UT2_slope.csv
	rm -f DUT1.pdf
	rm -f UT2_slope.pdf

download_time.txt : download.sh
	mkdir -p Bulletin_A
	mkdir -p Bulletin_D
	touch download_time.txt
	bash download.sh
	rm -f latest_date_A.txt
	rm -f latest_date_D.txt
	rm -f UT2_slope.csv
	rm -f DUT1.pdf
	rm -f UT2_slope.pdf

download.sh : build_download_script.py
	python3 build_download_script.py --output download.sh

UT2_slope.csv : 
	python3 parse_bulletin_A.py Bulletin_A/ --csv-output UT2_slope.csv \
--verbose 0 --latest-date-output latest_date_A.txt
	touch UT2_slope_parsed.txt

DUT1.csv : 
	python3 parse_bulletin_D.py Bulletin_D/ --csv-output DUT1.csv \
--verbose 0 --latest-date-output latest_date_D.txt
	touch DUT1_parsed.txt

plot_UT2_slope.gnuplot : plot_UT2_slope.gnuplot.in UT2_slope.csv
	bash edit_UT2_slope_gnuplot_file.sh

UT2_slope.pdf : UT2_slope.csv plot_UT2_slope.gnuplot
	gnuplot plot_UT2_slope.gnuplot

plot_DUT1.gnuplot : plot_DUT1.gnuplot.in DUT1.csv
	bash edit_DUT1_gnuplot_file.sh

DUT1.pdf : DUT1.csv plot_DUT1.gnuplot
	gnuplot plot_DUT1.gnuplot

# As is customary, "make clean" deletes all intermediate files.
.PHONEY: clean
clean:
	rm -f download.sh
	rm -f UT2_slope.csv
	rm -f DUT1.csv
	rm -f latest_date_A.txt
	rm -f latest_date_D.txt
	rm -f download_time.txt
	rm -f UT2_slope_parsed.txt
	rm -f DUT1_parsed.txt
	rm -f plot_UT2_slope.gnuplot
	rm -f plot_DUT1.gnuplot
	rm -rf Bulletin_A
	rm -rf Bulletin_D
	rm -f trace*.txt
	rm -f *~

# End of file Makefile
