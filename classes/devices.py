from classes.base import BaseFirewallaSDK

class Devices(BaseFirewallaSDK):
    
    def __init__(self, api_key: str, firewalla_msp_subdomain: str):
        super().__init__(api_key, firewalla_msp_subdomain)
    
    def get_devices(self, box: int = None, group: str = None):
        return super()._get("devices", params={"box": box, "group": group})