import json
import base64
import requests
import urllib.parse
from typing import Dict, Union, Literal, TypeAlias, List, Optional, TypedDict

# RulesQuery = Literal["group", "limit"]
EndpointTypes = Literal["pause", "resume"]
FlowType: TypeAlias = Literal["topBoxesByBlockedFlows", "topBoxesBySecurityAlarms", "topRegionsByBlockedFlows"]

class StatsParams(TypedDict):
    group: Optional[str]
    limit: Optional[int]
    
class SimpleStatsParams(TypedDict):
    group: Optional[str]

class AlarmParams(TypedDict):
    query: Optional[str]
    groupBy: Optional[str]
    # sortBy: Optional[str]
    limit: Optional[int]
    cursor: Optional[str]


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

    def __get(self, endpoint: str, params: Optional[Dict] = None, timeout: int = 10) -> Union[Dict, List]:
        """
        Send a GET request to the specified endpoint.

        Args:
            endpoint (str): The API endpoint to send the GET request to.
            params (Dict, optional): A dictionary of query parameters to include in the request. Defaults to None.
            timeout (int, optional): The maximum number of seconds to wait for a response. Defaults to 10 seconds.

        Returns:
            Union[Dict, List]: The JSON response from the API. If the response contains paginated results, 
                               it returns a list of all results. Otherwise, it returns the JSON response as a dictionary.
        Raises:
            HTTPError: If the HTTP request returned an unsuccessful status code.
        """
        self.url = f"{self.domain}/{self.api_version}/{endpoint}"
        headers = self.__get_headers()
    
        if params is not None:
            # Replace None values with empty strings
            params = {k: (v if v is not None else "") for k, v in params.items()}
            # Add identifier to URL
            # Parse query parameter
            if "query" in params and params["query"]:
                params["query"] = urllib.parse.quote_plus(str(params["query"]))
                print(f"Query: {params["query"]}")
            '''
            While this is documented in the API it does not appear to work
            resulting in a 400 error -- keeping here for possible future use
            '''
            # if "sortBy" in params and params["sortBy"]:
            #     params["sortBy"] = urllib.parse.quote_plus(str(params["sortBy"]))
            if "cursor" in params and params["cursor"]:
                params["cursor"] = base64.b64decode(str(params["cursor"]))

        print(f"Params: {params}")
                
        try:
            response = requests.get(self.url, headers=headers, params=params, timeout=timeout)
            print(f"Response: {response.text}")
            print(response.request.url)
            response.raise_for_status()
            data = json.loads(response.content)
            if endpoint and endpoint == "target-lists":
                print(f"TARGET LIST Data: {data}")
            return data
        except requests.exceptions.HTTPError as err:
            if response.status_code == 400 and not response.text:
                return {"error": "Received a 400 error with an empty body."}
            else:
                return json.loads(err.response.text)
        except requests.exceptions.RequestException as err:
            return json.loads({"error": f"HTTP Request Error occurred: {err}"})
        except json.JSONDecodeError as err:
            return json.loads({"error": f"JSONDecodeError occurred: {err}"})
    
        
    def __post(self, endpoint: str, data: Optional[Dict] = {}, timeout: int = 10) -> Dict:
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
        try:
            data = {k: (v if v is not None else "") for k, v in data.items()}
            headers = self.__get_headers()
            url = f"{self.domain}/{self.api_version}/{endpoint}"
            response = requests.post(url, headers=headers, json=data, timeout=timeout)
            response.raise_for_status()
            data = json.loads(response.content)
            return data
        except requests.exceptions.HTTPError as err:
            if response.status_code == 400 and err.response.text:
                data = json.loads(err.response.text)
                return data
            elif response.status_code == 400 and not err.response.text:
                return "Received a 400 error with an empty body."
        except requests.exceptions.RequestException as err:
            return json.loads({"error": f"HTTP Request Error occurred: {err}"})
        except json.JSONDecodeError as err:
            return json.loads({"error": f"JSONDecodeError occurred: {err}"})

    def __put(self, endpoint: str, data: Optional[Dict] = None, timeout: int = 10) -> Dict:
        """
        Send a PUT request to the specified endpoint.

        Args:
            endpoint (str): The API endpoint to send the PUT request to.
            json (Dict, optional): The JSON payload to include in the request. Defaults to None.
            timeout (int, optional): The maximum number of seconds to wait for a response. Defaults to 10 seconds.

        Returns:
            Dict: The JSON response from the API.
        Raises:
            HTTPError: If the HTTP request returned an unsuccessful status code.
        """
        headers = self.__get_headers()
        url = f"{self.domain}/{self.api_version}/{endpoint}"
        response = requests.put(url, headers=headers, json=data, timeout=timeout)
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
        """
        Retrieve boxes information.

        Args:
            group (Optional[int], optional): The group identifier to filter boxes.

        Returns:
            Union[Dict, List]: The boxes data. If multiple boxes are retrieved, a list is returned. 
                            Otherwise, returns a dictionary containing the box data.
        """
        return self.__get("boxes", params={"group": group})
    
    def get_alarms(self, params: AlarmParams) -> Union[Dict, List]:
        """
        Retrieve the alarms.

        Returns:
            Union[Dict, List]: The alarms data.
        """
        self.__get("alarms", params=params)


    def get_alarm(self, box_id: str, alarm_id: str) -> Union[Dict, List]:
        """
        Retrieve a specific alarm.

        Args:
            box_id (str): The ID of the box.
            alarm_id (str): The ID of the alarm.

        Returns:
            Union[Dict, List]: The alarm data.
        """
        return self.__get(f"alarms/{box_id}/{alarm_id}")
    
    def delete_alarm(self, box_id: str, alarm_id: str) -> Dict:
        """
        Delete a specific alarm.

        Args:
            box_id (str): The ID of the box.
            alarm_id (str): The ID of the alarm.

        Returns:
            Dict: The response from the API.
        """
        return self.__delete(f"alarms/{box_id}/{alarm_id}")
    
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
    
    def get_flows(self, params: Dict = {"query": None, "groupBy": None, "limit": None, "cursor": None}) -> Union[Dict, List]:
        """
        Retrieve the flows.

        Args:
            params (Dict, optional): A dictionary of query parameters. Defaults to {"query": None, "groupBy": None, "limit": None, "cursor": None}.

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
        return self.__get(f"target-list/{id}")
    
    def create_target_list(self, data={"name": None, "targets": [], "category": None, "notes": None, "owner": "205ce275-e674-4a83-9f04-5f27d67fac28"}) -> Dict:
        """
        Create a new target list.

        Args:
            params (Dict, optional): A dictionary of parameters to include in the request. Defaults to {"name": None, "targets": None, "category": None, "notes": None}.

        Returns:
            Dict: The response from the API.
        """        
        return self.__post("target-lists", data=data)
    
    def update_target_list(self, id: int, data: Dict = {"name": None, "targets": None, "category": None, "notes": None}) -> Dict:
        return self.__put(f"target-lists/{id}", data=data)
    
    def delete_target_list(self, id: int) -> Dict:
        return self.__delete(f"target-lists/{id}")

    def get_devices(self, params: Dict = {"box_id": None, "group_id": None}) -> Union[Dict, List]:
        return self.__get("devices", params=params)
    
    def get_stats(self, type: FlowType, params: StatsParams = None) -> Union[Dict, List]:
        return self.__get(f"stats/{type}", params=params)
    
    def get_simple_stats(self, params: SimpleStatsParams = {"group": None}) -> Union[Dict, List]:
        return self.__get("stats/simple", params=params)
    
    def get_flow_trends(self, group: Optional[str] = None) -> Dict:
        return self.__get("trends/flows", params={"group": group})
    
    def get_alarm_trends(self, group: Optional[str] = None) -> Dict:
        return self.__get("trends/alarms", params={"group": group})
    
    def get_rule_trends(self, group: Optional[str] = None) -> Dict:
        return self.__get("trends/rules", params={"group": group})
