from classes.base import BaseFirewallaSDK

class Trends(BaseFirewallaSDK):
    def get_flows(self, group: int = None):
        return self._get("trends/flows", params={"group": group})
    
    def get_alarms(self, group: int = None):
        return self._get("trends/alarms", params={"group": group})
    
    def get_rules(self, group: int = None):
        return self._get("trends/rules", params={"group": group})