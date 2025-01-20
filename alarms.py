import requests
from typing import Dict
from .firewalla import BaseFirewallaSDK

class Alarms(BaseFirewallaSDK):
    def get_all_alarms(self, **kwargs):
        return self.__get("alarms", params={
                              "query": None, 
                              "groupBy": None, 
                              "sortBy": None, 
                              "limit": None, 
                              "cursor": None })
