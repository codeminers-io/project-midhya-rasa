# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

hostname = 'ec2-54-243-198-191.compute-1.amazonaws.com'
username = 'nhfpgoiwhzrekw'
password = 'e2773b491671c7f91f561c94c665a98586fef404eef9e7884d48e5d43a11ac59'
database = 'dcsjh104da15vj'

#hostname = 'localhost'
#username = 'postgres'
#password = 'Schroders123'
#database = 'postgres'

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import psycopg2
from datetime import datetime
from dateutil import tz
from rasa_sdk.forms import FormAction
from typing import Dict, Text, Any, List, Union, Optional
import json

class ActionListDepartments(Action):
    def name(self) -> Text:
        return "action_list_departments"
        
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        print(tracker.latest_message['entities'])

        con = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
        cur = con.cursor()
        cur.execute('SELECT DISTINCT apex_ministry_dept_state FROM nodal_officer_details LIMIT 5')
        results = cur.fetchall()

        cur.close()
        con.close()

        delimiter = '\n'
        resultString = delimiter.join([result[0] for result in results])

        dispatcher.utter_message(template="utter_list_departments", departments=resultString)

        return []

class ActionBotDate(Action):
    def name(self) -> Text:
        return "action_bot_date"
        
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        from_zone = tz.gettz('UTC')
        to_zone = tz.gettz('Asia/Kolkata')

        utc = datetime.utcnow()

        utc = utc.replace(tzinfo=from_zone)

        date = utc.astimezone(to_zone).strftime("%b %d, %Y")

        dispatcher.utter_message(template="utter_bot_date", indiaDate=date)

        return []

class ActionBotTime(Action):
    def name(self) -> Text:
        return "action_bot_time"
        
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        from_zone = tz.gettz('UTC')
        to_zone = tz.gettz('Asia/Kolkata')

        utc = datetime.utcnow()

        utc = utc.replace(tzinfo=from_zone)

        time = utc.astimezone(to_zone).strftime("%b %d, %Y %H:%M:%S %p")

        dispatcher.utter_message(template="utter_bot_time", indiaTime=time)

        return []

class OrganizationForm(FormAction):
    def name(self) -> Text:

        return "organization_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:

        return ["organization"]

    def slot_mappings(self) -> Dict[Text, Union[Dict, List[Dict]]]:

        return {
            "organization": [self.from_entity(entity="organization"), self.from_text()]
        }

    def submit(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict]:

        intent = tracker.latest_message['intent'].get('name')
        value = tracker.get_slot('organization').lower()

        if intent == 'parent_organization':
            con = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
            cur = con.cursor()
            cur.execute('SELECT org_code, org_name, parent_of_organisation, apex_ministry_dept_state FROM nodal_officer_details WHERE LOWER(org_code) LIKE \'%' + value + '%\' OR LOWER(org_name) LIKE \'%' + value + '%\'')
            results = cur.fetchall()

            cur.close()
            con.close()

            if(len(results) != 0):
                delimiter = '\n\n'
                resultString = delimiter.join(['Organization: ' + str(result[1]) + ' (' + str(result[0]) +  ')' + '\n' + 'Parent: ' + str(result[2]) + '\n' + 'Ministry/Department/State: ' + str(result[3]) for result in results])

                dispatcher.utter_message(template="utter_about_organization", organization_details=resultString)
            else:
                dispatcher.utter_message(template="utter_organization_not_found", organization=value)
        elif intent == 'child_organizations':
            con = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
            cur = con.cursor()
            cur.execute('SELECT org_code, org_name, parent_of_organisation, apex_ministry_dept_state FROM nodal_officer_details WHERE LOWER(parent_of_organisation) LIKE \'%' + value + '%\'')
            results = cur.fetchall()

            cur.close()
            con.close()

            if(len(results) != 0):
                delimiter = '\n\n'
                resultString = delimiter.join(['Organization: ' + str(result[1]) + ' (' + str(result[0]) +  ')' + '\n' + 'Parent: ' + str(result[2]) + '\n' + 'Ministry/Department/State: ' + str(result[3]) for result in results])

                dispatcher.utter_message(template="utter_about_organization", organization_details=resultString)
            else:
                dispatcher.utter_message(template="utter_organization_not_found", organization=value)

        else:
            con = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
            cur = con.cursor()
            cur.execute('SELECT org_code, org_name, parent_of_organisation, apex_ministry_dept_state, contact_address1, contact_address2, contact_address3 FROM nodal_officer_details WHERE LOWER(org_code) LIKE \'%' + value + '%\' OR LOWER(org_name) LIKE \'%' + value + '%\'')
            results = cur.fetchall()

            cur.close()
            con.close()

            if(len(results) != 0):
                delimiter = '\n\n'
                resultString = delimiter.join(['Organization: ' + str(result[1]) + ' (' + str(result[0]) +  ')' + '\n' + 'Parent: ' + str(result[2]) + '\n' + 'Ministry/Department/State: ' + str(result[3]) + '\n' + 'Address: ' + str(result[4]) + '\n' + str(result[5]) + '\n' + str(result[6]) for result in results])

                dispatcher.utter_message(template="utter_about_organization", organization_details=resultString)
            else:
                dispatcher.utter_message(template="utter_organization_not_found", organization=value)

        return []

