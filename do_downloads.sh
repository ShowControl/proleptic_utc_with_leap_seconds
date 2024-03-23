# File: do_downloads.sh, author: John Sauter, date: March 21, 2024.
#
# Download data files from the IERS.

#   Copyright © 2024 by John Sauter <John_Sauter@systemeyescomputerstore.com>

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

# Download the current copy of IERS Bulletin A.
mkdir -p previous
cp -p ser7.dat previous/ser7.dat
wget -N https://maia.usno.navy.mil/ser7/ser7.dat
diff -q ser7.dat previous/ser7.dat
if [ $? -ne 0 ]; then
    cp -p previous/ser7.dat different/ser7.dat
fi

# When the USNO web site was down, the file was on the IERS weh site.
#cp -p 6_BULLETIN_A_V2013_016.txt previous/6_BULLETIN_A_V2013_016.txt
#wget -N https://datacenter.iers.org/data/latestVersion/6_BULLETIN_A_V2013_016.txt
#diff -q 6_BULLETIN_A_V2013_016.txt previous/6_BULLETIN_A_V2013_016.txt
#if [ $? -ne 0 ]; then
#    cp -p previous/6_BULLETIN_A_V2013_016.txt different/6_BULLETIN_A_V2013_016.txt
#fi

# Download the current copy of IERS Bulletin C.
cp -p bulletinc.dat previous/bulletinc.dat
wget -N https://hpiers.obspm.fr/iers/bul/bulc/bulletinc.dat
diff -q previous/bulletinc.dat bulletinc.dat
if [ $? -ne 0 ]; then
    cp -p previous/bulletinc.dat different/bulletinc.dat
fi

# When the USNO web site was down, the file was on the IERS web site.
#cp -p 16_BULLETIN_C16.txt previous/16_BULLETIN_C16.txt
#wget -N https://datacenter.iers.org/data/latestVersion/16_BULLETIN_C16.txt
#diff -q previous/16_BULLETIN_C16.txt 16_BULLETIN_C16.txt
#if [ $? -ne 0 ]; then
#    cp -p previous/16_BULLETIN_C16.txt different/16_BULLETIN_C16.txt
#fi

# Download the file of historical and predicted values of UT1-UTC.
cp -p finals.all previous/finals.all
wget -N https://maia.usno.navy.mil/ser7/finals.all
diff -q previous/finals.all finals.all
if [ $? -ne 0 ]; then
    cp -p previous/finals.all different/finals.all
fi

# When the USNO web site was down, a similar file was on the IERS web site.
#cp -p finals.all.csv previous/finals.all.csv
#wget -N https://datacenter.iers.org/data/csv/finals.all.csv
#diff -q previous/finals.all.csv finals.all.csv
#if [ $? -ne 0 ]; then
#    cp -p previous/finals.all.csv different/finals.all.csv
#fi

# Preserve the old copy of extraordinary_days.dat for debugging.
if [ -f extraordinary_days.dat ]; then
    cp -p extraordinary_days.dat previous/extraordinary_days.dat
fi

# Check the downloaded bulletins A and C.
python3 parse_bulletin_A.py ser7.dat
python3 parse_bulletin_C.py bulletinc.dat

# End of file do_downloads.sh
