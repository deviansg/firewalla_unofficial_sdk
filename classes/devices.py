from classes.base import BaseFirewallaSDK

class Devices(BaseFirewallaSDK):
    def get_devices(self, box: int = None, group: str = None):
        return super()._get("devices", params={"box": box, "group": group})