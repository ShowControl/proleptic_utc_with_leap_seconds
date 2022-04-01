# File: Makefile.am, author: John Sauter, date: April 1, 2022.
#
# Build proleptic_UTC.pdf and extraordinary_days.dat

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

# The main target is the file extraordinary_days.dat
all: extraordinary_days.dat 
.PHONEY: all

# Distribute the main file.
txtdir = ${datadir}/proleptic_utc_with_leap_seconds/data/
dist_txt_DATA = extraordinary_days.dat

# Also distribute a man file.
dist_man_MANS = extraordinary_days.dat.5

# Include the following documentation files in the distribution.
dist_doc_DATA = \
	README \
	COPYING \
	LICENSE \
	AUTHORS \
	ChangeLog \
	INSTALL \
	NEWS

# Conditionally build the PDF.
# Doing this will require texlive-scheme-full and gnuplot.
if ENABLE_PDF
  dist_doc_DATA += proleptic_UTC.pdf
endif

EXTRA_DIST = \
build_xtic_labels.py build_xtic_monthly_labels.py \
parse_bulletin_A.py parse_bulletin_C.py read_delta_t.py \
read_extraordinary_days_table.py reformat_delta_t.py \
find_next_leap_second.py \
proleptic_UTC.tex.in fix_files.sh autogen.sh

EXTRA_DIST += \
references.bib exdays_01.dat exdays_04.dat finals.all \
ser7.dat bulletinc.dat \
values_of_delta_T.csv USNO_delta_T.csv plot_extraordinary_days.gnuplot \
plot_extraordinary_days_since_1500.gnuplot \
plot_extraordinary_days_since_1600.gnuplot \
plot_extraordinary_days_since_1700.gnuplot \
plot_extraordinary_days_since_1800.gnuplot \
plot_extraordinary_days_since_1900.gnuplot \
plot_extraordinary_days_since_1950.gnuplot \
plot_extraordinary_days_since_2000.gnuplot \
plot_extraordinary_days_since_2015.gnuplot \
plot_extraordinary_days_since_2400.gnuplot \
plot_extraordinary_days_since_2490.gnuplot

EXTRA_DIST += 20160404.full.pdf \
R-REC-TF.460-6-200202-I!!PDF-E.pdf \
legalcode.txt values_of_delta_T.ods\
USNO_deltat_preds.csv gpl.txt John_Sauter_public_key.asc

# Distribute the shell script which builds the RPMs.
EXTRA_DIST += build_RPMs.sh

# Run it if the developer types "make RPMs".
.phoney: RPMs
RPMs:
	bash build_RPMs.sh

# The spec file is ueed to build RPMs for RPM-based distributions
# of GNU/Linux, including RHEL, CENTOS and Fedora.
EXTRA_DIST += proleptic_utc_with_leap_seconds.spec

# Run luaLaTeX four times to get the forward references and
# pdf bytecount right.
proleptic_UTC.pdf : proleptic_UTC.tex proleptic_UTC.tex.in \
proleptic_UTC.bbl \
delta_t.tex extraordinary_days.tex values_of_DTAI.tex \
values_of_DTAI_since_1500.tex values_of_DTAI_since_1600.tex \
values_of_DTAI_since_1700.tex values_of_DTAI_since_1800.tex \
values_of_DTAI_since_1900.tex values_of_DTAI_since_1950.tex \
values_of_DTAI_since_2000.tex exdays_01.dat exdays_04.dat \
finals.all 
	lualatex ${builddir}/proleptic_UTC.tex
	lualatex ${builddir}/proleptic_UTC.tex
	lualatex ${builddir}/proleptic_UTC.tex
	lualatex ${builddir}/proleptic_UTC.tex

# To create the .bbl file, we must run luaLaTeX against the
# .tex file and process its .aux file output.  Create a fake
# copy of the .bbl file for the .tex file to embed, in case
# it doesn't exist.  Embedding doesn't change the page numbers,
# so doing that won't hurt the .aux file.
proleptic_UTC.bbl : proleptic_UTC.tex proleptic_UTC.tex.in \
references.bib \
delta_t.tex extraordinary_days.tex values_of_DTAI.tex \
values_of_DTAI_since_1500.tex values_of_DTAI_since_1600.tex \
values_of_DTAI_since_1700.tex values_of_DTAI_since_1800.tex \
values_of_DTAI_since_1900.tex values_of_DTAI_since_1950.tex \
values_of_DTAI_since_2000.tex exdays_01.dat exdays_04.dat \
finals.all 
	echo " " >${builddir}/proleptic_UTC.bbl
	lualatex ${builddir}/proleptic_UTC.tex
	bibtex ${builddir}/proleptic_UTC.aux

