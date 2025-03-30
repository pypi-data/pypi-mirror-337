import time
import requests

class Discord():

    # This shit will hurt so much 
    @staticmethod

    def spam(message, delay, webhook, amount):

        counter = 0

        spam_payload = {
            "content": message,
            "username": "Discord_spammer"
        }
        try:
            for i in range(amount):
                req = requests.post(webhook, json=spam_payload)
                counter += 1
                print(f"Spammed messages: {counter}")
                time.sleep(delay)
        
        except:
            print("An error occured with some of the parameters, please enter them correctly!")
    
    @staticmethod
    def send(message, webhook):

        payload = {
            "content": message
        }
        try:
            req = requests.post(webhook, json=payload)
        except:
            print("Please enter every parameter correctly!")

    @staticmethod
    def delete_webhook(webhook):
        try:
            req = requests.delete(webhook)
        except:
            print("Invalid webhook, please enter a correct one!")
    
    def fetch_whdata(webhook):
        try:
            req = requests.get(webhook)

            data = req.json()

            final_data = f"""
Application ID: {data.get("application_id")}
Avatar: {data.get("avatar")}
Channel ID: {data.get("channel_id")}
Guild ID: {data.get("guild_id")}
ID: {data.get("id")}
Name: {data.get("name")}
Type: {data.get("type")}
Token: {data.get("token")}
URL: {data.get("url")}
"""

            print(final_data)

        except:
            print("Some error occured, please enter every parameter correctly!")