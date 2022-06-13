# -*- coding: utf-8 -*-
"""
Created on Sat Jun 11 16:57:12 2022

Set of functions for the yaml_script.

@author: dpava
"""

import datetime as dt

#### Extracting the relevant job information from ymal files

def open_file(file):
    '''
        Reads a yaml file and looks for keywords, extracts strings that match, and append them to a list which is then returned. 
    '''
    # List to store key information
    data = []
    # Keywords in yaml file to be found
    keywords = ['submitted_at:','id:','type:','method:','nsequences:','ncharacters:','completed_at:','num_threads:','query_length:','databases_ncharacters_total:']

    # Read the yaml file, finds the keywords and strips spaces and new lines
    with open (file,'r') as job:

        reader = job.readlines()

        for i in reader:
            for j in keywords: 
                if j in i:
                    data.append(i.strip(' ').strip('\n'))
    return data

### Calculating the total number of sequences
# Returns the total number of sequences
def total_sequences(lista):
    '''
        Receives a list, looks for the `nsequences: ` string and returns the total number of sequences used as a integer.
    '''
    nseq = 0
    for i in lista:
        if 'nsequences:' in i:
            num_seq = int(i.replace('nsequences: ','').replace("'",''))
            nseq +=  num_seq
    return nseq


### Calculating job duration
# Function - returns a dictionary with time data necessary for delta time package
def time_filter (time):
    '''
        Receives a string with datetime values in string and returns a dictionary with the values for a datetime object
    '''
    new_time = time.replace(' ',',')
    for i in time[::-1]:
        if i == '+':
            new_time = new_time[:time.index(i)-1].replace('-','').replace(':','')
    
    year = int(new_time[0:4])
    month = int(new_time[4:6])
    day = int(new_time[6:8])
    hour = int(new_time[9:11])
    minute = int(new_time[11:13])
    seconds = int(new_time[13:15])
    micro = int(new_time[16:22])

    
    dic = {
        'year':year,
        'month':month,
        'day':day,
        'hour':hour,
        'minute':minute,
        'seconds':seconds,
        'micro':micro}

    return dic

### Calculates the delta between start and end

def delta_time(st,et):
    '''
        Receives two dictionaries with datetime values returns a datetime object with the difference in time
    '''
    start = dt.datetime(st['year'],st['month'],st['day'],st['hour'],st['minute'],st['seconds'],st['micro'])
    end = dt.datetime(et['year'],et['month'],et['day'],et['hour'],et['minute'],et['seconds'],et['micro'])
    
    delta = end - start

    return delta

# Function to merge both functions and return the result as a datetime object and in minutes 
def job_duration(start_time,end_time):
    
    '''
        Receives 2 datetime strings, calculates the difference and returns a datetime object [0] or the difference in minutes [1]
    '''
    start_dict = time_filter(start_time)
    end_dict = time_filter(end_time)
    
    delta = delta_time(start_dict,end_dict)
    delta_in_minutes = divmod(delta.total_seconds(),60)[0]
    
    return delta, delta_in_minutes

### Function to assign a job duration into a category 
def duration_bins(datetime_object):
    '''
        Receives a datetime object and returns a string with the estimated bin duration
    '''
    if dt.timedelta(minutes = 5) >= datetime_object >= dt.timedelta(seconds = 60):
        bin = '1 to 5 minutes'
    elif dt.timedelta(minutes = 10) >= datetime_object >= dt.timedelta(minutes = 5, seconds = 1):
        bin = '5 to 10 minutes'
    elif dt.timedelta(minutes = 30) >= datetime_object >= dt.timedelta(minutes = 10, seconds = 1):
        bin = '10 to 30 minutes'
    elif dt.timedelta(hours = 1) >= datetime_object >= dt.timedelta(minutes = 31):
        bin = '30 to 60 minutes'
    elif dt.timedelta(hours = 2) >= datetime_object >= dt.timedelta(hours = 1, minutes = 1):
        bin = '1 to 2 hours'
    elif dt.timedelta(hours = 5) >= datetime_object >= dt.timedelta(hours = 2, minutes = 1):
        bin = '2 to 5 hours'
    elif dt.timedelta(hours = 10) >= datetime_object >= dt.timedelta(hours = 5, minutes = 1):
        bin = '5 to 10 hours'
    elif dt.timedelta(hours = 15) >= datetime_object >= dt.timedelta(hours = 10, minutes = 1):
        bin = '10 to 15 hours'
    elif dt.timedelta(hours = 24) >= datetime_object >= dt.timedelta(hours = 15, minutes = 1):
        bin = '15 to 24 hours'
    elif datetime_object >= dt.timedelta(hours = 24, minutes = 1):
        bin = 'More than 1 day'
    else:
        bin = 'Less than 1 minute'
    return bin