# StatusMessage is a message that is used to report the status of an agent

from prompits.AgentAddress import AgentAddress
from prompits.Message import Message

class StatusMessage(Message):
    def __init__(self, status: str, message: str, sender: AgentAddress, recipients: list[AgentAddress]):
        super().__init__(type="StatusMessage", 
                         body={"status": status, "message": message},
                         sender=sender,
                         recipients=recipients)