#!/bin/bash
# File: fix_files.sh, author: John Sauter, date: October 28, 2023.
#
# Imbedding files in a PDF loses their subdirectory and permissions.
# Restore them.

chmod +x configure
chmod +x autogen.sh
chmod +x test-driver

# Re-create the soft link

ln -s ../parse_bulletin_A.py survey_UT2_slope/parse_bulletin_A.py

# End of file fix_files.sh
