CREATE TABLE test(
   upload_timestamp TEXT,
   sequence_no INTEGER,
   state INTEGER,
   tick_count  INTEGER,
   state_delta INTEGER,
   tick_delta  INTEGER,
   time_stamp TEXT,
   s1 INTEGER, 
   s2 INTEGER,
   s3 INTEGER,
   s4 INTEGER,
   s5 INTEGER,
   s6 INTEGER,
   s7 INTEGER,
   s8 INTEGER,
   s9 INTEGER,
   s10 INTEGER,
   s11 INTEGER,
   s12 INTEGER,
   s13 INTEGER,
   s14 INTEGER,
   s15 INTEGER,
   s16 INTEGER,   
   d1 INTEGER, 
   d2 INTEGER,
   d3 INTEGER,
   d4 INTEGER,
   d5 INTEGER,
   d6 INTEGER,
   d7 INTEGER,
   d8 INTEGER,
   d9 INTEGER,
   d10 INTEGER,
   d11 INTEGER,
   d12 INTEGER,
   d13 INTEGER,
   d14 INTEGER,
   d15 INTEGER,
   d16 INTEGER,
   Reset BOOLEAN
   );
   
.mode csv
.import outputtest.csv test
