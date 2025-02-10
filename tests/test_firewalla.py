import pytest
import requests
import json
from unittest.mock import patch
from src.firewalla_unofficial_sdk.main import Firewalla, AlarmParams, StatsParams, SimpleStatsParams

@pytest.fixture
def firewalla_instance():
    api_key = "test_api_key"
    subdomain = "test_subdomain"
    return Firewalla(api_key=api_key, firewalla_msp_subdomain=subdomain)

def test_initialization(firewalla_instance):
    assert firewalla_instance.api_key == "test_api_key"
    assert firewalla_instance.domain == "https://test_subdomain.firewalla.net"
    assert firewalla_instance.api_version == "v2"
    assert firewalla_instance.paginated_results == []

def test_get_headers(firewalla_instance):
    headers = firewalla_instance._Firewalla__get_headers()
    assert headers == {
        "Authorization": "Token test_api_key",
        "Content-Type": "application/json"
    }

@patch('requests.get')
def test_get_request(mock_get, firewalla_instance):
    mock_response = {"status": "success"}
    mock_get.return_value = requests.Response()
    mock_get.return_value._content = json.dumps(mock_response).encode()
    mock_get.return_value.raise_for_status = lambda: None
    mock_get.return_value.status_code = 200
    
    response = firewalla_instance._Firewalla__get("test")
    assert response == mock_response
    mock_get.assert_called_once_with(
        "https://test_subdomain.firewalla.net/v2/test",
        headers={
            "Authorization": "Token test_api_key",
            "Content-Type": "application/json"
        },
        params=None,
        timeout=10
    )

@patch('requests.post')
def test_post_request(mock_post, firewalla_instance):
    mock_response = {"status": "created"}
    mock_post.return_value = requests.Response()
    mock_post.return_value._content = json.dumps(mock_response).encode()
    mock_post.return_value.raise_for_status = lambda: None
    mock_post.return_value.status_code = 201
    
    data = {"key": "value"}
    response = firewalla_instance._Firewalla__post("test", data=data)
    assert response == mock_response
    mock_post.assert_called_once_with(
        "https://test_subdomain.firewalla.net/v2/test",
        headers={
            "Authorization": "Token test_api_key",
            "Content-Type": "application/json"
        },
        json=data,
        timeout=10
    )

@patch('requests.put')
def test_put_request(mock_put, firewalla_instance):
    mock_response = {"status": "updated"}
    mock_put.return_value = requests.Response()
    mock_put.return_value._content = json.dumps(mock_response).encode()
    mock_put.return_value.raise_for_status = lambda: None
    mock_put.return_value.status_code = 200
    
    data = {"key": "value"}
    response = firewalla_instance._Firewalla__put("test", data=data)
    assert response == mock_response
    mock_put.assert_called_once_with(
        "https://test_subdomain.firewalla.net/v2/test",
        headers={
            "Authorization": "Token test_api_key",
            "Content-Type": "application/json"
        },
        json=data,
        timeout=10
    )

@patch('requests.delete')
def test_delete_request(mock_delete, firewalla_instance):
    mock_response = {"status": "deleted"}
    mock_delete.return_value = requests.Response()
    mock_delete.return_value._content = json.dumps(mock_response).encode()
    mock_delete.return_value.raise_for_status = lambda: None
    mock_delete.return_value.status_code = 200
    
    response = firewalla_instance._Firewalla__delete("test")
    assert response == mock_response
    mock_delete.assert_called_once_with(
        "https://test_subdomain.firewalla.net/v2/test",
        headers={
            "Authorization": "Token test_api_key",
            "Content-Type": "application/json"
        },
        params=None,
        timeout=10
    )

