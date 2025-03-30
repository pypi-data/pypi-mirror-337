# Message is a class for information interchange between agents
# MEssage is an abstract class
# Message contains type, sent_time, body, attachments, sender, recipients


from datetime import datetime
import json
import uuid
from prompits.AgentAddress import AgentAddress

class Attachment:
    def __init__(self, name: str, content: str):
        self.name = name
        self.content = content

    def ToJson(self):
        return {
            "name": self.name,
            "content": self.content
        }
    def FromJson(self, json_data: dict):
        self.name = json_data["name"]
        self.content = json_data["content"]

class Message:
    def __init__(self, type, body: dict, 
                 sender: AgentAddress, 
                 recipients: list[AgentAddress], attachments: list=[], msg_id=None, sent_time=None):
        self.type = type
        # if msg_id is not provided, generate a new one
        if msg_id is None:
            self.msg_id = str(uuid.uuid4())
        else:
            self.msg_id = msg_id
        self.sent_time = sent_time
        self.body = body
        self.attachments = attachments
        self.sender = sender
        self.recipients = recipients

    # declare variables
    type: str
    msg_id: str
    sent_time: datetime
    body: dict
    attachments: list
    sender: AgentAddress
    recipients: list[AgentAddress]

    def __str__(self):
        return f"Message(type={self.type}, sent_time={self.sent_time}, body={self.body}, attachments={self.attachments})"
    
    def __repr__(self):
        return self.__str__()
    
    def ToJson(self) -> dict:
        # if sender and recipients are AgentAddress objects, convert them to json
        if isinstance(self.sender, AgentAddress):
            sender = self.sender.ToJson()
        recipient_list = []
        if isinstance(self.recipients, list):
            for recipient in self.recipients:
                if isinstance(recipient, AgentAddress):
                    recipient_list.append(recipient.ToJson())
                else:
                    recipient_list.append(recipient)
        elif isinstance(self.recipients, AgentAddress):
            recipient_list.append(self.recipients.ToJson())
        else:
            recipient_list.append(self.recipients)
        attachment_list = []
        if isinstance(self.attachments, list):
            for attachment in self.attachments:
                if isinstance(attachment, Attachment):
                    attachment_list.append(attachment.ToJson())
                else:
                    attachment_list.append(attachment)  
        msg_json = {
            "type": self.type,
            "body": self.body,
            "sender": sender,
            "recipients": recipient_list,
            "msg_id": self.msg_id,
            "sent_time": self.sent_time.isoformat() if self.sent_time else None,
            "attachments": attachment_list
        }
        print(f"Sender: {sender}")
        print(f"Recipients: {recipient_list}")
        print(f"Message.ToJson: {msg_json}")
        #msg_str = json.dumps(msg_json)
        return msg_json
    # static method
    @classmethod
    def FromJson(cls, json_data: dict):
        # msg_type=json_data["type"]
        # create a message object based on the type
        msg = Message(json_data["type"], json_data["body"], json_data["sender"], json_data["recipients"], json_data["msg_id"], json_data["sent_time"])
        msg.FromJson(json_data)
        return msg
    
    # non static method
    def FromJson(self, json_data: dict):
        self.type = json_data["type"]
        self.body = json_data["body"]
        self.sender = AgentAddress.FromJson(json_data["sender"])
        self.recipients = [AgentAddress.FromJson(recipient) for recipient in json_data["recipients"]]
        self.msg_id = json_data["msg_id"]
        self.sent_time = datetime.fromisoformat(json_data["sent_time"]) if json_data["sent_time"] else None
        self.attachments = [attachment for attachment in json_data["attachments"]]