# The extraordinary_days.dat file is constructed from five parts:
# exdays_01.dat is the introductory comments, exdays_02.dat is
# the expiration date, exdays_03.dat is the checksum line,
# exdays_04.dat is the header for the data, and exdays_05.dat
# is the data.  Exdays_01.dat and exdays_04.dat are source files.
# Exdays_02.dat is computed from IERS Bulletin C.  Exdays_03.dat is
# computed from the other four files, and exdays_05.dat is the output
# of the algorithm which converts Delta T into a schedule of extraordinary days.

# You can download an updated IERS finals.all file from
# https://maia.usno.navy.mil/ser7/finals.all.
# The UT1-UTC projections beyond finals.all use a formula
# in the latest issue of IERS Bulletin A, at
# https://maia.usno.navy.mil/ser7/ser7.dat.
# The expiration date is in IERS Bulletin C, at
# https://hpiers.obspm.fr/iers/bul/bulc/bulletinc.dat

# The recipe below downloads the three files and
# prints some information from the bulletins.  It also preserves the
# previous different download, so we can see what changed.

# Distribute the shell scripts which do the downloads and compares.
EXTRA_DIST += do_downloads.sh do_compare.sh

.PHONEY: download
download:
	bash do_downloads.sh

# The recipe below uses the IERS file to replace the estimates
# of delta T.  It also uses the leap seconds dates from Tony Finch
# and the IERS to replace the computed extraordinary days from 1958
# until the expiration date of the latest IERS Bulletin C.
#
# IERS_delta_t.tex is not used in the PDF file.  It shows the
# values of delta T after replacing the estimated values with
# the values from the IERS.
#
# If the file exdays_05.dat exists, which means this is a re-run,
# perhaps with newly downloaded data or a new algorithm for future
# leap seconds, save the old version of exdays_05.dat so we can see
# the changes in the schedule of leap seconds.
# The old value for IERS-projection-days was 1461.
#
exdays_05.dat : read_delta_t.py values_of_delta_T.csv finals.all ser7.dat
	if [ -f ${builddir}/exdays_05.dat ]; then \
	   mv ${builddir}/exdays_05.dat ${builddir}/exdays_05_previous.dat ; \
	fi
	if [ -f ${builddir}/UT1UTC.csv ]; then \
	   mv ${builddir}/UT1UTC.csv ${builddir}/UT1UTC_previous.csv ; \
	fi
	python3 ${srcdir}/read_delta_t.py ${srcdir}/values_of_delta_T.csv \
${builddir}/exdays_05.dat \
--latex-output ${builddir}/IERS_delta_t.tex \
--csv-output ${builddir}/delta_T.csv  \
--IERS-final=${srcdir}/finals.all --Tony-Finch-leaps --IERS-leaps \
--UT1UTC-output=${builddir}/UT1UTC.csv --UT1UTC-start-jdn=2305814 \
--USNO-delta-t=${srcdir}/USNO_delta_T.csv \
--IERS-Bulletin-A=${srcdir}/ser7.dat \
--IERS-projection-days=0
	if [ -f ${builddir}/exdays_05_previous.dat ]; then \
	   bash do_compare.sh ; \
	fi

# If you want to see what the next leap second would be if we just
# used the IERS projection for UT2, make the following file:

no_parabola_exdays_05.dat : read_delta_t.py values_of_delta_T.csv \
finals.all ser7.dat
	python3 ${srcdir}/read_delta_t.py ${srcdir}/values_of_delta_T.csv \
${builddir}/no_parabola_exdays_05.dat \
--IERS-final=${srcdir}/finals.all --Tony-Finch-leaps --IERS-leaps \
--UT1UTC-output=${builddir}/UT1UTC.csv --UT1UTC-start-jdn=2305814 \
--USNO-delta-t=${srcdir}/USNO_delta_T.csv \
--IERS-Bulletin-A=${srcdir}/ser7.dat \
--IERS-projection-days=-1

delta_t.tex : reformat_delta_t.py values_of_delta_T.csv
	python3 ${srcdir}/reformat_delta_t.py \
${srcdir}/values_of_delta_T.csv ${builddir}/delta_t.tex

extraordinary_days.dat : exdays_01.dat exdays_02.dat exdays_03.dat \
exdays_04.dat exdays_05.dat
	cat ${srcdir}/exdays_01.dat ${builddir}/exdays_02.dat \
