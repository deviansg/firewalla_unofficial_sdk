from classes.base import BaseFirewallaSDK

class Boxes(BaseFirewallaSDK):
    def get_boxes(self, group: int = None):
        return self._get("boxes", params={"group": group})