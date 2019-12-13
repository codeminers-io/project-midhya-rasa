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

class ActionListDepartments(Action):
    def name(self) -> Text:
        return "action_list_departments"
        
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

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
        value = tracker.get_slot('organization')

        print(intent)
        print(value)

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
