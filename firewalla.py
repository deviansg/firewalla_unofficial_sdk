from classes.base import BaseFirewallaSDK
from classes.alarms import Alarms
from classes.boxes import Boxes
from classes.devices import Devices
from classes.flows import Flows
from classes.target_lists import TargetLists
from classes.trends import Trends

class Firewalla():
    
    def __init__(self, api_key, firewalla_msp_subdomain):
        self.api_key = api_key
        self.firewalla_msp_subdomain = firewalla_msp_subdomain
    
    def target_lists(self):
        return TargetLists(self.api_key, self.firewalla_msp_subdomain)
    
    def flows(self):
        return Flows(self.api_key, self.firewalla_msp_subdomain)
    
    def alarms(self):
        return Alarms(self.api_key, self.firewalla_msp_subdomain)
    
    def devices(self):
        return Devices(self.api_key, self.firewalla_msp_subdomain)
    
    def boxes(self):
        return Boxes(self.api_key, self.firewalla_msp_subdomain)
    
    def trends(self):
        return Trends(self.api_key, self.firewalla_msp_subdomain)
