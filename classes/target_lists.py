from classes.base import BaseFirewallaSDK

class TargetLists(BaseFirewallaSDK):
    def get_target_lists(self):
        return self._get("target-lists")

    def get_target_list(self, id=None):
        return self._get("target-lists", identifier=id)
    
    def create_target_list(self, name: str = None, targets: list = [], 
                           owner: str = None, category: str = None, notes: str = None):
        return self._post(json={"name": name, "targets": targets, owner: owner, category: category, notes: notes})
    
    def update_target_list(self, id: int, name: str = None, targets: list = [], notes: str = None):
        return self._put("target-lists", identifier=id, json={"name": name, "targets": targets, notes: notes})
    
    def delete_target_list(self, id: int):
        return self._delete("target-lists", identifier=id)