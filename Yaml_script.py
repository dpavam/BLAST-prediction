# -*- coding: utf-8 -*-
"""
Created on Sat Jun 11 16:51:23 2022

Script to process job.yaml files from SequenceServer 2.0.0.

@author: dpava
"""

# imports 
from pathlib import Path
import pandas as pd
from YSF import *

# Dataframe to store data from all jobs
df = pd.DataFrame()


# Assiging file directory adapted from: https://www.geeksforgeeks.org/how-to-iterate-over-files-in-directory-using-python/
# Directory assignment
directory = './Jobs/'

# Assign path and file type in the directory
files = Path(directory).glob('*.yaml')

# Iterate over files in the job folder
for file in files:
    data = open_file(file)
    
    ### Data processing ###
    
    # Job dictionary to store all information
    job = {}
    
    
    ### Extract: id, method, type, num_threads, query_length, start time, end time, and database length
    
    # File has multiple id's, this is used to stop after the first one (main one)
    has_id = False
    
    # Each if statement looks for a different paramenter in the file.
    for i in data:
        #Finds the id of the job, stops at the first one
        if ('id:' in i) and (has_id==False) :
            idn = i.replace('id: ','')
            has_id = True
            continue
        elif 'method:' in i:
            method = i.replace('method: ','')
            continue
        elif 'type:' in i:
            tipo = i.replace('type: ','')
            continue
        elif 'num_threads:' in i:
            num_threads = int(i.replace('num_threads: ',''))
            print(num_threads)
            continue
        elif 'query_length:' in i:
            query_length = int(i.replace('query_length: ',''))
            continue
        elif 'submitted_at' in i:
            start = i.replace('submitted_at: ','')
            continue
        elif 'completed_at' in i:
            end = i.replace('completed_at: ','')
            continue
        elif 'databases_ncharacters_total:' in i:
            databases_ncharacters = int(i.replace('databases_ncharacters_total: ',''))
            break
        
    # Assing extracted values to the job dictionary
    
    job['id'] = idn
    job['method'] = method
    job['type'] = tipo
    job['nsequences'] = total_sequences(data)
    job['num_threads']= num_threads
    job['query_length']=query_length
    job['databases_ncharacters_total']=databases_ncharacters
    job['duration'] = job_duration(start,end)[1]
    job['duration_window'] = duration_bins(job_duration(start,end)[0])
    print(job)
    
    ### Assigning job to the dataframe:
        
    # Temporary df from dictionary --> dataframe
    temp_df = pd.DataFrame([job])
    # Concatenate master df with temporary dataframe
    df = pd.concat([df,temp_df],ignore_index = True)
    print(df)

# Exporting file as a tsv
#df.to_csv('jobs.tsv', sep='\t')