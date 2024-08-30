from math import ceil
import time
import requests

class Message:
    def __init__(self, content, sender):
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
        self.server_addr = "http://localhost:12345"
        
    def wait_for_vendor(self):
        response = requests.get(f"{self.server_addr}/new_chat?user_id={self.user_id}")
        response_data = response.json()
        if not self.validate_response(response_data, "Couldn't create chat"):
            return None
        if "chat_id" in response_data:
            self.chat_id = response_data["chat_id"]
            self.counterparty = response_data["vendor_id"]
            return True
        else:
            print("No active vendors at the moment. Try again later.")
            return False

    def wait_for_user(self):
        response = requests.get(f"{self.server_addr}/start_chat?chat_id={self.chat_id}")
        response_data = response.json()
        if not self.validate_response(response_data, "Couldn't start chat"):
            return
        if "user_id" in response_data and response_data["user_id"]:
            self.counterparty = response_data["user_id"]
        else:
            time.sleep(5)
            self.wait_for_user()

    def create_chat(self):
        data = {'vendor_id': self.user_id}
        response = requests.post(f"{self.server_addr}/new_chat", json=data)
        response_data = response.json()
        if not self.validate_response(response_data, "Couldn't start chat"):
            return
        self.chat_id = response_data["chat_id"]

    def send_message(self, content):
        data = {'content': content, "user_type": self.user_type, "chat_id": self.chat_id, "sender": self.user_type}
        response = requests.post(f"{self.server_addr}/message", json=data)
        response_data = response.json()
        if not self.validate_response(response_data, "Couldn't send message"):
            return
        message = Message(content, self.user_type)
        self.messages.append(message)

    def wait_for_response(self):
        response_data = None
        while not response_data or not "status" in response_data or response_data["status"] != "OK" or not "message" in response_data:
            response = requests.get(f"{self.server_addr}/message?chat_id={self.chat_id}&receiver={self.user_type}")
            response_data = response.json()
            time.sleep(5)
        sender = "vendor" if self.user_type == "user" else "user"
        message = Message(response_data["message"], sender)
        self.messages.append(message)
        return response_data["message"]
    
    def print_messages(self):
        line_width = 100
        message_width = 40
        counterpaty_text = "Vendor: " if self.user_type == "user" else "User: "
        print(" " * int(line_width / 2 - len("Chat") / 2) + "Chat")
        for message in self.messages:
            offset = 0 if message.sender == self.user_type else line_width - message_width
            sender_label = "You: " if message.sender == self.user_type else counterpaty_text
            for i in range(0, ceil(len(message.content) / message_width)):
                sender_label_text = sender_label if i == 0 else " " * len(sender_label)
                start = i * message_width
                end = min((i + 1) * message_width, len(message.content))
                print(" " * offset + sender_label_text + message.content[start:end])
    
    def validate_response(self, response_data, error_message = ""):
        if not "status" in response_data or response_data["status"] != "OK":
            if len(error_message):
                print(error_message)
            return False
        return True