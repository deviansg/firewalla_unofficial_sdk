from typing import Dict, TypeAlias
from classes.base import BaseFirewallaSDK

class Flows(BaseFirewallaSDK):
    
    def get_flows(self, params: Dict = {"query": None, "groupBy": None, "sortBy": None, "limit": None, "cursor": None}):
        return self._get("flows", params=params)
            