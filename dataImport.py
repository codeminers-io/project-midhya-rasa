#!/usr/bin/python

hostname = 'ec2-54-243-198-191.compute-1.amazonaws.com'
username = 'nhfpgoiwhzrekw'
password = 'e2773b491671c7f91f561c94c665a98586fef404eef9e7884d48e5d43a11ac59'
database = 'dcsjh104da15vj'

# Simple routine to run a query on a database and print the results:
def doQuery(conn) :
    cur = conn.cursor()

    cur.execute('CREATE TABLE "receipts" (ministry_department_state varchar,total_receipts integer,total_disposal integer, total_pending integer,pending_more_than_1_year integer,pending_between_6_to_12_months integer,pending_between_2_to_6_months integer,pending_less_than_2_months integer);')

import psycopg2
myConnection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
doQuery(myConnection)
myConnection.close()