${builddir}/exdays_03.dat ${srcdir}/exdays_04.dat \
${builddir}/exdays_05.dat > ${builddir}/extraordinary_days.dat
	python3 ${srcdir}/find_next_leap_second.py ${builddir}/UT1UTC.csv

exdays_02.dat : parse_bulletin_C.py bulletinc.dat
	python3 ${srcdir}/parse_bulletin_C.py ${srcdir}/bulletinc.dat \
--expiration-date-file=${builddir}/exdays_02.dat

# Compute the checksum by first creating a file without the checksum line
# then computing the checksum line from it.
exdays.dat : exdays_01.dat exdays_02.dat exdays_04.dat exdays_05.dat
	cat ${srcdir}/exdays_01.dat ${builddir}/exdays_02.dat \
${srcdir}/exdays_04.dat ${builddir}/exdays_05.dat > ${builddir}/exdays.dat

exdays_03.dat : read_extraordinary_days_table.py exdays.dat
	python3 ${srcdir}/read_extraordinary_days_table.py \
${builddir}/exdays.dat --checksum-file=${builddir}/exdays_03.dat

# If you omit the latex-start and latex-end from the following recipe
# you will get the whole extraordinary days table from the year -2000
# to the year 2500,  which will make the PDF over 1500 pages long.
extraordinary_days.tex : read_extraordinary_days_table.py extraordinary_days.dat
	python3 ${srcdir}/read_extraordinary_days_table.py \
${builddir}/extraordinary_days.dat \
--latex-output ${builddir}/extraordinary_days.tex \
--latex-start 2341972 --latex-end 2488070

# The figures are created using GNUplot.  If you change the spacing of
# the dates along the horizontal axis, in addition to editing the
# .gnuplot.in file you will need to edit this section of the Makefile.am
# file to provide a rule for building the xtics file, and add it to the
# dependencies for the figure.
gnuplot.dat : extraordinary_days.dat
	python3 ${srcdir}/read_extraordinary_days_table.py \
${builddir}/extraordinary_days.dat --gnuplot-output ${builddir}/gnuplot.dat

set_xtics_001mo.gnuplot : build_xtic_monthly_labels.py
	python3 ${srcdir}/build_xtic_monthly_labels.py \
${builddir}/set_xtics_001mo.gnuplot --interval 1

set_xtics_002mo.gnuplot : build_xtic_monthly_labels.py
	python3 ${srcdir}/build_xtic_monthly_labels.py \
${builddir}/set_xtics_002mo.gnuplot --interval 2

set_xtics_003mo.gnuplot : build_xtic_monthly_labels.py
	python3 ${srcdir}/build_xtic_monthly_labels.py \
${builddir}/set_xtics_003mo.gnuplot --interval 3

set_xtics_004mo.gnuplot : build_xtic_monthly_labels.py
	python3 ${srcdir}/build_xtic_monthly_labels.py \
${builddir}/set_xtics_004mo.gnuplot --interval 4

set_xtics_006mo.gnuplot : build_xtic_monthly_labels.py
	python3 ${srcdir}/build_xtic_monthly_labels.py \
${builddir}/set_xtics_006mo.gnuplot --interval 6

set_xtics_012mo.gnuplot : build_xtic_monthly_labels.py
	python3 ${srcdir}/build_xtic_monthly_labels.py \
${builddir}/set_xtics_012mo.gnuplot --interval 12

set_xtics_001yr.gnuplot : build_xtic_labels.py
	python3 ${srcdir}/build_xtic_labels.py \
${builddir}/set_xtics_001yr.gnuplot --interval 1

set_xtics_002yr.gnuplot : build_xtic_labels.py
	python3 ${srcdir}/build_xtic_labels.py \
${builddir}/set_xtics_002yr.gnuplot --interval 2

set_xtics_003yr.gnuplot : build_xtic_labels.py
	python3 ${srcdir}/build_xtic_labels.py \
${builddir}/set_xtics_003yr.gnuplot --interval 3

set_xtics_004yr.gnuplot : build_xtic_labels.py
	python3 ${srcdir}/build_xtic_labels.py \
${builddir}/set_xtics_004yr.gnuplot --interval 4

set_xtics_005yr.gnuplot : build_xtic_labels.py
	python3 ${srcdir}/build_xtic_labels.py \
${builddir}/set_xtics_005yr.gnuplot --interval 5

set_xtics_006yr.gnuplot : build_xtic_labels.py
	python3 ${srcdir}/build_xtic_labels.py \
