import requests
from typing import Dict
from .firewalla import BaseFirewallaSDK

class Alarms(BaseFirewallaSDK):
    def get_all_alarms(self, **kwargs):
        url = f"{self.domain}/{self.api_version}/alarms"
        headers = self.__get_headers()
        params: Dict[str,str,str,int,str] = {"query": None, "groupBy": None, "sortBy": None, "limit": None, "cursor": None}
        for key, value in kwargs.items():
            if key in params:
                params[key] = value
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()