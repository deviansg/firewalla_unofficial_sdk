import requests
from typing import Dict, Union

class BaseFirewallaSDK:
    def __init__(self, api_key: str, domain: str):
        self.api_key = api_key
        self.domain = f"https://{domain}"
        self.api_version = "v2"
        self.endpoint
        self.url = None

    def __get_headers(self):
        return {
            "Authorization": f"Token {self.api_key}",
            "Content-Type": "application/json"
        }

    def __get(self, endpoint: str, params: Dict = None, identifier: Union[int, str] = None):
        self.url = f"{self.domain}/{self.api_version}/{endpoint}"
        if identifier:
            self.url = f"{self.url}/{identifier}"
        headers = self.__get_headers()
        response = requests.get(self.url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    
    def __post(self, endpoint: str, json: Dict):
        headers = self._get_headers()
        url = f"{self.domain}/{self.api_version}/{endpoint}"
        response = requests.post(url, headers=headers, json={"id": id}, json=json)
        response.raise_for_status()
        return response.json()
    
    def __put(self, endpoint: str, identifier: Union[int, str] = None):
        headers = self._get_headers()
        url = f"{self.domain}/{self.api_version}/{endpoint}/{identifier}"
        response = requests.put(url, headers=headers)
        response.raise_for_status()
        return response.json()
    
    def __delete(self, endpoint: str, identifier: Union[int, str] = None):
        headers = self._get_headers()
        url = f"{self.domain}/{self.api_version}/{endpoint}/{identifier}"
        response = requests.delete(url, headers=headers)
        response.raise_for_status()
        return response.json()
