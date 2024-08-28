import time
import requests
import json
from flask import jsonify


class Message:
    def __init__(self, content, sender, index):
        self.index = index
        self.content = content
        self.sender = sender
        self.sent_time = time.time()


class Chat:
    def __init__(self, db, user_id, user_type):
        self.messages = []
        self.db = db
        self.user_id = user_id
        self.user_type = user_type
        self.messages_index = 0
        
    def wait_for_vendor(self):
        response = requests.get(f"http://localhost:12345/new_chat?user_id={self.user_id}")
        response_data = response.json()
        if not "status" in response_data or response_data["status"] != "OK":
            print("Error creating chat")
            return
        if "chat_id" in response_data:
            self.chat_id = response_data["chat_id"]
            self.counterparty = response_data["vendor_id"]
            return True
        else:
            print("No active vendors at the moment. Try again later.")
            return False

    def wait_for_user(self):
        response = requests.get(f"http://localhost:12345/start_chat?chat_id={self.chat_id}")
        response_data = response.json()
        if not "status" in response_data or response_data["status"] != "OK":
            print("Error creating chat")
            return
        if response_data["user_id"]:
            self.counterparty = response_data["user_id"]
        else:
            print("...")
            time.sleep(5)
            self.wait_for_user()

    def create_chat(self):
        data = {'vendor_id': self.user_id}
        response = requests.post("http://127.0.0.1:12345/new_chat", json=data)
        response_data = response.json()
        if not "status" in response_data or response_data["status"] != "OK":
            print("Error creating chat")
            return
        self.chat_id = response_data["chat_id"]

    def send_message(self, content):
        data = {'content': content, "user_type": self.user_type, "chat_id": self.chat_id}
        response = requests.post("http://127.0.0.1:12345/message", json=data)
        response_data = response.json()
        if not "status" in response_data or response_data["status"] != "OK":
            print("Error creating chat")
            return
        message = Message(content, self.user_id, self.messages_index)
        self.messages.append(message)
        self.messages_index += 1