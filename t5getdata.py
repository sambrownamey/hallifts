#!/ usr/bin/python

from datareader import *
import os

##To do: make sure the lifts are read in the right order -- this means reading all of lift 2 first, in order of date, then all of lift 5, etc...

def recursive_list_dir(folder,dosorting = True):
    output = []
    for a,b,c in os.walk(folder):
        for thefile in c:
            output.append(os.path.join(a,thefile))
    if dosorting:
        sortedoutput = []
        output.sort() #Does the sorting by date
        sortednumbers=sorted(list(set([int(filepath[27:-4]) for filepath in output]))) #Gets the lift numbers
        for lift in sortednumbers:
            files = [fn for fn in output if int(fn[27:-4])==lift]
            sortedoutput.extend(files)
        return sortedoutput
    else:            
        return output

def read_csv_with_filename_column(csvfiletoread):
    data_array = []
    filename_column = csvfiletoread[27:-4]
    with open(csvfiletoread, 'rb') as csvfile:
        print "Reading", csvfiletoread, "for lift number", filename_column
        readerobj = csv.reader(csvfile)
        for row in readerobj:
            row = row + [filename_column]
            data_array.append(row)
    return data_array

def read_array_from_multiple_csvs(folder):
    files = recursive_list_dir(folder)
    array = []
    for thefile in files:
        array = array + read_csv_with_filename_column(thefile)
    return array

def data_extractor_t5(array):
    output_array = [] #Initialize the output array
    datetime_previous_timestamp = timereader(array[0][0], formatstr="%Y-%m-%d %H:%M:%S") #Setting the 'previous timestamp' so that the code works for the first row!
    last_lift = array[0][5] #Setting the 'last lift' so that the code works for the first row
    reset_on_this_row = True
    initial_time_delta = dt.timedelta(0)
    initial_c1_delta = 0 
    initial_c2_delta = 0
    initial_c_delta = 0
    time_delay_tolerance = 90 #Change this if desired
    first_row = True #Switch changes to false after row 1, unless it is the first row of data for a different lift number.
    for row in array:
        newrow = [] #Initializing the new row
        datetime_timestamp = timereader(row[0], formatstr="%Y-%m-%d %H:%M:%S") #Reading the time as a datetime object
        newrow.append(dt.datetime.strftime(datetime_timestamp, "%Y-%m-%d %H:%M:%S.%f")[:-3]) #Writing the timestamp as a string
        this_lift = row[5]
        c1 = int(row[1]) #reading the state c1
        c2 = int(row[2]) #reading the state c2
        c = (c1 & 0x00FF) + ((c2 & 0x0F) << 8) #Combining the states; last 4 bits of c2 followed by last 8 bits of c1
        raw_time_delta = datetime_timestamp - datetime_previous_timestamp #Calculating the time delta
        #print "time delta", raw_time_delta.total_seconds(), "seconds"
        if (this_lift != last_lift):
            first_row = True
        else:
            pass
        if (raw_time_delta.total_seconds() >= time_delay_tolerance) or first_row:
            reset_on_this_row = True
        else:
            pass
        if first_row:
            time_delta = initial_time_delta    
            c1_delta = initial_c1_delta
            c2_delta = initial_c2_delta
            c_delta = initial_c_delta
        else:
            time_delta = raw_time_delta
            c1_delta = c1 ^ previous_c1
            c2_delta = c2 ^ previous_c2
            c_delta = c ^ previous_c
        newrow.append(time_delta.total_seconds()) #Adding the timedelta (calculated on the previous loop)
        newrow.append(row[5]) #The lift number
        #newrow.append(c1) #First state code
        #newrow.append(c2) #Second state code
        
        #newrow.extend(binreader16bit(c1)[-1:-9:-1]) #The eight bit columns from the first state code (reverse order)
        #newrow.extend(binreader16bit(c1_delta)[-1:-9:-1])
        #newrow.extend(binreader16bit(c2)[-1:-9:-1]) #The eight bit columns from the second state code (reverse order)
        #newrow.extend(binreader16bit(c2_delta)[-1:-9:-1])
        newrow.append(c) #Combined state code
        newrow.append(c_delta) #Combined state delta
        newrow.extend(binreader16bit(c)[-1:-13:-1]) #Twelve bit columns of combined state (in order 1,2,4,8... from left to right)
        newrow.extend(binreader16bit(c_delta)[-1:-13:-1]) #Twelve bit columns of c_delta
        floor = (c2 & 0xF0) >> 4 #Decoding the floor
        newrow.append(floor) #The floor
        newrow.append(reset_on_this_row)
        output_array.append(newrow)
        datetime_previous_timestamp = datetime_timestamp #Updating the "previous timestamp".
        previous_c1 = c1
        previous_c2 = c2
        previous_c = c
        last_lift = this_lift
        reset_on_this_row = False
        first_row = False
    return output_array
 
if __name__ == "__main__":
    print "running"
    raw_data = read_array_from_multiple_csvs('dbr/')           
    outputarray = data_extractor_t5(raw_data)
    write_array_to_csv(outputarray, "outputt5.csv")  


