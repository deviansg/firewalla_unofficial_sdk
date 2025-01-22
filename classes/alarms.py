from typing import Dict
from classes.base import BaseFirewallaSDK

class Alarms(BaseFirewallaSDK):
    def get_all_alarms(self):
        return self.__get("alarms", params={"query": None, "groupBy": None, "sortBy": None, "limit": None, "cursor": None })