@patch('requests.get')
def test_get_boxes(mock_get, firewalla_instance):
    mock_response = {"results": [{"id": 1, "name": "Box 1"}]}
    mock_get.return_value = requests.Response()
    mock_get.return_value._content = json.dumps(mock_response).encode()
    mock_get.return_value.raise_for_status = lambda: None
    mock_get.return_value.status_code = 200
    
    response = firewalla_instance.get_boxes(group=1)
    assert response == mock_response
    mock_get.assert_called_once_with(
        "https://test_subdomain.firewalla.net/v2/boxes",
        headers={
            "Authorization": "Token test_api_key",
            "Content-Type": "application/json"
        },
        params={"group": 1},
        timeout=10
    )

@patch('requests.get')
def test_get_alarms(mock_get, firewalla_instance):
    mock_response = {"results": [{"id": 1, "alarm": "Alarm 1"}]}
    mock_get.return_value = requests.Response()
    mock_get.return_value._content = json.dumps(mock_response).encode()
    mock_get.return_value.raise_for_status = lambda: None
    mock_get.return_value.status_code = 200
    
    params = AlarmParams(query="test", groupBy="type", limit=10)
    response = firewalla_instance.get_alarms(params=params)
    assert response == mock_response
    mock_get.assert_called_once_with(
        "https://test_subdomain.firewalla.net/v2/alarms",
        headers={
            "Authorization": "Token test_api_key",
            "Content-Type": "application/json"
        },
        params=params,
        timeout=10
    )

@patch('requests.get')
def test_get_flows(mock_get, firewalla_instance):
    mock_response = {"results": [{"id": 1, "flow": "Flow 1"}]}
    mock_get.return_value = requests.Response()
    mock_get.return_value._content = json.dumps(mock_response).encode()
    mock_get.return_value.raise_for_status = lambda: None
    mock_get.return_value.status_code = 200
    
    params = {"query": "test", "groupBy": "type", "limit": 10}
    response = firewalla_instance.get_flows(params=params)
    assert response == mock_response
    mock_get.assert_called_once_with(
        "https://test_subdomain.firewalla.net/v2/flows",
        headers={
            "Authorization": "Token test_api_key",
            "Content-Type": "application/json"
        },
        params=params,
        timeout=10
    )

@patch('requests.get')
def test_get_stats(mock_get, firewalla_instance):
    mock_response = {"results": [{"id": 1, "stat": "Stat 1"}]}
    mock_get.return_value = requests.Response()
    mock_get.return_value._content = json.dumps(mock_response).encode()
    mock_get.return_value.raise_for_status = lambda: None
    mock_get.return_value.status_code = 200
    
    params = StatsParams(group="1", limit=10)
    response = firewalla_instance.get_stats(type="topBoxesByBlockedFlows", params=params)
    assert response == mock_response
    mock_get.assert_called_once_with(
        "https://test_subdomain.firewalla.net/v2/stats/topBoxesByBlockedFlows",
        headers={
            "Authorization": "Token test_api_key",
            "Content-Type": "application/json"
        },
        params=params,
        timeout=10
    )

@patch('requests.get')
def test_get_simple_stats(mock_get, firewalla_instance):
    mock_response = {"results": [{"id": 1, "stat": "Simple Stat 1"}]}
    mock_get.return_value = requests.Response()
    mock_get.return_value._content = json.dumps(mock_response).encode()
    mock_get.return_value.raise_for_status = lambda: None
    mock_get.return_value.status_code = 200
    
    params = SimpleStatsParams(group="1")
    response = firewalla_instance.get_simple_stats(params=params)
    assert response == mock_response
    mock_get.assert_called_once_with(
        "https://test_subdomain.firewalla.net/v2/stats/simple",
        headers={
            "Authorization": "Token test_api_key",
            "Content-Type": "application/json"
        },
        params=params,
        timeout=10
    )

