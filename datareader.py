#!/ usr/bin/python

import numpy as np
import csv
import datetime as dt
#import sqlite3

def timereader(timestr):
    return dt.datetime.strptime(timestr, "%d/%m/%Y %H:%M")

def read_array_from_csv(csvfiletoread):
    data_array = []
    with open(csvfiletoread, 'rb') as csvfile:
        readerobj = csv.reader(csvfile)
        for row in readerobj:
            data_array.append(row)
    return np.array(data_array)

"""delete null rows"""
def nullrowdelete(nparray):
    nullrows = []
    for row in range(nparray.shape[0]):
        if "NULL" in nparray[row]:
            print "NULL found in row", row
            nullrows.append(row)
    print "Shape", nparray.shape
    cleansed_array = np.delete(nparray, nullrows, axis=0)            
    print "Shape after deleting null rows", cleansed_array.shape
    return cleansed_array
    
def binreader16bit(abcde):
    return map(int, list(bin(abcde)[2:].zfill(16)))

def data_extractor(nparray, start, end, initial_delay=0): 
    data_array = []
    sqlite_table = []   
    timestamp = timereader(nparray[start][0])
    seqnum = nparray[start][1]
    delta = 0
    previous_tc = 0
    previous_state = 0
    #tickcount = previous_tc
    reset_timestamp = False
    for row in range(start, end):
        if reset_timestamp:
            timestamp = timereader(nparray[row][0])
            previous_tc = int(nparray[row][6])-50
            previous_state = 0
            reset_timestamp = False
        seqnumprev = seqnum
        seqnumnew = int(nparray[row][1])
        if seqnumprev != seqnumnew - 1:
            pass
            #print "Warning: sequences off!", seqnumprev, "followed by", seqnumnew
            #print "Delay:", int(np_data_array[row][6])-int(np_data_array[row-1][24])
        seqnum = seqnumnew
        timestamp_delay = timestamp - timereader(nparray[row][0])
        timestamp_delay = timestamp_delay.total_seconds()
        if row % 100 == 0:
            print "row", row, "Timestamp delay", timestamp_delay
        try:
            for i in range(10):
                #print i
                current_tc = int(nparray[row][2*i+6]) 
                """Check if the tickcount has reset"""
                if previous_tc - current_tc == 0:
                    print "Error: zero tickcount delta. Trying next row:", row
                    reset_timestamp = True   
                    break
                if previous_tc - current_tc > 20000:
                    delta = 65536 + current_tc - previous_tc
                #"""Check if the tickcount looks likely to have un-reset..."""
                elif current_tc - previous_tc > 20000:
                        delta = current_tc - previous_tc - 65536
                else:
                    delta = current_tc - previous_tc
                #tickcount = tickcount + delta
                state = int(nparray[row][2*i+5])
                state_delta = state - previous_state
                #print "state delta", state_delta
                timestamp = timestamp + dt.timedelta(microseconds = delta*10000)
                newrow = []
                newrow.append(dt.datetime.strftime(timereader(nparray[row][0]), "%Y-%m-%d %H:%M:%S.%f")[:-3]) #Upload timestamp
                newrow.append(seqnum) #Sequence number
                newrow.append(nparray[row][2*i+5]) #State
                newrow.append(current_tc) #Tickcount
                newrow.append(state_delta % 65536) #State delta mod 65536
                newrow.append(delta) #Tick delta
                newrow.append(dt.datetime.strftime(timestamp, "%Y-%m-%d %H:%M:%S.%f")[:-3])#timestamp
                newrow = newrow + binreader16bit(state) #state descriptions
                newrow = newrow + binreader16bit(state_delta % 65536) #state delta (mod 65536) descriptions
                #excel_reference = ['F', 'H', 'J', 'L', 'N', 'P', 'R', 'T', 'V', 'X'][i] + str(row+1)
                #newrow = [excel_reference] + newrow
                previous_tc = current_tc
                previous_state = state
                #print newrow        
                sqlite_table.append(newrow)
        except ValueError:
            print "Error encountered. Skipping to the next row." #deals with the few null rows in the csv file
    return sqlite_table
            
#np_data_array = nullrowdelete(np_data_array)

def write_array_to_csv(array, output = "output.csv"):
    with open("output.csv", 'wb') as csvfile:
        thewriter = csv.writer(csvfile)
        for row in array:
            thewriter.writerow(row)
    print "Written to", output

def zero_sd_finder(thecsvfile, columntolook, columntoreturn):
    returnlist = []
    array_to_read = read_array_from_csv(thecsvfile)
    for i in range(array_to_read.shape[0]):
        if array_to_read[i][columntolook] == '0':
            returnlist.append(array_to_read[i][columntoreturn])
    return returnlist
            
