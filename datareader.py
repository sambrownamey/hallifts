#!/ usr/bin/python

import numpy as np
import csv
import datetime as dt

initial_timestamp_offset = 3500
data_array = []
sqlite_table = []

def timereader(timestr):
    return dt.datetime.strptime(timestr, "%d/%m/%Y %H:%M")

with open('Test.csv', 'rb') as csvfile:
    readerobj = csv.reader(csvfile)
    for row in readerobj:
        data_array.append(row)

np_data_array = np.array(data_array)

"""delete null rows"""
def nullrowdelete(nparray):
    nullrows = []
    for row in range(nparray.shape[0]):
        if "NULL" in nparray[row]:
            print "NULL found in row", row
            nullrows.append(row)
    print "Shape", nparray.shape
    cleansed_array = np.delete(nparray, nullrows, axis=0)            
    print "Shape after deleting null rows", nparray.shape
    return cleansed_array

#timestamp = initial_timestamp
#seqnum = 2
#delta = 0

#tickcount = int(np_data_array[0][6])
#previous_tc = tickcount

def data_extractor(nparray, start, end, initial_delay=0):    
    timestamp = timereader(nparray[start][0])
    seqnum = nparray[start][1]
    delta = 0
    previous_tc = 0
    #tickcount = previous_tc
    reset_timestamp = False
    for row in range(start, end):
        if reset_timestamp:
            timestamp = timereader(nparray[row][0])
            previous_tc = int(nparray[row][6])-50 
            reset_timestamp = False
        seqnumprev = seqnum
        seqnumnew = int(nparray[row][1])
        if seqnumprev != seqnumnew - 1:
            pass
            #print "Warning: sequences off!", seqnumprev, "followed by", seqnumnew
            #print "Delay:", int(np_data_array[row][6])-int(np_data_array[row-1][24])
        seqnum = seqnumnew
        timestamp_delay = timestamp - timereader(np_data_array[row][0])
        timestamp_delay = timestamp_delay.total_seconds()
        #if abs(timestamp_delay)>120:
         #   raise ValueError("timestamp delay too great")
        #    print "row", row
            #timestamp = timereader(np_data_array[row][0])
            #print "Resetting timestamp at row", row, "to", timestamp
        if row % 100 == 0:
            print "row", row, "Timestamp delay", timestamp_delay
        for i in range(10):
            #print i
            current_tc = int(nparray[row][2*i+6])
            #print "Comparing", current_tc, "with existing cyclic tickcount", previous_tc     
            """Check if the tickcount has reset"""
            if previous_tc - current_tc == 0:
                print "Error: zero tickcount delta. Trying next row:", row
                reset_timestamp = True   
                break
            if previous_tc - current_tc > 20000:
                delta = 65536 + current_tc - previous_tc
            # print ">
            #"""Check if the tickcount looks likely to have un-reset..."""
            elif current_tc - previous_tc > 20000:
                    delta = current_tc - previous_tc - 65536
            else:
                delta = current_tc - previous_tc
            #tickcount = tickcount + delta
            timestamp = timestamp + dt.timedelta(microseconds = delta*10000)
            newrow = []
            newrow.append[np_data_array[row][0]] #Upload timestamp
            newrow.append(seqnum) #Sequence number
            newrow.append(nparray[row][2*i+5]) #State
            newrow.append(
            newrow.append(dt.datetime.strftime(timestamp, "%d/%m/%Y %H:%M:%S.%f"))
            
            newrow.append(nparray[row][2*i+5])
            previous_tc = current_tc
            #print newrow        
            sqlite_table.append(newrow)
    return sqlite_table
            
np_data_array = nullrowdelete(np_data_array)

initial_timestamp = timereader(np_data_array[0][0]) + dt.timedelta(microseconds = initial_timestamp_offset*10000)

print initial_timestamp
            
data_extractor(np_data_array, 0, 31000)
        
#print "SQLite table: "
#print sqlite_table

#put this inside a function with a tolerance in the sequence number and the delta, so it re-starts if they are too big...