class ActionComplaintsCount(Action):
    def name(self) -> Text:
        return "action_complaints_count"
        
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        status = next(tracker.get_latest_entity_values("status"), None)
        organization = next(tracker.get_latest_entity_values("organization"), None)
        time = next(tracker.get_latest_entity_values("time"), None)
        duration = next((e for e in tracker.latest_message["entities"] if e['entity'] == 'duration'), None)

        print(duration)

        sql = "SELECT SUM(h.Recetpts), SUM(h.Disposals), SUM(h.Recetpts) - SUM(h.Disposals) FROM receipts_history h INNER JOIN nodal_officer_details n ON h.org_name = n.org_name WHERE 1 = 1"

        if organization != None:
            sql+= " AND (LOWER(n.org_code) =\'" + organization.lower() + "\' OR LOWER(h.org_name) = \'" + organization.lower() + "\')"
        elif time != None:
            if time["from"] != None and time["from"] != None:
                sql+= " AND ((year::text || LPAD(month::text, 2, '0')::date BETWEEN \'" + time["from"] + "\' AND \'" + time["to"] + "\')"
            elif time["from"] != None and time["to"] == None:
                sql+= " AND ((year::text || LPAD(month::text, 2, '0') || \'01\')::timestamp > \'" + time["from"] + "\'::timestamp)"
            elif time["from"] == None and time["to"] != None:
                sql+= " AND ((year::text || LPAD(month::text, 2, '0') || \'01\')::timestamp < \'" + time["to"] + "\'::timestamp)"
        elif duration != None:
            sql+= " AND ((DATE_PART(\'day\', now()::timestamp - (year::text || LPAD(month::text, 2, \'0\') || '01 00:00:00' )::timestamp) * 24 + DATE_PART(\'hour\',now()::timestamp -  (year::text || LPAD(month::text, 2, \'0\') || '01 00:00:00' )::timestamp)) * 60 + DATE_PART(\'minute\', now()::timestamp - (year::text || LPAD(month::text, 2, \'0\') || '01 00:00:00' )::timestamp)) * 60 + DATE_PART(\'second\', now()::timestamp - (year::text || LPAD(month::text, 2, \'0\') || '01 00:00:00' )::timestamp) > " + str(duration["additional_info"]["normalized"]["value"])

        print(sql)

        con = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
        cur = con.cursor()
        cur.execute(sql)
        results = cur.fetchall()

        if(len(results) != 0):
            if status != None and status.lower() == 'pending':
                desc = 'Total Pending: ' + str(results[0][2])
                dispatcher.utter_message(template="utter_complaints_count", description=desc)
            elif status != None and status.lower() == 'resolved':
                desc = 'Total Resolved: ' + str(results[0][1])
                dispatcher.utter_message(template="utter_complaints_count", description=desc)
            elif status != None and status.lower() == 'registered':
                desc = 'Total Receipts: ' + str(results[0][0])
                dispatcher.utter_message(template="utter_complaints_count", description=desc)
            else:
                desc = 'Total Receipts: ' + str(results[0][0])
                desc = 'Total Resolved: ' + str(results[0][1])
                desc = 'Total Pending: ' + str(results[0][2])
                dispatcher.utter_message(template="utter_complaints_count", description=desc)
            
        else:
            dispatcher.utter_message(template="utter_default")

        return []
