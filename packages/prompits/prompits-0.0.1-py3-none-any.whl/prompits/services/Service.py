# Service is a Pit that can be used by agents to perform actions
# Service has an owner, who is the agent that created the service
# Service may have a pool, which is the pool of agents that can use the service
# Service may have tables, which are the tables of the service

from prompits.Pit import Pit

class Service(Pit):
    def __init__(self, name, description):
        super().__init__(name, description)
 

