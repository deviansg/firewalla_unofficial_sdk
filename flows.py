import base64
from typing import Dict, TypeAlias
from .firewalla import BaseFirewallaSDK

Pagination: TypeAlias = Dict[str, str, str]

class Flows(BaseFirewallaSDK):
    
    def __init__(self, api_key, domain):
        super().__init__(api_key, domain)
        self.paginated_results = []
    
    def get_flows(self, params: Dict = None):
        if params is None:
            params = {
                "query": None, "groupBy": None, "sortBy": None, "limit": None,
                "paginate": {"enable": False, "limit": 10, "cursor": None}
            }
        
        results = self.__get("flows", params=params)
        self.paginated_results.extend(results.get("data", []))
        next_cursor = results.get("next_cursor")
        
        if next_cursor:
            try:
                next_cursor = base64.b64decode(next_cursor).decode('utf-8')
            except (base64.binascii.Error, UnicodeDecodeError):
                pass
            
            if params["paginate"]["enable"]:
                params["paginate"]["cursor"] = next_cursor
                return self.get_flows(params=params)
        
        return self.paginated_results
    