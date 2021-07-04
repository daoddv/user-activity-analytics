# connect with server

from typing import Dict

import pyodbc

import pandas as pd

import time

from datetime import datetime

from csv import DictWriter

 

# Some other example server values are

# server = 'localhost\sqlexpress' # for a named instance

# server = 'myserver,port' # to specify an alternate port

server = 'assc-kl-gh.database.windows.net'

database = 'ltu-assc-gh-db'

username = 'analytics'

password = 'internship_2021'

cnxn = pyodbc.connect(

    'DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)

cursor = cnxn.cursor()

 

# start overall time clock

# first we will check overall time taken to run all the sequence, then we will use individual processes like Login etc

start = time.time()

 

# function created to recall the table(s)

# create an additional column called table and add all the table names in the row for each entry

def cloud(table):

    sql = pd.read_sql_query('SELECT * FROM "' + table + '"', cnxn)

    sql[['table_name']] = str(table)

    return sql

 

# list all the table names

table_list = ["csv_azure_terminate", "csv_azure_background", "csv_azure_article-access", "csv_azure_app-removed",

              "csv_azure_back-button-pressed", "clinician_list", "antenatal_list", "csv_azure_tool-access",

              "csv_azure_topic-access", "csv_azure_external-url", "csv_azure_foreground", "csv_azure_login",

              "csv_azure_forum-access", "csv_azure_new-post", "csv_azure_pn-access", "csv_azure_post-deleted",

              "csv_azure_post-liked", "csv_azure_post-reported", "csv_azure_terminate", "csv_azure_tool-access",

              "csv_azure_topic-access", "csv_azure_video-watched"]

 

list_of_dataframes = []

for df_azure1 in table_list:

    list_of_dataframes.append(cloud(df_azure1))

 

merged_df_azure1 = pd.concat(list_of_dataframes)

 

# Current Time Constructor and File Name Descriptor

now = datetime.now()

print(merged_df_azure1)

_path_csv = "C:/test/"

_filename = "export.csv"

_fullpath = _path_csv + now.strftime("%m-%d-%y--%H-%M-%S") + _filename

header = ["email", "date", "time", "device_type", "table_name"]

 

#change the file name to a local folders on server it sits on

merged_df_azure1.to_csv(_fullpath, columns=header)

 

#########################################################################-Exec-########################################################################

#will save the time taken to execute this bit of program

end = time.time()

# Time counter in Seconds

_total_exec_time = int(end - start)

_ts = now.strftime("%d-%m-%y--%H-%M-%S")

# Define a struct for the timestamp, convert to pandas dataframe

_dict_exec_time = {

    'run_datetime': _total_exec_time,

    'exec_time': _ts

}

# Create the CSV Consturctor, change here if you want to log more things

field_name = ['run_datetime','exec_time']

 

with open('mybabynow_log.csv','a') as f_object:

    DictWriter_object = DictWriter(f_object,fieldnames=field_name)

    DictWriter_object.writerow(_dict_exec_time)

    f_object.close()