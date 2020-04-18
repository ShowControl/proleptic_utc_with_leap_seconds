#!/bin/bash
# File: rebuild_figures.sh; Author: John Sauter; date: June 21, 2016
# Recreate the figures from the extraordinary days table.

# Run read_extraordinary_days, telling it to output a file
# for gnuplot.  Don't limit the time interval--we will do that
# when we create each plot.
python3 read_extraordinary_days_table.py extraordinary_days.dat --gnuplot-output gnuplot.dat

# Run GNUplot for each figure.  You can choose the frequency of labels
# on the time axis by selecting an appropriate set_xtics_*.gnuplot file
# in the plot_extraordinary_days*.gnuplot file.  If you want more choices,
# edit and run build_all_xtics.sh.
#
# There is also set_xtics_all_extraordinary_days.gnuplot, that labels the
# time axis at every extraordinary day.  I didn't find a use for it in the
# paper, but if you are doing a narrowly-focused plot you might find it
# useful.  It will need to be updated manually if you change the table
# of extraordinary days.
#
gnuplot plot_extraordinary_days.gnuplot
gnuplot plot_extraordinary_days_since_1500.gnuplot
gnuplot plot_extraordinary_days_since_1600.gnuplot
gnuplot plot_extraordinary_days_since_1700.gnuplot
gnuplot plot_extraordinary_days_since_1800.gnuplot
gnuplot plot_extraordinary_days_since_1900.gnuplot

# End of file rebuild_figures.sh
