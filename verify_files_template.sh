#!/bin/bash
# File: verify_files_template.sh, author: John Sauter, date: August 29, 2020. 
# This file is executed as verify_files.sh to check extraordinary_days.dat.

diff check_output.txt check_expected_output.txt
diff_result=$?
if [[ $diff_result -ne 0 ]]; then
  exit $diff_result
fi

# End of file verify_files_template.sh
