import base64
import requests
import urllib.parse
from typing import Dict, Union, Literal, TypeAlias, List, Optional

RulesQuery = Literal["group", "limit"]
EndpointTypes = Literal["pause", "resume"]
FlowType: TypeAlias = Literal["topBoxesByBlockedFlows", "topBoxesBySecurityAlarms", "topRegionsByBlockedFlows"]
StatsParams: TypeAlias = Literal["group", "limit"]

class Firewalla:
    
    def __init__(self, api_key: str, firewalla_msp_subdomain: str):
        self.api_key: str = api_key
        self.domain: str = f"https://{firewalla_msp_subdomain}.firewalla.net"
        self.api_version: str = "v2"
        self.url: Optional[str] = None
        self.paginated_results: List[Dict] = []

    def __get_headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Token {self.api_key}",
            "Content-Type": "application/json"
        }

    def __get(self, endpoint: str, params: Optional[Dict] = None, identifier: Optional[Union[int, str]] = None) -> Union[Dict, List]:
        self.url = f"{self.domain}/{self.api_version}/{endpoint}"
        if identifier:
            self.url = f"{self.url}/{identifier}"
        headers = self.__get_headers()
        if params is not None and "query" in params:
            params["query"] = urllib.parse.quote_plus(str(params["query"]))
        response = requests.get(self.url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
                  
        if isinstance(data, dict) and "results" in data:
            self.paginated_results.extend(data.get("results", []))
            next_cursor = data.get("next_cursor")
        
            while next_cursor:
                next_cursor = base64.b64decode(next_cursor).decode('utf-8')
                params["cursor"] = next_cursor
                data = self.__get(endpoint=endpoint, params=params, identifier=identifier)
                self.paginated_results.extend(data.get("results", []))
                next_cursor = data.get("next_cursor")

            return self.paginated_results
        else:
            return data
        
    def __post(self, endpoint: str, json: Optional[Dict] = None) -> Dict:
        headers = self.__get_headers()
        url = f"{self.domain}/{self.api_version}/{endpoint}"
        response = requests.post(url, headers=headers, json=json, timeout=10)
        response.raise_for_status()
        return response.json()
    
    def __put(self, endpoint: str, identifier: Optional[Union[int, str]] = None, json: Optional[Dict] = None) -> Dict:
        headers = self.__get_headers()
        url = f"{self.domain}/{self.api_version}/{endpoint}/{identifier}"
        response = requests.put(url, headers=headers, json=json, timeout=10)
        response.raise_for_status()
        return response.json()
    
    def __delete(self, endpoint: str, identifier: Optional[Union[int, str]] = None, params: Optional[Dict] = None) -> Dict:
        headers = self.__get_headers()
        url = f"{self.domain}/{self.api_version}/{endpoint}/{identifier}"
        response = requests.delete(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()

    def __post_rules(self, endpoint: EndpointTypes, id: int, query: RulesQuery) -> Dict:
        headers = self.__get_headers()
        url = f"{self.domain}/{self.api_version}/boxes/{id}/{endpoint}"
        response = requests.post(url, headers=headers, json={"id": id}, params=query, timeout=10)
        response.raise_for_status()
        return response.json()
    
    def get_boxes(self, group: Optional[int] = None) -> Union[Dict, List]:
        return self.__get("boxes", params={"group": group})
    
    def get_alarms(self) -> Union[Dict, List]:
        return self.__get("alarms", params={"query": None, "groupBy": None, "sortBy": None, "limit": None, "cursor": None })

    def get_alarm(self, box_id: str, alarm_id: str) -> Union[Dict, List]:
        return self.__get("alarms", params={"gid": box_id, "aid": alarm_id})
    
    def delete_alarm(self, box_id: str, alarm_id: str) -> Dict:
        return self.__delete("alarms", params={"gid": box_id, "aid": alarm_id})
    
    def pause_rule(self, id: str) -> str:
        return self.__post(f"rules/{id}/pause")
    
    def resume_rule(self, id: str) -> str:
        return self.__post(f"rules/{id}/resume")
    
    def get_flows(self, params: Dict = {"query": None, "groupBy": None, "sortBy": None, "limit": None, "cursor": None}) -> Union[Dict, List]:
        return self.__get("flows", params=params)
    
    def get_target_lists(self) -> Union[Dict, List]:
        return self.__get("target-lists")

    def get_target_list(self, id: Optional[str] = None) -> Union[Dict, List]:
        return self.__get("target-lists", identifier=id)
    
    def create_target_list(self, name: Optional[str] = None, targets: List = [], 
                           owner: Optional[str] = None, category: Optional[str] = None, notes: Optional[str] = None) -> Dict:
        return self.__post("target-lists", json={"name": name, "targets": targets, "owner": owner, "category": category, "notes": notes})
    
    def update_target_list(self, id: int, name: Optional[str] = None, targets: List = [], notes: Optional[str] = None) -> Dict:
        return self.__put("target-lists", identifier=id, json={"name": name, "targets": targets, "notes": notes})
    
    def delete_target_list(self, id: int) -> Dict:
        return self.__delete("target-lists", identifier=id)

    def get_devices(self, box: Optional[int] = None, group: Optional[str] = None) -> Union[Dict, List]:
        return self.__get("devices", params={"box": box, "group": group})
    
    def get_stats(self, params: StatsParams, type: Optional[FlowType] = None) -> Union[Dict, List]:
        query_params = ["group", "limit"]
        for key, value in params.items():
            if key in query_params:
                params[key] = value
        return self.__get("stats", params=params, identifier=type)
    
    def get_simple_stats(self, params: StatsParams) -> Union[Dict, List]:
        query_params = ["group"]
        for key, value in params.items():
            if key in query_params:
                params[key] = value
        return self.__get("stats/simple", params=params)
    
    def get_flow_trends(self, group: Optional[int] = None) -> Dict:
        return self.__get("trends/flows", params={"group": group})
    
    def get_alarm_trends(self, group: Optional[int] = None) -> Dict:
        return self.__get("trends/alarms", params={"group": group})
    
    def get_rule_trends(self, group: Optional[int] = None) -> Dict:
        return self.__get("trends/rules", params={"group": group})
