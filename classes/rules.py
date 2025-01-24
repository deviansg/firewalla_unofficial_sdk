from classes.base import BaseFirewallaSDK

class Rules(BaseFirewallaSDK):    
    def pause_rule(self, id: str) -> str:
        return self._post(f"rules/{id}/pause")
    
    def resume_rule(self, id: str) -> str:
        return self._post(f"rules/{id}/resume")