${builddir}/set_xtics_006yr.gnuplot --interval 6

set_xtics_007yr.gnuplot : build_xtic_labels.py
	python3 ${srcdir}/build_xtic_labels.py \
${builddir}/set_xtics_007yr.gnuplot --interval 7

set_xtics_008yr.gnuplot : build_xtic_labels.py
	python3 ${srcdir}/build_xtic_labels.py \
${builddir}/set_xtics_008yr.gnuplot --interval 8

set_xtics_009yr.gnuplot : build_xtic_labels.py
	python3 ${srcdir}/build_xtic_labels.py \
${builddir}/set_xtics_009yr.gnuplot --interval 9

set_xtics_010yr.gnuplot : build_xtic_labels.py
	python3 ${srcdir}/build_xtic_labels.py \
${builddir}/set_xtics_010yr.gnuplot --interval 10

set_xtics_015yr.gnuplot : build_xtic_labels.py
	python3 ${srcdir}/build_xtic_labels.py \
${builddir}/set_xtics_015yr.gnuplot --interval 15

set_xtics_020yr.gnuplot : build_xtic_labels.py
	python3 ${srcdir}/build_xtic_labels.py \
${builddir}/set_xtics_020yr.gnuplot --interval 20

set_xtics_025yr.gnuplot : build_xtic_labels.py
	python3 ${srcdir}/build_xtic_labels.py \
${builddir}/set_xtics_025yr.gnuplot --interval 25

set_xtics_030yr.gnuplot : build_xtic_labels.py
	python3 ${srcdir}/build_xtic_labels.py \
${builddir}/set_xtics_030yr.gnuplot --interval 30

set_xtics_050yr.gnuplot : build_xtic_labels.py
	python3 ${srcdir}/build_xtic_labels.py \
${builddir}/set_xtics_050yr.gnuplot --interval 50

set_xtics_100yr.gnuplot : build_xtic_labels.py
	python3 ${srcdir}/build_xtic_labels.py \
${builddir}/set_xtics_100yr.gnuplot --interval 100

set_xtics_200yr.gnuplot : build_xtic_labels.py
	python3 ${srcdir}/build_xtic_labels.py \
${builddir}/set_xtics_200yr.gnuplot --interval 200

set_xtics_500yr.gnuplot : build_xtic_labels.py
	python3 ${srcdir}/build_xtic_labels.py \
$dstdir}/set_xtics_500yr.gnuplot --interval 500

values_of_DTAI.tex : gnuplot.dat plot_extraordinary_days.gnuplot \
set_xtics_200yr.gnuplot
	gnuplot plot_extraordinary_days.gnuplot

values_of_DTAI_since_1500.tex : gnuplot.dat \
plot_extraordinary_days_since_1500.gnuplot set_xtics_030yr.gnuplot
	gnuplot plot_extraordinary_days_since_1500.gnuplot

values_of_DTAI_since_1600.tex : gnuplot.dat \
plot_extraordinary_days_since_1600.gnuplot set_xtics_020yr.gnuplot
	gnuplot plot_extraordinary_days_since_1600.gnuplot

values_of_DTAI_since_1700.tex : gnuplot.dat \
plot_extraordinary_days_since_1700.gnuplot set_xtics_015yr.gnuplot
	gnuplot plot_extraordinary_days_since_1700.gnuplot

values_of_DTAI_since_1800.tex : gnuplot.dat \
plot_extraordinary_days_since_1800.gnuplot set_xtics_010yr.gnuplot
	gnuplot plot_extraordinary_days_since_1800.gnuplot

values_of_DTAI_since_1900.tex : gnuplot.dat \
plot_extraordinary_days_since_1900.gnuplot set_xtics_010yr.gnuplot
	gnuplot plot_extraordinary_days_since_1900.gnuplot

values_of_DTAI_since_1950.tex : gnuplot.dat \
plot_extraordinary_days_since_1950.gnuplot set_xtics_005yr.gnuplot
	gnuplot plot_extraordinary_days_since_1950.gnuplot

values_of_DTAI_since_2000.tex : gnuplot.dat \
plot_extraordinary_days_since_2000.gnuplot set_xtics_005yr.gnuplot
	gnuplot plot_extraordinary_days_since_2000.gnuplot

# The following charts are not used in the document, but may be
# built using Make.  They show the increasing frequency of leap
# seconds in the future.  By 2500 it will be common to have three
# in a year.

