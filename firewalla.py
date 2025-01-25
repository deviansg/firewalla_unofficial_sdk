import base64
import requests
import urllib.parse
from typing import Dict, Union, Literal, TypeAlias

RulesQuery = Literal["group", "limit"]
EndpointTypes = Literal["pause", "resume"]
FlowType: TypeAlias = Literal["topBoxesByBlockedFlows", "topBoxesBySecurityAlarms", "topRegionsByBlockedFlows"]
StatsParams: TypeAlias = Literal["group", "limit"]

class Firewalla():
    
    def __init__(self, api_key: str, firewalla_msp_subdomain: str):
        """
        Initialize the Firewalla SDK instance.

        Args:
            api_key (str): The API key for authenticating with the Firewalla service.
            firewalla_msp_subdomain (str): The subdomain for the Firewalla MSP.

        Attributes:
            api_key (str): The API key for authenticating with the Firewalla service.
            domain (str): The base URL for the Firewalla MSP.
            api_version (str): The version of the Firewalla API being used.
            url (str or None): The URL for the current API request.
            paginated_results (list): A list to store paginated results from API responses.
        """
        self.api_key = api_key
        self.domain = f"https://{firewalla_msp_subdomain}.firewalla.net"
        self.api_version = "v2"
        self.url = None
        self.paginated_results = []

    def __get_headers(self):
        """
        Generate the headers required for API requests.

        Returns:
            dict: A dictionary containing the authorization token and content type.
        """
        return {
            "Authorization": f"Token {self.api_key}",
            "Content-Type": "application/json"
        }

    def __get(self, endpoint: str, params: Dict = None, identifier: Union[int, str] = None):
        """
        Sends a GET request to the specified endpoint with optional parameters and identifier.
        Args:
            endpoint (str): The API endpoint to send the GET request to.
            params (Dict, optional): A dictionary of query parameters to include in the request. Defaults to None.
            identifier (Union[int, str], optional): An optional identifier to append to the endpoint URL. Defaults to None.
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
        
    def __post(self, endpoint: str, json: Dict = None):
        """
        Sends a POST request to the specified endpoint with the given JSON payload.

        Args:
            endpoint (str): The API endpoint to send the request to.
            json (Dict, optional): The JSON payload to include in the request. Defaults to None.

        Returns:
            dict: The JSON response from the server.

        Raises:
            requests.exceptions.HTTPError: If the HTTP request returned an unsuccessful status code.
        """
        headers = self.__get_headers()
        url = f"{self.domain}/{self.api_version}/{endpoint}"
        response = requests.post(url, headers=headers, json=json, timeout=10)
        response.raise_for_status()
        return response.json()
    
    def __put(self, endpoint: str, identifier: Union[int, str] = None, json: Dict = None):
        """
        Sends a PUT request to the specified endpoint with the given JSON payload.

        Args:
            endpoint (str): The API endpoint to send the request to.
            identifier (Union[int, str], optional): An optional identifier to append to the endpoint URL. Defaults to None.
            json (Dict, optional): The JSON payload to include in the request body. Defaults to None.

        Returns:
            dict: The JSON response from the server.

        Raises:
            requests.exceptions.HTTPError: If the HTTP request returned an unsuccessful status code.
        """
        headers = self.__get_headers()
        url = f"{self.domain}/{self.api_version}/{endpoint}/{identifier}"
        response = requests.put(url, headers=headers, json=json, timeout=10)
        response.raise_for_status()
        return response.json()
    
    def __delete(self, endpoint: str, identifier: Union[int, str] = None, params: Dict = None):
        """
        Sends a DELETE request to the specified endpoint with an optional identifier.

        Args:
            endpoint (str): The API endpoint to send the DELETE request to.
            identifier (Union[int, str], optional): The identifier to append to the endpoint URL. Defaults to None.

        Returns:
            dict: The JSON response from the server.

        Raises:
            requests.exceptions.HTTPError: If the HTTP request returned an unsuccessful status code.
        """
        headers = self.__get_headers()
        url = f"{self.domain}/{self.api_version}/{endpoint}/{identifier}"
        response = requests.delete(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()

    def __post_rules(self, endpoint: EndpointTypes, id: int, query: RulesQuery):
        """
        Sends a POST request to the specified endpoint with the given rules query.

        Args:
            endpoint (EndpointTypes): The endpoint to which the request is sent.
            id (int): The ID of the box.
            query (RulesQuery): The query parameters for the rules.

        Returns:
            dict: The JSON response from the server.

        Raises:
            HTTPError: If the HTTP request returned an unsuccessful status code.
        """
        headers = self.__get_headers()
        url = f"{self.domain}/{self.api_version}/boxes/{id}/{endpoint}"
        response = requests.post(url, headers=headers, json={"id": id}, params=query, timeout=10)
        response.raise_for_status()
        return response.json()
    
    def get_boxes(self, group: int = None):
        """
        Retrieve a list of boxes.

        Args:
            group (int, optional): The group ID to filter boxes by. Defaults to None.

        Returns:
            dict: The response from the API containing the list of boxes.
        """
        return self.__get("boxes", params={"group": group})
    
    def get_alarms(self):
        """
        Retrieve alarms from the Firewalla device.

        This method sends a GET request to the "alarms" endpoint to fetch alarm data.
        
        Returns:
            dict: A dictionary containing the alarm data.
        """
        return self.__get("alarms", params={"query": None, "groupBy": None, "sortBy": None, "limit": None, "cursor": None })

    def get_alarm(self, box_id: str, alarm_id: str):
        """
        Retrieve a specific alarm from a Firewalla box.

        Args:
            box_id (str): The unique identifier of the Firewalla box.
            alarm_id (str): The unique identifier of the alarm.

        Returns:
            dict: The alarm details retrieved from the Firewalla box.
        """
        return self.__get("alarms", params={"gid": box_id, "aid": alarm_id})
    
    def delete_alarm(self, box_id: str, alarm_id: str):
        """
        Deletes an alarm from the specified box.

        Args:
            box_id (str): The ID of the box from which the alarm will be deleted.
            alarm_id (str): The ID of the alarm to be deleted.

        Returns:
            Response: The response from the delete request.
        """
        return self.__delete("alarms", params={"gid": box_id, "aid": alarm_id})
    
    def pause_rule(self, id: str) -> str:
        """
        Pause a specific rule by its ID.

        Args:
            id (str): The ID of the rule to be paused.

        Returns:
            str: The response from the server after attempting to pause the rule.
        """
        return self.__post(f"rules/{id}/pause")
    
    def resume_rule(self, id: str) -> str:
        """
        Resume a specific rule by its ID.

        Args:
            id (str): The ID of the rule to be resumed.

        Returns:
            str: The response from the server after attempting to resume the rule.
        """
        return self.__post(f"rules/{id}/resume")
    
    def get_flows(self, params: Dict = {"query": None, "groupBy": None, "sortBy": None, "limit": None, "cursor": None}):
        """
        Retrieve network flows based on specified parameters.

        Args:
            params (Dict, optional): A dictionary of parameters to filter and sort the flows.
                - query (str, optional): Query string to filter the flows.
                - groupBy (str, optional): Field to group the flows by.
                - sortBy (str, optional): Field to sort the flows by.
                - limit (int, optional): Maximum number of flows to return.
                - cursor (str, optional): Cursor for pagination.

        Returns:
            dict: A dictionary containing the network flows data.
        """
        return self.__get("flows", params=params)
    
    def get_target_lists(self):
        """
        Retrieve the target lists from the Firewalla API.

        Returns:
            dict: A dictionary containing the target lists.
        """
        return self.__get("target-lists")

    def get_target_list(self, id=None):
        """
        Retrieve the target list.

        Args:
            id (str, optional): The identifier for the target list. Defaults to None.

        Returns:
            dict: The target list data.
        """
        return self.__get("target-lists", identifier=id)
    
    def create_target_list(self, name: str = None, targets: list = [], 
                           owner: str = None, category: str = None, notes: str = None):
        """
        Creates a target list with the specified parameters.

        Args:
            name (str, optional): The name of the target list. Defaults to None.
            targets (list, optional): A list of targets to include in the target list. Defaults to an empty list.
            owner (str, optional): The owner of the target list. Defaults to None.
            category (str, optional): The category of the target list. Defaults to None.
            notes (str, optional): Additional notes for the target list. Defaults to None.

        Returns:
            dict: The response from the server after creating the target list.
        """
        return self.__post(json={"name": name, "targets": targets, owner: owner, category: category, notes: notes})
    
    def update_target_list(self, id: int, name: str = None, targets: list = [], notes: str = None):
        """
        Update a target list with the given parameters.

        Args:
            id (int): The identifier of the target list to update.
            name (str, optional): The new name for the target list. Defaults to None.
            targets (list, optional): A list of new targets to include in the target list. Defaults to an empty list.
            notes (str, optional): Additional notes for the target list. Defaults to None.

        Returns:
            Response: The response from the PUT request to update the target list.
        """
        return self.__put("target-lists", identifier=id, json={"name": name, "targets": targets, "notes": notes})
    
    def delete_target_list(self, id: int):
        """
        Deletes a target list by its identifier.

        Args:
            id (int): The identifier of the target list to be deleted.

        Returns:
            Response: The response from the delete request.
        """
        return self.__delete("target-lists", identifier=id)

    def get_devices(self, box: int = None, group: str = None):
        """
        Retrieve a list of devices.

        Args:
            box (int, optional): The ID of the box to filter devices. Defaults to None.
            group (str, optional): The group name to filter devices. Defaults to None.

        Returns:
            dict: A dictionary containing the list of devices.
        """
        return super().__get("devices", params={"box": box, "group": group})
    
    def pause_rules(self, id: int, query: RulesQuery):
        """
        Pauses the specified rules.

        Args:
            id (int): The ID of the rule to pause.
            query (RulesQuery): The query parameters for the rule.

        Returns:
            Response: The response from the server after attempting to pause the rule.
        """
        return self.__post_rules("pause", id, query=query)
    
    def resume_rules(self, id: int, query: RulesQuery):
        """
        Resume the specified rules.

        Args:
            id (int): The ID of the rules to resume.
            query (RulesQuery): The query parameters for resuming the rules.

        Returns:
            Response: The response from the server after attempting to resume the rules.
        """
        return self.__post_rules("resume", id, query=query)
    
    def get_stats(self, params: StatsParams, type: FlowType=None):
        """
        Retrieve statistics based on the provided parameters.

        Args:
            params (StatsParams): The parameters for the statistics query.
            type (FlowType, optional): The type of flow to filter the statistics. Defaults to None.

        Returns:
            dict: The statistics data retrieved from the API.
        """
        query_params = ["group", "limit"]
        for key, value in params.items():
            if key in query_params:
                params[key] = value
        return self.__get("stats", params=params, identifier=type)
    
    def get_simple_stats(self, params: StatsParams):
        """
        Retrieve simple statistics based on the provided parameters.

        Args:
            params (StatsParams): A dictionary containing the parameters for the statistics query.
                - group (str, optional): The group parameter to filter the statistics.

        Returns:
            dict: A dictionary containing the simple statistics data.

        Raises:
            HTTPError: If the request to the stats endpoint fails.
        """
        query_params = ["group"]
        for key, value in params.items():
            if key in query_params:
                params[key] = value
        return self.__get("stats/simple", params=params)
    
    # Trends
    def get_flow_trends(self, group: int = None) -> Dict:
        """
        Retrieve network flow trend data.

        Args:
            group (int, optional): The group identifier for the flows. Defaults to None.

        Returns:
            dict: A dictionary containing the network flow data.
        """
        return self.__get("trends/flows", params={"group": group})
    
    def get_alarm_trends(self, group: int = None) -> Dict:
        """
        Retrieve alarm trends from the Firewalla device.

        Args:
            group (int, optional): The group ID to filter alarms. Defaults to None.

        Returns:
            dict: A dictionary containing the alarms data.
        """
        return self.__get("trends/alarms", params={"group": group})
    
    def get_rule_trends(self, group: int = None) -> Dict:
        """
        Retrieve the rules for a specified group.

        Args:
            group (int, optional): The group ID for which to retrieve rules. Defaults to None.

        Returns:
            dict: The rules for the specified group.
        """
        return self.__get("trends/rules", params={"group": group})