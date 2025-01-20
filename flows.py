from typing import Dict
from .firewalla import BaseFirewallaSDK

class Flows(BaseFirewallaSDK):
    def get_flows(self, **kwargs):
        params: Dict[str,str,str,int,str] = {"query": None, "groupBy": None, "sortBy": None, "limit": None, "cursor": None}
        for key, value in kwargs.items():
            if key in params:
                params[key] = value
        return self.__get("flows", params=params)
    