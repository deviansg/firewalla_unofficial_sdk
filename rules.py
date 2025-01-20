import requests
from typing import Literal, Dict
from .firewalla import BaseFirewallaSDK

Query = Literal["group", "limit"]

class Rules(BaseFirewallaSDK):
    def __init__(self, api_key, domain):
        super().__init__(api_key, domain)

    def __post_rules(self, endpoint: Literal["pause", "resume"], id: int, query: Query):
        headers = self._get_headers()
        url = f"{self.domain}/{self.api_version}/boxes/{id}/{endpoint}"
        response = requests.post(url, headers=headers, json={"id": id}, params=query)
        response.raise_for_status()
        return response.json()
    
    def pause_rules(self, id: int, query: Query):
        return self.__post_rules("pause", id, query=query)
    
    def resume_rules(self, id: int, query: Query):
        return self.__post_rules("resume", id, query=query)