@patch('requests.get')
def test_get_flow_trends(mock_get, firewalla_instance):
    mock_response = {"results": [{"id": 1, "trend": "Flow Trend 1"}]}
    mock_get.return_value = requests.Response()
    mock_get.return_value._content = json.dumps(mock_response).encode()
    mock_get.return_value.raise_for_status = lambda: None
    mock_get.return_value.status_code = 200
    
    response = firewalla_instance.get_flow_trends()
    assert response == mock_response
    mock_get.assert_called_once_with(
        "https://test_subdomain.firewalla.net/v2/trends/flows",
        headers={
            "Authorization": "Token test_api_key",
            "Content-Type": "application/json"
        },
        params=None,
        timeout=10
    )

@patch('requests.get')
def test_get_alarm_trends(mock_get, firewalla_instance):
    mock_response = {"results": [{"id": 1, "trend": "Alarm Trend 1"}]}
    mock_get.return_value = requests.Response()
    mock_get.return_value._content = json.dumps(mock_response).encode()
    mock_get.return_value.raise_for_status = lambda: None
    mock_get.return_value.status_code = 200
    
    response = firewalla_instance.get_alarm_trends()
    assert response == mock_response
    mock_get.assert_called_once_with(
        "https://test_subdomain.firewalla.net/v2/trends/alarms",
        headers={
            "Authorization": "Token test_api_key",
            "Content-Type": "application/json"
        },
        params=None,
        timeout=10
    )

@patch('requests.get')
def test_get_target_lists(mock_get, firewalla_instance):
    mock_response = [{"id": 1, "name": "Target List 1"}]
    mock_get.return_value = requests.Response()
    mock_get.return_value._content = json.dumps(mock_response).encode()
    mock_get.return_value.raise_for_status = lambda: None
    mock_get.return_value.status_code = 200
    
    response = firewalla_instance.get_target_lists()
    assert response == mock_response
    mock_get.assert_called_once_with(
        "https://test_subdomain.firewalla.net/v2/target-lists",
        headers={
            "Authorization": "Token test_api_key",
            "Content-Type": "application/json"
        },
        params=None,
        timeout=10
    )

@patch('requests.post')
def test_create_target_list(mock_post, firewalla_instance):
    mock_response = {"id": 1, "name": "New Target List"}
    mock_post.return_value = requests.Response()
    mock_post.return_value._content = json.dumps(mock_response).encode()
    mock_post.return_value.raise_for_status = lambda: None
    mock_post.return_value.status_code = 201
    
    name = "New Target List"
    targets = ["example.com"]
    owner = "user1"
    category = "custom"
    notes = "Test notes"
    
    response = firewalla_instance.create_target_list(
        name=name,
        targets=targets,
        owner=owner,
        category=category,
        notes=notes
    )
    assert response == mock_response
    mock_post.assert_called_once_with(
        "https://test_subdomain.firewalla.net/v2/target-lists",
        headers={
            "Authorization": "Token test_api_key",
            "Content-Type": "application/json"
        },
        json={
            "name": name,
            "targets": targets,
            "owner": owner,
            "category": category,
            "notes": notes
        },
        timeout=10
    )

@patch('requests.put')
def test_update_target_list(mock_put, firewalla_instance):
    mock_response = {"id": 1, "name": "Updated Target List"}
    mock_put.return_value = requests.Response()
    mock_put.return_value._content = json.dumps(mock_response).encode()
    mock_put.return_value.raise_for_status = lambda: None
    mock_put.return_value.status_code = 200
    
    id = 1
    name = "Updated Target List"
    targets = ["example.com"]
    category = "custom"
    notes = "Updated notes"
    
    response = firewalla_instance.update_target_list(
        id=id,
        name=name,
        targets=targets,
        category=category,
        notes=notes
    )
    assert response == mock_response
    mock_put.assert_called_once_with(
        f"https://test_subdomain.firewalla.net/v2/target-lists/{id}",
        headers={
            "Authorization": "Token test_api_key",
            "Content-Type": "application/json"
        },
        json={
            "name": name,
            "targets": targets,
            "category": category,
            "notes": notes
        },
        timeout=10
    )

