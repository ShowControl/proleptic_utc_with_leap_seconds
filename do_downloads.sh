# File: do_downloads.sh, author: John Sauter, date: July 9, 2020.
#
# Download data files from the IERS.

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

cp -p 6_BULLETIN_A_V2013_016.txt previous/6_BULLETIN_A_V2013_016.txt
wget -N https://datacenter.iers.org/data/latestVersion/6_BULLETIN_A_V2013_016.txt
diff -q 6_BULLETIN_A_V2013_016.txt previous/6_BULLETIN_A_V2013_016.txt
if [ $? -ne 0 ]; then
    cp -p previous/6_BULLETIN_A_V2013_016.txt different/6_BULLETIN_A_V2013_016.txt
fi
cp -p 16_BULLETIN_C16.txt previous/16_BULLETIN_C16.txt
wget -N https://datacenter.iers.org/data/latestVersion/16_BULLETIN_C16.txt
diff -q previous/16_BULLETIN_C16.txt 16_BULLETIN_C16.txt
if [ $? -ne 0 ]; then
    cp -p previous/16_BULLETIN_C16.txt different/16_BULLETIN_C16.txt
fi
cp -p finals.all.csv previous/finals.all.csv
wget -N https://datacenter.iers.org/data/csv/finals.all.csv
diff -q previous/finals.all.csv finals.all.csv
if [ $? -ne 0 ]; then
    cp -p previous/finals.all.csv different/finals.all.csv
fi
if [ -f extraordinary_days.dat ]; then
    cp -p extraordinary_days.dat previous/extraordinary_days.dat
fi

python3 parse_bulletin_A.py 6_BULLETIN_A_V2013_016.txt
python3 parse_bulletin_C.py 16_BULLETIN_C16.txt

# End of file do_downloads.sh

