import requests
from typing import Dict, Callable

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
    
    def set_type(type: str = None):
        def set_type_inner(self, func: Callable):
            def wrapper(self, endpoint: str, params: Dict = None, type: str = None):
                if type:
                    self.url = f"{endpoint}/{type}"
                return func(self, self.url, params)
            return wrapper
        return set_type_inner

    def __get(self, endpoint: str, params: Dict = None, type: str = None):
        self.url = f"{self.domain}/{self.api_version}/{endpoint}"
        if type:
            self.url = f"{self.url}/{type}"
        headers = self.__get_headers()
        response = requests.get(self.url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
