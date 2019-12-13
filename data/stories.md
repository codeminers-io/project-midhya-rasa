## happy path
* greet
  - utter_greet
* mood_great
  - utter_happy

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
* bot_age
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

## bot likes
* bot_likes
  - utter_bot_likes

## bot date
* bot_date
  - action_bot_date

## bot time
* bot_time
  - action_bot_time
  
## list departments
* list_departments
  - action_list_departments
* affirm
  - action_list_departments

## list departments
* list_departments
  - action_list_departments
* deny
  - utter_ok

## parent organization
* parent_organization
  - organization_form
  - slot{"organization": "darpg"}
  - form{"name": "organization_form"}
  - form{"name": null}

## child organization
* child_organizations
  - organization_form
  - slot{"organization": "darpg"}
  - form{"name": "organization_form"}
  - form{"name": null}

## about organization address
* organization_address
  - organization_form
  - slot{"organization": "darpg"}
  - form{"name": "organization_form"}
  - form{"name": null}

## user info
* user_info
  - utter_user_info
