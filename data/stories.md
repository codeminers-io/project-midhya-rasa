## happy path
* greet
  - utter_greet
* mood_great
  - utter_happy

## sad path 1
* greet
  - utter_greet
* mood_unhappy
  - utter_cheer_up
  - utter_did_that_help
* affirm
  - utter_happy

## sad path 2
* greet
  - utter_greet
* mood_unhappy
  - utter_cheer_up
  - utter_did_that_help
* deny
  - utter_goodbye

## say goodbye
* goodbye
  - utter_goodbye

## bot challenge
* bot_challenge
  - utter_iamabot

## bot location
* bot_location
  - utter_location

## bot age
* bot_location
  - utter_age

## bot asl
* bot_asl
  - utter_asl

## bot language
* bot_language
  - utter_language

## bot help
* bot_help
  - utter_help

## bot state
* bot_state
  - utter_state

## bot hobby
* bot_hobby
  - utter_hobby
  
## list departments
* list_departments
  - action_list_departments
