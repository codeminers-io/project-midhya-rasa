#!/usr/bin/python

hostname = 'ec2-54-243-198-191.compute-1.amazonaws.com'
username = 'nhfpgoiwhzrekw'
password = 'e2773b491671c7f91f561c94c665a98586fef404eef9e7884d48e5d43a11ac59'
database = 'dcsjh104da15vj'

# Simple routine to run a query on a database and print the results:
def doQuery(conn, query) :
    cur = conn.cursor()
    cur.execute(query)
    conn.commit()
    cur.close()

import psycopg2
import csv

with open('/workdir/dataset/4.csv', encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count > 0 and line_count < 4000:
            myConnection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
            doQuery(myConnection, 'INSERT INTO \"receipts\" (ministry_department_state,total_receipts,total_disposal, total_pending,pending_more_than_1_year,pending_between_6_to_12_months,pending_between_2_to_6_months,pending_less_than_2_months) VALUES (\'' + row[0] + '\',\'' + row[1] + '\', \'' + row[2] + '\', \'' + row[3] + '\', \'' + row[4] + '\', \'' + row[5] + '\', \'' + row[6] + '\', \'' + row[7] + '\');')
            myConnection.close()
            print(f'Processing {line_count}')
            
        line_count += 1
    
    print(f'Processed {line_count} lines.')
    
with open('/workdir/dataset/3.csv', encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count > 0 and line_count < 4000:
            myConnection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
            doQuery(myConnection, 'INSERT INTO \"receipts_history\" (org_name,\"year\",\"month\",recetpts,disposals) VALUES (\'' + row[0] + '\',\'' + row[1] + '\', \'' + row[2] + '\', \'' + row[3] + '\', \'' + row[4] + '\');')
            myConnection.close()
            print(f'Processing {line_count}')
            
        line_count += 1
    
    print(f'Processed {line_count} lines.')

