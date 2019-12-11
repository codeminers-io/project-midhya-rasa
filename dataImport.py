#!/usr/bin/python

hostname = 'ec2-54-243-198-191.compute-1.amazonaws.com'
username = 'nhfpgoiwhzrekw'
password = 'e2773b491671c7f91f561c94c665a98586fef404eef9e7884d48e5d43a11ac59'
database = 'dcsjh104da15vj'

def doQuery(conn) :
    print('Inside doQuery')
    cur = conn.cursor()

    cur.execute('CREATE TABLE "nodal_officer_details" (apex_ministry_dept_state varchar,parent_of_organisation varchar,org_code varchar,org_name varchar,contact_address1 varchar,contact_address2 varchar,contact_address3 varchar,pincode varchar,pg_officer_desig varchar,organisation_levels smallint);')
    print('Completed create table1')
    
    cur.execute('CREATE TABLE "receipts_history" (org_name varchar,year integer,month integer,recetpts integer,disposals integer);')
    print('Completed create table2')
    cur.close()
    conn.commit()
    print('Completed')

import psycopg2
myConnection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
doQuery(myConnection)
myConnection.close()