@patch('requests.delete')
def test_delete_target_list(mock_delete, firewalla_instance):
    mock_response = {"status": "success"}
    mock_delete.return_value = requests.Response()
    mock_delete.return_value._content = json.dumps(mock_response).encode()
    mock_delete.return_value.raise_for_status = lambda: None
    mock_delete.return_value.status_code = 200
    
    id = 1
    response = firewalla_instance.delete_target_list(id=id)
    assert response == mock_response
    mock_delete.assert_called_once_with(
        f"https://test_subdomain.firewalla.net/v2/target-lists/{id}",
        headers={
            "Authorization": "Token test_api_key",
            "Content-Type": "application/json"
        },
        params=None,
        timeout=10
    )

@patch('requests.get')
def test_get_request_timeout(mock_get, firewalla_instance):
    mock_get.side_effect = requests.exceptions.Timeout("Request timed out")
    
    response = firewalla_instance._Firewalla__get("test")
    assert response == {"error": "Timeout occurred: Request timed out"}

@patch('requests.get')
def test_get_request_connection_error(mock_get, firewalla_instance):
    mock_get.side_effect = requests.exceptions.ConnectionError("Connection refused")
    
    response = firewalla_instance._Firewalla__get("test")
    assert response == {"error": "ConnectionError occurred: Connection refused"}

@patch('requests.get')
def test_get_json_decode_error(mock_get, firewalla_instance):
    mock_response = requests.Response()
    mock_response.status_code = 200
    mock_response._content = "Invalid JSON".encode()
    mock_response.raise_for_status = lambda: None
    mock_get.return_value = mock_response
    
    response = firewalla_instance._Firewalla__get("test")
    assert "JSONDecodeError occurred" in response["error"]

@patch('requests.post')
def test_post_json_decode_error(mock_post, firewalla_instance):
    mock_response = requests.Response()
    mock_response.status_code = 200
    mock_response._content = "Invalid JSON".encode()
    mock_response.raise_for_status = lambda: None
    mock_post.return_value = mock_response
    
    response = firewalla_instance._Firewalla__post("test", data={"data": "test"})
    assert "JSONDecodeError occurred" in response["error"]

@patch('requests.get')
def test_get_empty_response(mock_get, firewalla_instance):
    mock_response = requests.Response()
    mock_response.status_code = 200
    mock_response._content = "".encode()
    mock_response.raise_for_status = lambda: None
    mock_get.return_value = mock_response
    
    response = firewalla_instance._Firewalla__get("test")
    assert "JSONDecodeError occurred" in response["error"]

@patch('requests.get')
def test_get_query_url_encoding(mock_get, firewalla_instance):
    mock_response = requests.Response()
    mock_response.status_code = 200
    mock_response._content = json.dumps({"result": "success"}).encode()
    mock_response.raise_for_status = lambda: None
    mock_get.return_value = mock_response
    
    params = {"query": "box.name:\"Test Box\""}
    firewalla_instance._Firewalla__get("test", params=params)
    
    # Verify the query was URL encoded
    called_args = mock_get.call_args[1]
    assert "box.name%3A%22Test+Box%22" in str(called_args["params"]["query"])

@patch('requests.get')
def test_get_cursor_base64_decoding(mock_get, firewalla_instance):
    mock_response = requests.Response()
    mock_response.status_code = 200
    mock_response._content = json.dumps({"result": "success"}).encode()
    mock_response.raise_for_status = lambda: None
    mock_get.return_value = mock_response
    
    # Test with valid base64 cursor
    params = {"cursor": "SGVsbG8gV29ybGQ="}  # Base64 for "Hello World"
    firewalla_instance._Firewalla__get("test", params=params)
    
    # Verify the cursor was decoded
    called_args = mock_get.call_args[1]
    assert called_args["params"]["cursor"] == b"Hello World"
