import base64
import requests
import urllib.parse
from typing import Dict, Union, Literal, TypeAlias, List, Optional

RulesQuery = Literal["group", "limit"]
EndpointTypes = Literal["pause", "resume"]
FlowType: TypeAlias = Literal["topBoxesByBlockedFlows", "topBoxesBySecurityAlarms", "topRegionsByBlockedFlows"]
StatsParams: TypeAlias = Literal["group", "limit"]

class Firewalla:
    '''
    Firewalla API client
    Simple interface to interact with the Firewalla API
    '''
    
    def __init__(self, api_key: str, firewalla_msp_subdomain: str):
        """
        Initialize the Firewalla SDK instance.

        Args:
            api_key (str): The API key for authenticating with the Firewalla service.
            firewalla_msp_subdomain (str): The subdomain for the Firewalla MSP.
        """
        self.api_key: str = api_key
        self.domain: str = f"https://{firewalla_msp_subdomain}.firewalla.net"
        self.api_version: str = "v2"
        self.url: str = None
        self.paginated_results: List[Dict] = []

    def __get_headers(self) -> Dict[str, str]:
        """
        Get the headers for the API request.

        Returns:
            Dict[str, str]: A dictionary containing the headers.
        """
        return {
            "Authorization": f"Token {self.api_key}",
            "Content-Type": "application/json"
        }

    def __get(self, endpoint: str, params: Optional[Dict] = None, identifier: Optional[Union[int, str]] = None, timeout: int = 10) -> Union[Dict, List]:
        """
        Send a GET request to the specified endpoint.

        Args:
            endpoint (str): The API endpoint to send the GET request to.
            params (Dict, optional): A dictionary of query parameters to include in the request. Defaults to None.
            identifier (Union[int, str], optional): An optional identifier to append to the endpoint URL. Defaults to None.
            timeout (int, optional): The maximum number of seconds to wait for a response. Defaults to 10 seconds.

        Returns:
            Union[Dict, List]: The JSON response from the API. If the response contains paginated results, 
                               it returns a list of all results. Otherwise, it returns the JSON response as a dictionary.
        Raises:
            HTTPError: If the HTTP request returned an unsuccessful status code.
        """
        self.url = f"{self.domain}/{self.api_version}/{endpoint}"
        if identifier:
            self.url = f"{self.url}/{identifier}"
        headers = self.__get_headers()
        if params is not None:
            params = {k: v for k, v in params.items() if v is not None}
            if "query" in params and not None:
                print(params["query"])
                params["query"] = urllib.parse.quote_plus(str(params["query"]))
            if "cursor" in params and not None:
                params["cursor"] = base64.b64decode(str(params["cursor"]))
        response = requests.get(self.url, headers=headers, params=params, timeout=timeout)
        response.raise_for_status()
        data = response.json()
        return data

    def __post(self, endpoint: str, json: Optional[Dict] = None, timeout: int = 10) -> Dict:
        """
        Send a POST request to the specified endpoint.

        Args:
            endpoint (str): The API endpoint to send the POST request to.
            json (Dict, optional): The JSON payload to include in the request. Defaults to None.
            timeout (int, optional): The maximum number of seconds to wait for a response. Defaults to 10 seconds.

        Returns:
            Dict: The JSON response from the API.
        Raises:
            HTTPError: If the HTTP request returned an unsuccessful status code.
        """
        headers = self.__get_headers()
        url = f"{self.domain}/{self.api_version}/{endpoint}"
        response = requests.post(url, headers=headers, json=json, timeout=timeout)
        response.raise_for_status()
        return response.json()

    def __put(self, endpoint: str, identifier: Optional[Union[int, str]] = None, json: Optional[Dict] = None, timeout: int = 10) -> Dict:
        """
        Send a PUT request to the specified endpoint.

        Args:
            endpoint (str): The API endpoint to send the PUT request to.
            identifier (Union[int, str], optional): An optional identifier to append to the endpoint URL. Defaults to None.
            json (Dict, optional): The JSON payload to include in the request. Defaults to None.
            timeout (int, optional): The maximum number of seconds to wait for a response. Defaults to 10 seconds.

        Returns:
            Dict: The JSON response from the API.
        Raises:
            HTTPError: If the HTTP request returned an unsuccessful status code.
        """
        headers = self.__get_headers()
        url = f"{self.domain}/{self.api_version}/{endpoint}"
        if identifier:
            url = f"{url}/{identifier}"
        response = requests.put(url, headers=headers, json=json, timeout=timeout)
        response.raise_for_status()
        return response.json()

    def __delete(self, endpoint: str, params: Optional[Dict] = None, timeout: int = 10) -> Dict:
        """
        Send a DELETE request to the specified endpoint.

        Args:
            endpoint (str): The API endpoint to send the DELETE request to.
            params (Dict, optional): A dictionary of query parameters to include in the request. Defaults to None.
            timeout (int, optional): The maximum number of seconds to wait for a response. Defaults to 10 seconds.

        Returns:
            Dict: The JSON response from the API.
        Raises:
            HTTPError: If the HTTP request returned an unsuccessful status code.
        """
        headers = self.__get_headers()
        url = f"{self.domain}/{self.api_version}/{endpoint}"
        response = requests.delete(url, headers=headers, params=params, timeout=timeout)
        response.raise_for_status()
        return response.json()

    def get_boxes(self, group: Optional[int] = None) -> Union[Dict, List]:
        return self.__get("boxes", params={"group": group})
    
    def get_alarms(self, params={"query": None, "groupBy": None, "sortBy": None, "limit": None, "cursor": None }) -> Union[Dict, List]:
        """
        Retrieve the alarms.

        Returns:
            Union[Dict, List]: The alarms data.
        """
        return self.__get("alarms", params=params)

    def get_alarm(self, box_id: str, alarm_id: str) -> Union[Dict, List]:
        """
        Retrieve a specific alarm.

        Args:
            box_id (str): The ID of the box.
            alarm_id (str): The ID of the alarm.

        Returns:
            Union[Dict, List]: The alarm data.
        """
        return self.__get("alarms", params={"gid": box_id, "aid": alarm_id})
    
    def delete_alarm(self, box_id: str, alarm_id: str) -> Dict:
        """
        Delete a specific alarm.

        Args:
            box_id (str): The ID of the box.
            alarm_id (str): The ID of the alarm.

        Returns:
            Dict: The response from the API.
        """
        return self.__delete("alarms", params={"gid": box_id, "aid": alarm_id})
    
    def pause_rule(self, id: str) -> str:
        """
        Pause a specific rule.

        Args:
            id (str): The ID of the rule.

        Returns:
            str: The response from the API.
        """
        return self.__post(f"rules/{id}/pause")
    
    def resume_rule(self, id: str) -> str:
        """
        Resume a specific rule.

        Args:
            id (str): The ID of the rule.

        Returns:
            str: The response from the API.
        """
        return self.__post(f"rules/{id}/resume")
    
    def get_flows(self, params: Dict = {"query": None, "groupBy": None, "sortBy": None, "limit": None, "cursor": None}) -> Union[Dict, List]:
        """
        Retrieve the flows.

        Args:
            params (Dict, optional): A dictionary of query parameters. Defaults to {"query": None, "groupBy": None, "sortBy": None, "limit": None, "cursor": None}.

        Returns:
            Union[Dict, List]: The flows data.
        """
        return self.__get("flows", params=params)
    
    def get_target_lists(self) -> Union[Dict, List]:
        """
        Retrieve the target lists.

        Returns:
            Union[Dict, List]: The target lists data.
        """
        return self.__get("target-lists")

    def get_target_list(self, id: str = None) -> Union[Dict, List]:
        """
        Retrieve a specific target list.

        Args:
            id (str, optional): The ID of the target list. Defaults to None.

        Returns:
            Union[Dict, List]: The target list data.
        """
        return self.__get("target-lists", identifier=id)
    
    def create_target_list(self, name: str = None, targets: List = [], 
                           owner: str = None, category: str = None, notes: str = None) -> Dict:
        return self.__post("target-lists", json={"name": name, "targets": targets, "owner": owner, "category": category, "notes": notes})
    
    def update_target_list(self, id: int, name: str = None, targets: List = [], notes: str = None) -> Dict:
        return self.__put("target-lists", identifier=id, json={"name": name, "targets": targets, "notes": notes})
    
    def delete_target_list(self, id: int) -> Dict:
        return self.__delete(f"target-lists/{id}")

    def get_devices(self, box: str = None, group: str = None) -> Union[Dict, List]:
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
