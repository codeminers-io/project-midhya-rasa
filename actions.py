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
#password = ''
#database = 'postgres'

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import psycopg2
from datetime import datetime
from dateutil import tz

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

        resultString = '<ol>'

        for result in results:
            resultString = resultString + '<li>' + result[0] + '</li>'
            
        resultString = resultString + '</ol>'

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
