import requests
from .firewalla import BaseFirewallaSDK

class Boxes(BaseFirewallaSDK):
    def get_boxes(self, group: int = None):
        return self.__get("boxes", params={"group": group})