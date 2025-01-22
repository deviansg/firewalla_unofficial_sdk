from typing import Literal, Dict
from classes.base import BaseFirewallaSDK

class TargetLists(BaseFirewallaSDK):
    def get_target_lists(self):
        return self.__get("target-lists")

    def get_target_list(self, id=None):
        return self.__get("target-lists", identifier=id)
    
    def create_target_list(self, name: str = None, targets: list = [], 
                           owner: str = None, category: str = None, notes: str = None):
        return self.__post(json={"name": name, "targets": targets, owner: owner, category: category, notes: notes})
    
    def update_target_list(self, id: int):
        return self.__put("target-lists", identifier=id)
    
    def delete_target_list(self, id: int):
        return self.__delete("target-lists", identifier=id)