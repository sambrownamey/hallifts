# hallifts

<b>Python scripts</b>

The datareader.py script should work for the dlr data. The "timereader" function at the top may need altering between the test set and the real data, because the timestamp is formatted differently (%Y versus %y). Running the script from the command line should ask for the input and output filenames.

The t5getdata.py script should work for t5 data. The filenames need manually adding into the script (but should be correct at the moment). The script assumes the "dbr/" folder containing the data is in the current directory.

<b>SQL scripts</b>

The names of the tables and input filenames need manually changing in the scripts, then they can be run using .read create_sql_table_cal.sql for the DLR lifts (or .read create_sql_table_t5.sql for T5) in SQLite. The database needs to be created first in SQLite.
