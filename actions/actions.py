# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from unidecode import unidecode
from rasa_sdk.events import EventType, SlotSet
import requests
from email.mime.text import MIMEText
import json
import smtplib
from email.mime.multipart import MIMEMultipart



class ActionSubmit(Action):
    def name(self) -> Text:
        return "action_submit"

    def run(
        self,
        dispatcher,
        tracker: Tracker,
        domain: "DomainDict"
    ) -> List[Dict[Text, Any]]:

        SendEmail(
            tracker.get_slot("email"),tracker.get_slot("message")
        )

        dispatcher.utter_message("Cảm ơn bạn đã gửi câu hỏi cho tổ tư vấn, tư vấn viên sẽ xem xét và trả lời câu hỏi của bạn sớm nhất có thể.")
        return []

def SendEmail(email,message):
    fromaddr = 'evnchatbot@gmail.com'
    msg = MIMEMultipart()
    toaddr = 'evnchatbot@gmail.com'

    msg['To'] = "evnchatbot@gmail.com"
    msg['Subject'] = "EVN - QUESTION FROM: " + email
    body = message
    msg.attach(MIMEText(body, 'plain'))
    
    s = smtplib.SMTP('smtp.gmail.com', 587)

    s.starttls()

    try:
       # password here
        s.login(fromaddr, "icommvietnam")
        text = msg.as_string()
        s.sendmail(fromaddr, toaddr, text)
    except:
        print("Error")
    finally:
        s.quit()



class Specifier(Action):

    def name(self) -> Text:
        return 'action_specifier'

    def run(self,dispatcher: CollectingDispatcher,tracker: Tracker,domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        tra_cuu = ['tra cuu']  
        bac_1 = ['bac 1']
        bac_2 = ['bac 2']
        bac_3 = ['bac 3']
        phan_nan = ['cao the', 'doc quyen', 'toi te', 'ngu dot', 'ngu', 'khong nhan duoc thong bao', 'doc ton', 'qua cao']

        id_user = tracker.sender_id
        f = open("user_database.txt", "a")
        f.write(id_user+"\n")
        f.close()


        user_input = unidecode(tracker.latest_message.get('text')).lower()
        print(user_input)
        intent = tracker.latest_message['intent'].get('name')
        ogintent = intent

        if any(map(user_input.__contains__, tra_cuu)):
           intent = "utter_tra_cuu_thong_tin"
        elif any(map(user_input.__contains__, phan_nan)):
           intent = "utter_xin_loi"
        else :
           intent = "utter_" + ogintent
        if(user_input.find('https') != -1) or ((user_input.find('hhtps') != -1)):
           intent = "utter_emotes"
        print(tracker.latest_message)   
        print(intent)
        try:
         dispatcher.utter_message(template=intent)
        except:
         dispatcher.utter_message(template="utter_"+ogintent)
        return []

