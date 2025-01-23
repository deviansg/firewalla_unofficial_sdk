from typing import Dict
from classes.base import BaseFirewallaSDK

class Alarms(BaseFirewallaSDK):
    def get_alarms(self):
        return self._get("alarms", params={"query": None, "groupBy": None, "sortBy": None, "limit": None, "cursor": None })

    def get_alarm(self, box_id: str, alarm_id: str):
        return self._get("alarms", params={"gid": box_id, "aid": alarm_id})
    
    def delete_alarm(self, box_id: str, alarm_id: str):
        return self._delete("alarms", params={"gid": box_id, "aid": alarm_id})