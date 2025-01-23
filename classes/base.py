import base64
import requests
import urllib.parse
from typing import Dict, Union

class BaseFirewallaSDK:
    def __init__(self, api_key: str, firewalla_msp_subdomain: str):
        self.api_key = api_key
        self.domain = f"https://{firewalla_msp_subdomain}.firewalla.net"
        self.api_version = "v2"
        self.url = None
        self.paginated_results = []

    def __get_headers(self):
        return {
            "Authorization": f"Token {self.api_key}",
            "Content-Type": "application/json"
        }

    def _get(self, endpoint: str, params: Dict = None, identifier: Union[int, str] = None):
        self.url = f"{self.domain}/{self.api_version}/{endpoint}"
        if identifier:
            self.url = f"{self.url}/{identifier}"
        headers = self.__get_headers()
        if "query" in params:
            params["query"] = urllib.parse.quote_plus(params["query"])
        print(params)
        response = requests.get(self.url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
                        
        if isinstance(data, dict):
            self.paginated_results.extend(data.get("results", []))
            next_cursor = data.get("next_cursor")
        
            while next_cursor:
                next_cursor = base64.b64decode(next_cursor).decode('utf-8')
                params["cursor"] = next_cursor
                data = self._get(endpoint=endpoint, params=params, identifier=identifier)
                self.paginated_results.extend(data.get("results", []))
                next_cursor = data.get("next_cursor")

            return self.paginated_results
        else:
            return data
        

    def _post(self, endpoint: str, json: Dict) -> Dict:
        headers = self.__get_headers()
        url = f"{self.domain}/{self.api_version}/{endpoint}"
        response = requests.post(url, headers=headers, json=json)
        response.raise_for_status()
        return response.json()
    
    def _put(self, endpoint: str, identifier: Union[int, str] = None, json: Dict = None) -> Dict:
        headers = self.__get_headers()
        url = f"{self.domain}/{self.api_version}/{endpoint}/{identifier}"
        response = requests.put(url, headers=headers, json=json)
        response.raise_for_status()
        return response.json()
    
    def _delete(self, endpoint: str, identifier: Union[int, str] = None):
        headers = self.__get_headers()
        url = f"{self.domain}/{self.api_version}/{endpoint}/{identifier}"
        response = requests.delete(url, headers=headers)
        response.raise_for_status()
        return response.json()
