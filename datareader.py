#!/ usr/bin/python

import numpy as np
import csv
import datetime as dt
import sys

def timereader(timestr, formatstr="%d/%m/%Y %H:%M"): #Change %Y to %y if necessary...
    return dt.datetime.strptime(timestr, formatstr)
    
def binlistxor(list1, list2):
    if len(list1) != len(list2):
        raise TypeError("Lists not the same length")
    else:
        return [(list1[i]+list2[i]) % 2 for i in range(len(list1))]

def read_array_from_csv(csvfiletoread):
    data_array = []
    with open(csvfiletoread, 'rb') as csvfile:
        readerobj = csv.reader(csvfile)
        for row in readerobj:
            data_array.append(row)
    return data_array

#"""delete null rows"""
#def nullrowdelete(nparray):
#    nullrows = []
#   for row in range(nparray.shape[0]):
#        if "NULL" in nparray[row]:
#            print "NULL found in row", row
#            nullrows.append(row)
#    print "Shape", nparray.shape
#    cleansed_array = np.delete(nparray, nullrows, axis=0)            
#    print "Shape after deleting null rows", cleansed_array.shape
#    return cleansed_array
    
def binreader16bit(abcde):
    return map(int, list(bin(abcde)[2:].zfill(16)))
    
def binreader8bit(abcde):
    return map(int, list(bin(abcde)[2:].zfill(8)))

def data_extractor_dlrlifts(array): 
    output = [] 
    timestamp = timereader(array[0][0])
    seqnum = array[0][1]
    delta = 0
    previous_tc = 0
    previous_state = 0
    #tickcount = previous_tc
    reset = True
    line = 0
    for row in array:
        upload_timestamp = timereader(row[0])       
        if reset:
            previous_tickcount = int(row[6])
            previous_state = int(row[5])
            prev_dt_precise_timestamp = timereader(row[0])
            #reset=False
        #seqnumprev = seqnum
        #seqnumnew = int(nparray[row][1])
        #if seqnumprev != seqnumnew - 1:
        #   pass
            #print "Warning: sequences off!", seqnumprev, "followed by", seqnumnew
            #print "Delay:", int(np_data_array[row][6])-int(np_data_array[row-1][24])
        seqnum = row[1]
        #timestamp_delay = timestamp - timereader(nparray[row][0])
        #timestamp_delay = timestamp_delay.total_seconds()
        #if row % 100 == 0:
        #    print "row", row, #"Timestamp delay", timestamp_delay
        data_pairs =  [ [row[5+2*i], row[6+2*i]] for i in range(len(row[5::2]))]
        for pair in data_pairs:
            if pair[0] == 'NULL' or pair[1] == 'NULL':
                break
            state = int(pair[0])
            tickcount = int(pair[1])
            if state == 0 and tickcount == 0:
                pass
            else:
                tickcount_delta = (tickcount - previous_tickcount) % 65536
                dt_tickcount_delta = dt.timedelta(microseconds = tickcount_delta*10000)
                dt_precise_timestamp = prev_dt_precise_timestamp + dt_tickcount_delta #Try and work out the timestamp from the previous one...
                state_delta = state ^ previous_state
                #print "dt_precise_timestamp is", dt_precise_timestamp
                #print "upload_timestamp is", upload_timestamp
                #print "tickcount_delta is", tickcount_delta
                #print "seconds difference is", (dt_precise_timestamp - upload_timestamp).total_seconds()
                if abs((dt_precise_timestamp - upload_timestamp).total_seconds()) >= 70:
                    for i in [-1,0,1,2,3,4,5,6,7,8,9,10,11,12]: #Guessing how many times the tickcounter has cycled
                        tickcount_delta = tickcount - previous_tickcount + i*65536
                        dt_tickcount_delta = dt.timedelta(microseconds = tickcount_delta*10000)
                        dt_precise_timestamp = prev_dt_precise_timestamp + dt_tickcount_delta
                        if abs((dt_precise_timestamp - upload_timestamp).total_seconds()) < 70:
                            reset = False
                            print "Tickcount cycled", i, "times at", dt_precise_timestamp
                            break
                        else:
                            tickcount_delta = 0 #Resetting the tickcount delta if no match was found
                            reset = True
                else:
                    pass
                if reset:
                    print "found reset", dt_precise_timestamp, upload_timestamp, "line", line
                    dt_precise_timestamp = upload_timestamp          
                else:
                    pass
                newrow = []
                newrow.append(dt.datetime.strftime(upload_timestamp, "%Y-%m-%d %H:%M:%S.%f")[:-3]) #Upload timestamp
                newrow.append(seqnum) #Sequence number
                newrow.append(state)
                newrow.append(tickcount)
                newrow.append(state_delta) #State delta
                newrow.append(tickcount_delta) #Tickcount delta deduced
                newrow.append(dt.datetime.strftime(dt_precise_timestamp, "%Y-%m-%d %H:%M:%S.%f")[:-3])#timestamp
                newrow = newrow + binreader16bit(state)[::-1] #state descriptions
                newrow = newrow + binreader16bit(state_delta)[::-1] #state delta descriptions
                newrow.append(reset)
                previous_tickcount = tickcount
                previous_state = state
                prev_dt_precise_timestamp = dt_precise_timestamp       
                output.append(newrow)
                line += 1
                reset = False
    return output
            
#np_data_array = nullrowdelete(np_data_array)

def write_array_to_csv(array, output):
    with open(output, 'wb') as csvfile:
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
    
print __name__  
if __name__ == "__main__":
    filename = raw_input('Enter input filename: ')
    outputfilename = raw_input('Enter output filename: ')
    print filename
    print "running"
    np_data_array = read_array_from_csv(filename)           
    outputarray = data_extractor_dlrlifts(np_data_array)
    write_array_to_csv(outputarray, outputfilename)
                
