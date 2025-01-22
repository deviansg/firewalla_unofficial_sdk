from typing import Dict
from classes.base import BaseFirewallaSDK

class Alarms(BaseFirewallaSDK):
    def get_alarms(self):
        return self._get("alarms", params={"query": None, "groupBy": None, "sortBy": None, "limit": None, "cursor": None })
