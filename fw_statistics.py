import requests

from typing import Literal, TypeAlias, Dict
from .firewalla import BaseFirewallaSDK, set_type

FlowType: TypeAlias = Literal["topBoxesByBlockedFlows", "topBoxesBySecurityAlarms", "topRegionsByBlockedFlows"]

class Statistics(BaseFirewallaSDK):

    def __init__(self, api_key: str, domain: str):
        super().__init__(api_key, domain)
        self.url = None
   
    def get_stats(self, params: Dict = {"group": None, "limit": 5}, type: FlowType=None):
        query_params = ["group", "limit"]
        for key, value in params.items():
            if key in query_params:
                params[key] = value
        return self.__get("stats", params=params, type=type)