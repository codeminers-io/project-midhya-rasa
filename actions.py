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

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import psycopg2

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

        resultString = 'These are the top 5 departments under Government of India.'
        for result in results:
            resultString = resultString + '</ br>' + result[0]

        dispatcher.utter_message(resultString)

        return []
