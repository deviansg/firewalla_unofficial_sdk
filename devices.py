import requests
from .firewalla import BaseFirewallaSDK

class Devices(BaseFirewallaSDK):
    def get_devices(self, box: int = None, group: int = None):
        return self.__get("devices", params={"box": box, "group": group})