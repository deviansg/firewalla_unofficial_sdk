import requests
from typing import Literal, Dict
from .firewalla import BaseFirewallaSDK

RulesQuery = Literal["group", "limit"]
EndpointTypes = Literal["pause", "resume"]

class Rules(BaseFirewallaSDK):
    def __post_rules(self, endpoint: EndpointTypes, id: int, query: RulesQuery):
        headers = self._get_headers()
        url = f"{self.domain}/{self.api_version}/boxes/{id}/{endpoint}"
        response = requests.post(url, headers=headers, json={"id": id}, params=query)
        response.raise_for_status()
        return response.json()
    
    def pause_rules(self, id: int, query: RulesQuery):
        return self.__post_rules("pause", id, query=query)
    
    def resume_rules(self, id: int, query: RulesQuery):
        return self.__post_rules("resume", id, query=query)
