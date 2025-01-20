from typing import Dict
from .firewalla import BaseFirewallaSDK

class Trends(BaseFirewallaSDK):
    def get_trends(self, **kwargs):
        return self.__get("trends/flows", params={"group": None})
    
    def get_alarms(self, **kwargs):
        return self.__get("trends/alarms", params={"group": None})
    
    def get_rules(self, **kwargs):
        return self.__get("trends/rules", params={"group": None})