values_of_DTAI_since_2015.tex : gnuplot.dat \
plot_extraordinary_days_since_2015.gnuplot set_xtics_005yr.gnuplot
	gnuplot plot_extraordinary_days_since_2015.gnuplot

values_of_DTAI_since_2400.tex : gnuplot.dat \
plot_extraordinary_days_since_2400.gnuplot set_xtics_001yr.gnuplot
	gnuplot plot_extraordinary_days_since_2400.gnuplot

values_of_DTAI_since_2490.tex : gnuplot.dat \
plot_extraordinary_days_since_2490.gnuplot set_xtics_006mo.gnuplot
	gnuplot plot_extraordinary_days_since_2490.gnuplot

# Buld the PDF on demand, if requested.
pdf-local: proleptic_UTC.pdf
.PHONEY: pdf-local

# Include the PGP signature file in the repository.  Create it using
# "make signature".
signature : ${PACKAGE}-${VERSION}.tar.gz.asc
.PHONEY: signature

${PACKAGE}-${VERSION}.tar.gz.asc : ${PACKAGE}-${VERSION}.tar.gz
	rm -f ${PACKAGE}-*.tar.gz.asc
	gpg2 --detach-sign --armor ${PACKAGE}-${VERSION}.tar.gz

# Support make check and make distcheck
dist_check_DATA = check_output.txt check_expected_output.txt
dist_check_SCRIPTS = verify_files_template.sh

TESTS = verify_files.sh
verify_files.sh : verify_files_template.sh check_output.txt 
	cp $(srcdir)/verify_files_template.sh verify_files.sh
	if [ ! -r "check_expected_output.txt" ] ; then cp $(srcdir)/check_expected_output.txt check_expected_output.txt ; touch copied_from_srcdir ; fi
	chmod +x verify_files.sh

check_output.txt : read_extraordinary_days_table.py extraordinary_days.dat
	python3 ${srcdir}/read_extraordinary_days_table.py ${builddir}/extraordinary_days.dat | tee ${builddir}/check_output.txt

# When removing files, also remove the followins:
CLEANFILES = \
delta_t.tex \
exdays_02.dat \
IERS_delta_t.tex \
delta_T.csv \
exdays_05.dat \
no_parabola_exdays_05.dat \
UT1UTC.csv \
exdays.dat \
exdays_03.dat \
extraordinary_days.dat \
extraordinary_days.tex \
verify_files.sh \
check_output.txt \
gnuplot.dat \
set_xtics_200yr.gnuplot \
set_xtics_025yr.gnuplot \
set_xtics_030yr.gnuplot \
set_xtics_020yr.gnuplot \
set_xtics_015yr.gnuplot \
set_xtics_010yr.gnuplot \
set_xtics_005yr.gnuplot \
set_xtics_001yr.gnuplot \
set_xtics_006mo.gnuplot \
gnuplot-lua-tikz.sty \
t-gnuplot-lua-tikz.tex \
gnuplot-lua-tikz.tex \
gnuplot-lua-tikz-common.tex \
values_of_DTAI.tex \
values_of_DTAI.tex.aux \
values_of_DTAI_since_1500.tex \
values_of_DTAI_since_1600.tex \
values_of_DTAI_since_1700.tex \
values_of_DTAI_since_1800.tex \
values_of_DTAI_since_1900.tex \
values_of_DTAI_since_1950.tex \
values_of_DTAI_since_2000.tex \
values_of_DTAI_since_2015.tex \
values_of_DTAI_since_2400.tex \
values_of_DTAI_since_2490.tex \
values_of_DTAI.aux \
values_of_DTAI_since_1500.aux \
values_of_DTAI_since_1600.aux \
values_of_DTAI_since_1700.aux \
values_of_DTAI_since_1800.aux \
values_of_DTAI_since_1900.aux \
values_of_DTAI_since_1950.aux \
values_of_DTAI_since_2000.aux \
values_of_DTAI_since_2015.aux \
values_of_DTAI_since_2400.aux \
values_of_DTAI_since_2490.aux \
proleptic_UTC.bbl \
proleptic_UTC.log \
proleptic_UTC.aux \
proleptic_UTC.out \
proleptic_UTC.blg \
proleptic_UTC.brf \
proleptic_UTC.pdf

clean-local: clean-local-check
.PHONEY: clean-local-check
clean-local-check:
	if [ -e "copied_from_srcdir" ] ; then rm -f check_expected_output.txt ; rm copied_from_srcdir ; fi
	rm -rf autom4te.cache
	rm -f trace*.txt
	rm -f *~

# end of file Makefile.am
