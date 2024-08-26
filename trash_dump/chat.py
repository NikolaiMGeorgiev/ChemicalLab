import time

class ChatMessage:
    def __init__(self, content):
        self.content = content
        self.sent_time = time.time()
        self.read_status = False

class PeerToPeerChat:
    def __init__(self):
        self.messages = []

    def send_message(self, content):
        message = ChatMessage(content)
        self.messages.append(message)

    def mark_message_as_read(self, index):
        if index < len(self.messages):
            self.messages[index].read_status = True

    def get_unread_messages(self):
        unread_messages = []
        for message in self.messages:
            if not message.read_status:
                unread_messages.append(message)
        return unread_messages

# Example usage
chat = PeerToPeerChat()
chat.send_message("Hello!")
chat.send_message("How are you?")
chat.mark_message_as_read(0)

unread_messages = chat.get_unread_messages()
for message in unread_messages:
    print(f"Message: {message.content}")
    print(f"Sent Time: {message.sent_time}")
    print(f"Read Status: {message.read_status}")