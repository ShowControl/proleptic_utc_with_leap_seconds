#!/bin/bash
# File: build_all_xtics.sh; Author: John Sauter; date: December 18, 2016
# Create all of the xtics files for gnuplot
python3 build_xtic_labels.py set_xtics_001yr.gnuplot --interval 1
python3 build_xtic_labels.py set_xtics_002yr.gnuplot --interval 2
python3 build_xtic_labels.py set_xtics_003yr.gnuplot --interval 3
python3 build_xtic_labels.py set_xtics_004yr.gnuplot --interval 4
python3 build_xtic_labels.py set_xtics_005yr.gnuplot --interval 5
python3 build_xtic_labels.py set_xtics_006yr.gnuplot --interval 6
python3 build_xtic_labels.py set_xtics_007yr.gnuplot --interval 7
python3 build_xtic_labels.py set_xtics_008yr.gnuplot --interval 8
python3 build_xtic_labels.py set_xtics_009yr.gnuplot --interval 9
python3 build_xtic_labels.py set_xtics_010yr.gnuplot --interval 10
python3 build_xtic_labels.py set_xtics_015yr.gnuplot --interval 15
python3 build_xtic_labels.py set_xtics_020yr.gnuplot --interval 20
python3 build_xtic_labels.py set_xtics_025yr.gnuplot --interval 25
python3 build_xtic_labels.py set_xtics_050yr.gnuplot --interval 50
python3 build_xtic_labels.py set_xtics_100yr.gnuplot --interval 100
python3 build_xtic_labels.py set_xtics_200yr.gnuplot --interval 200
python3 build_xtic_labels.py set_xtics_500yr.gnuplot --interval 500

# End of file build_all_xtics.sh
