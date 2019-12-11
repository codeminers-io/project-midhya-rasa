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

with open('/workdir/dataset/NodalOfficer_Details.csv', encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count > 0 and line_count <= 5000:
            myConnection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
            doQuery(myConnection, 'INSERT INTO \"nodal_officer_details\" (apex_ministry_dept_state,parent_of_organisation,org_code,org_name,contact_address1,contact_address2,contact_address3,pincode,pg_officer_desig,organisation_levels) VALUES (\'' + row[0] + '\',\'' + row[1] + '\', \'' + row[2] + '\', \'' + row[3] + '\', \'' + row[4] + '\', \'' + row[5] + '\', \'' + row[6] + '\', \'' + row[7] + '\',\'' + row[8] + '\',\'' + row[9] + '\');')
            myConnection.close()
            print(f'Processing {line_count}')
            
        line_count += 1
    
    print(f'Processed {line_count} lines.')
