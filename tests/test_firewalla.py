import pytest
from unittest.mock import patch
from ..firewalla import Firewalla

@pytest.fixture
def firewalla_instance():
    api_key = "test_api_key"
    subdomain = "test_subdomain"
    return Firewalla(api_key=api_key, firewalla_msp_subdomain=subdomain)

@patch('firewalla.requests.get')
def test_get_boxes_no_group(mock_get, firewalla_instance):
    mock_response = {
        "results": [{"id": 1, "name": "Box 1"}, {"id": 2, "name": "Box 2"}]
    }
    mock_get.return_value.json.return_value = mock_response
    mock_get.return_value.raise_for_status = lambda: None

    response = firewalla_instance.get_boxes()
    assert response == mock_response

@patch('firewalla.requests.get')
def test_get_boxes_with_group(mock_get, firewalla_instance):
    mock_response = {
        "results": [{"id": 1, "name": "Box 1"}]
    }
    mock_get.return_value.json.return_value = mock_response
    mock_get.return_value.raise_for_status = lambda: None

    response = firewalla_instance.get_boxes(group=1)
    assert response == mock_response

@patch('firewalla.requests.get')
def test_get_alarms(mock_get, firewalla_instance):
    mock_response = {
        "results": [{"id": 1, "alarm": "Alarm 1"}, {"id": 2, "alarm": "Alarm 2"}]
    }
    mock_get.return_value.json.return_value = mock_response
    mock_get.return_value.raise_for_status = lambda: None

    response = firewalla_instance.get_alarms()
    assert response == mock_response

@patch('firewalla.requests.get')
def test_get_alarm(mock_get, firewalla_instance):
    mock_response = {
        "results": [{"id": 1, "alarm": "Alarm 1"}]
    }
    mock_get.return_value.json.return_value = mock_response
    mock_get.return_value.raise_for_status = lambda: None

    response = firewalla_instance.get_alarm(box_id="box1", alarm_id="alarm1")
    assert response == mock_response

@patch('firewalla.requests.delete')
def test_delete_alarm(mock_delete, firewalla_instance):
    mock_response = {"status": "success"}
    mock_delete.return_value.json.return_value = mock_response
    mock_delete.return_value.raise_for_status = lambda: None

    response = firewalla_instance.delete_alarm(box_id="box1", alarm_id="alarm1")
    assert response == mock_response

@patch('firewalla.requests.post')
def test_pause_rule(mock_post, firewalla_instance):
    mock_response = {"status": "paused"}
    mock_post.return_value.json.return_value = mock_response
    mock_post.return_value.raise_for_status = lambda: None

    response = firewalla_instance.pause_rule(id="rule1")
    assert response == mock_response

@patch('firewalla.requests.post')
def test_resume_rule(mock_post, firewalla_instance):
    mock_response = {"status": "resumed"}
    mock_post.return_value.json.return_value = mock_response
    mock_post.return_value.raise_for_status = lambda: None

    response = firewalla_instance.resume_rule(id="rule1")
    assert response == mock_response

@patch('firewalla.requests.get')
def test_get_flows(mock_get, firewalla_instance):
    mock_response = {
        "results": [{"id": 1, "flow": "Flow 1"}, {"id": 2, "flow": "Flow 2"}]
    }
    mock_get.return_value.json.return_value = mock_response
    mock_get.return_value.raise_for_status = lambda: None

    response = firewalla_instance.get_flows()
    assert response == mock_response

@patch('firewalla.requests.get')
def test_get_target_lists(mock_get, firewalla_instance):
    mock_response = [
        {
            "id": "TL-00000000-0000-0000-0000-000000000000",
            "name": "A Simple Target List",
            "owner": "global",
            "targets": [
                "foo.com",
                "bar.net"
            ],
            "category": "edu",
            "notes": "This is a simple target list",
            "lastUpdated": 1664373339.857
        }
    ]
    mock_get.return_value.json.return_value = mock_response
    mock_get.return_value.raise_for_status = lambda: None

    response = firewalla_instance.get_target_lists()
    assert response == mock_response

@patch('firewalla.requests.get')
def test_get_target_list(mock_get, firewalla_instance):
    mock_response = {"id": 1, "target": "Target 1"}
    mock_get.return_value.json.return_value = mock_response
    mock_get.return_value.raise_for_status = lambda: None

    response = firewalla_instance.get_target_list(id=1)
    assert response == mock_response
    
@patch('firewalla.requests.put')
def test_put_request_with_identifier(mock_put, firewalla_instance):
    mock_response = {"status": "updated"}
    mock_put.return_value.json.return_value = mock_response
    mock_put.return_value.raise_for_status = lambda: None

    endpoint = "test-endpoint"
    identifier = "123"
    json_payload = {"key": "value"}

    response = firewalla_instance._Firewalla__put(endpoint=endpoint, identifier=identifier, json=json_payload)
    assert response == mock_response
    mock_put.assert_called_once_with(
        f"https://test_subdomain.firewalla.net/v2/{endpoint}/{identifier}",
        headers={
            "Authorization": "Token test_api_key",
            "Content-Type": "application/json"
        },
        json=json_payload,
        timeout=10
    )

@patch('firewalla.requests.put')
def test_put_request_without_identifier(mock_put, firewalla_instance):
    mock_response = {"status": "updated"}
    mock_put.return_value.json.return_value = mock_response
    mock_put.return_value.raise_for_status = lambda: None

    endpoint = "test-endpoint"
    json_payload = {"key": "value"}

    response = firewalla_instance._Firewalla__put(endpoint=endpoint, json=json_payload)
    assert response == mock_response
    mock_put.assert_called_once_with(
        f"https://test_subdomain.firewalla.net/v2/{endpoint}",
        headers={
            "Authorization": "Token test_api_key",
            "Content-Type": "application/json"
        },
        json=json_payload,
        timeout=10
    )

@patch('firewalla.requests.put')
def test_put_request_with_timeout(mock_put, firewalla_instance):
    mock_response = {"status": "updated"}
    mock_put.return_value.json.return_value = mock_response
    mock_put.return_value.raise_for_status = lambda: None

    endpoint = "test-endpoint"
    identifier = "123"
    json_payload = {"key": "value"}
    timeout = 20

    response = firewalla_instance._Firewalla__put(endpoint=endpoint, identifier=identifier, json=json_payload, timeout=timeout)
    assert response == mock_response
    mock_put.assert_called_once_with(
        f"https://test_subdomain.firewalla.net/v2/{endpoint}/{identifier}",
        headers={
            "Authorization": "Token test_api_key",
            "Content-Type": "application/json"
        },
        json=json_payload,
        timeout=timeout
    )
    
@patch('firewalla.requests.put')
def test_update_target_list(mock_put, firewalla_instance):
    mock_response = {"status": "updated"}
    mock_put.return_value.json.return_value = mock_response
    mock_put.return_value.raise_for_status = lambda: None

    id = 1
    name = "Updated Target List"
    targets = ["example.com", "example.net"]
    notes = "Updated notes"

    response = firewalla_instance.update_target_list(id=id, name=name, targets=targets, notes=notes)
    assert response == mock_response
    mock_put.assert_called_once_with(
        f"https://test_subdomain.firewalla.net/v2/target-lists/{id}",
        headers={
            "Authorization": "Token test_api_key",
            "Content-Type": "application/json"
        },
        json={"name": name, "targets": targets, "notes": notes},
        timeout=10
    )

@patch('firewalla.requests.put')
def test_update_target_list_no_name(mock_put, firewalla_instance):
    mock_response = {"status": "updated"}
    mock_put.return_value.json.return_value = mock_response
    mock_put.return_value.raise_for_status = lambda: None

    id = 1
    targets = ["example.com", "example.net"]
    notes = "Updated notes"

    response = firewalla_instance.update_target_list(id=id, targets=targets, notes=notes)
    assert response == mock_response
    mock_put.assert_called_once_with(
        f"https://test_subdomain.firewalla.net/v2/target-lists/{id}",
        headers={
            "Authorization": "Token test_api_key",
            "Content-Type": "application/json"
        },
        json={"name": None, "targets": targets, "notes": notes},
        timeout=10
    )

@patch('firewalla.requests.put')
def test_update_target_list_no_targets(mock_put, firewalla_instance):
    mock_response = {"status": "updated"}
    mock_put.return_value.json.return_value = mock_response
    mock_put.return_value.raise_for_status = lambda: None

    id = 1
    name = "Updated Target List"
    notes = "Updated notes"

    response = firewalla_instance.update_target_list(id=id, name=name, notes=notes)
    assert response == mock_response
    mock_put.assert_called_once_with(
        f"https://test_subdomain.firewalla.net/v2/target-lists/{id}",
        headers={
            "Authorization": "Token test_api_key",
            "Content-Type": "application/json"
        },
        json={"name": name, "targets": [], "notes": notes},
        timeout=10
    )

@patch('firewalla.requests.put')
def test_update_target_list_no_notes(mock_put, firewalla_instance):
    mock_response = {"status": "updated"}
    mock_put.return_value.json.return_value = mock_response
    mock_put.return_value.raise_for_status = lambda: None

    id = 1
    name = "Updated Target List"
    targets = ["example.com", "example.net"]

    response = firewalla_instance.update_target_list(id=id, name=name, targets=targets)
    assert response == mock_response
    mock_put.assert_called_once_with(
        f"https://test_subdomain.firewalla.net/v2/target-lists/{id}",
        headers={
            "Authorization": "Token test_api_key",
            "Content-Type": "application/json"
        },
        json={"name": name, "targets": targets, "notes": None},
        timeout=10
    )
    
@patch('firewalla.requests.post')
def test_create_target_list(mock_post, firewalla_instance):
    mock_response = {"status": "created"}
    mock_post.return_value.json.return_value = mock_response
    mock_post.return_value.raise_for_status = lambda: None

    name = "New Target List"
    targets = ["example.com", "example.net"]
    owner = "user"
    category = "test"
    notes = "Test notes"

    response = firewalla_instance.create_target_list(name=name, targets=targets, owner=owner, category=category, notes=notes)
    assert response == mock_response
    mock_post.assert_called_once_with(
        "https://test_subdomain.firewalla.net/v2/target-lists",
        headers={
            "Authorization": "Token test_api_key",
            "Content-Type": "application/json"
        },
        json={"name": name, "targets": targets, "owner": owner, "category": category, "notes": notes},
        timeout=10
    )

@patch('firewalla.requests.post')
def test_create_target_list_no_name(mock_post, firewalla_instance):
    mock_response = {"status": "created"}
    mock_post.return_value.json.return_value = mock_response
    mock_post.return_value.raise_for_status = lambda: None

    targets = ["example.com", "example.net"]
    owner = "user"
    category = "test"
    notes = "Test notes"

    response = firewalla_instance.create_target_list(targets=targets, owner=owner, category=category, notes=notes)
    assert response == mock_response
    mock_post.assert_called_once_with(
        "https://test_subdomain.firewalla.net/v2/target-lists",
        headers={
            "Authorization": "Token test_api_key",
            "Content-Type": "application/json"
        },
        json={"name": None, "targets": targets, "owner": owner, "category": category, "notes": notes},
        timeout=10
    )

@patch('firewalla.requests.post')
def test_create_target_list_no_targets(mock_post, firewalla_instance):
    mock_response = {"status": "created"}
    mock_post.return_value.json.return_value = mock_response
    mock_post.return_value.raise_for_status = lambda: None

    name = "New Target List"
    owner = "user"
    category = "test"
    notes = "Test notes"

    response = firewalla_instance.create_target_list(name=name, owner=owner, category=category, notes=notes)
    assert response == mock_response
    mock_post.assert_called_once_with(
        "https://test_subdomain.firewalla.net/v2/target-lists",
        headers={
            "Authorization": "Token test_api_key",
            "Content-Type": "application/json"
        },
        json={"name": name, "targets": [], "owner": owner, "category": category, "notes": notes},
        timeout=10
    )

@patch('firewalla.requests.post')
def test_create_target_list_no_owner(mock_post, firewalla_instance):
    mock_response = {"status": "created"}
    mock_post.return_value.json.return_value = mock_response
    mock_post.return_value.raise_for_status = lambda: None

    name = "New Target List"
    targets = ["example.com", "example.net"]
    category = "test"
    notes = "Test notes"

    response = firewalla_instance.create_target_list(name=name, targets=targets, category=category, notes=notes)
    assert response == mock_response
    mock_post.assert_called_once_with(
        "https://test_subdomain.firewalla.net/v2/target-lists",
        headers={
            "Authorization": "Token test_api_key",
            "Content-Type": "application/json"
        },
        json={"name": name, "targets": targets, "owner": None, "category": category, "notes": notes},
        timeout=10
    )

@patch('firewalla.requests.post')
def test_create_target_list_no_category(mock_post, firewalla_instance):
    mock_response = {"status": "created"}
    mock_post.return_value.json.return_value = mock_response
    mock_post.return_value.raise_for_status = lambda: None

    name = "New Target List"
    targets = ["example.com", "example.net"]
    owner = "user"
    notes = "Test notes"

    response = firewalla_instance.create_target_list(name=name, targets=targets, owner=owner, notes=notes)
    assert response == mock_response
    mock_post.assert_called_once_with(
        "https://test_subdomain.firewalla.net/v2/target-lists",
        headers={
            "Authorization": "Token test_api_key",
            "Content-Type": "application/json"
        },
        json={"name": name, "targets": targets, "owner": owner, "category": None, "notes": notes},
        timeout=10
    )

@patch('firewalla.requests.post')
def test_create_target_list_no_notes(mock_post, firewalla_instance):
    mock_response = {"status": "created"}
    mock_post.return_value.json.return_value = mock_response
    mock_post.return_value.raise_for_status = lambda: None

    name = "New Target List"
    targets = ["example.com", "example.net"]
    owner = "user"
    category = "test"

    response = firewalla_instance.create_target_list(name=name, targets=targets, owner=owner, category=category)
    assert response == mock_response
    mock_post.assert_called_once_with(
        "https://test_subdomain.firewalla.net/v2/target-lists",
        headers={
            "Authorization": "Token test_api_key",
            "Content-Type": "application/json"
        },
        json={"name": name, "targets": targets, "owner": owner, "category": category, "notes": None},
        timeout=10
    )
    
@patch('firewalla.requests.get')
def test_get_devices_no_params(mock_get, firewalla_instance):
    mock_response = {
        "results": [{"id": 1, "device": "Device 1"}, {"id": 2, "device": "Device 2"}]
    }
    mock_get.return_value.json.return_value = mock_response
    mock_get.return_value.raise_for_status = lambda: None

    response = firewalla_instance.get_devices()
    assert response == mock_response

@patch('firewalla.requests.get')
def test_get_devices_with_box(mock_get, firewalla_instance):
    mock_response = {
        "results": [{"id": 1, "device": "Device 1"}]
    }
    mock_get.return_value.json.return_value = mock_response
    mock_get.return_value.raise_for_status = lambda: None

    response = firewalla_instance.get_devices(box=1)
    assert response == mock_response

@patch('firewalla.requests.get')
def test_get_devices_with_group(mock_get, firewalla_instance):
    mock_response = {
        "results": [{"id": 1, "device": "Device 1"}]
    }
    mock_get.return_value.json.return_value = mock_response
    mock_get.return_value.raise_for_status = lambda: None

    response = firewalla_instance.get_devices(group="test_group")
    assert response == mock_response

@patch('firewalla.requests.get')
def test_get_devices_with_box_and_group(mock_get, firewalla_instance):
    mock_response = {
        "results": [{"id": 1, "device": "Device 1"}]
    }
    mock_get.return_value.json.return_value = mock_response
    mock_get.return_value.raise_for_status = lambda: None

    response = firewalla_instance.get_devices(box=1, group="test_group")
    assert response == mock_response
    
@patch('firewalla.requests.get')
def test_get_stats_no_type(mock_get, firewalla_instance):
    mock_response = {
        "results": [{"id": 1, "stat": "Stat 1"}, {"id": 2, "stat": "Stat 2"}]
    }
    mock_get.return_value.json.return_value = mock_response
    mock_get.return_value.raise_for_status = lambda: None

    params = {"group": 1, "limit": 10}
    response = firewalla_instance.get_stats(params=params)
    assert response == mock_response
    mock_get.assert_called_once_with(
        "https://test_subdomain.firewalla.net/v2/stats",
        headers={
            "Authorization": "Token test_api_key",
            "Content-Type": "application/json"
        },
        params=params,
        timeout=10
    )

@patch('firewalla.requests.get')
def test_get_stats_with_type(mock_get, firewalla_instance):
    mock_response = {
        "results": [{"id": 1, "stat": "Stat 1"}, {"id": 2, "stat": "Stat 2"}]
    }
    mock_get.return_value.json.return_value = mock_response
    mock_get.return_value.raise_for_status = lambda: None

    params = {"group": 1, "limit": 10}
    type = "topBoxesByBlockedFlows"
    response = firewalla_instance.get_stats(params=params, type=type)
    assert response == mock_response
    mock_get.assert_called_once_with(
        f"https://test_subdomain.firewalla.net/v2/stats/{type}",
        headers={
            "Authorization": "Token test_api_key",
            "Content-Type": "application/json"
        },
        params=params,
        timeout=10
    )

@patch('firewalla.requests.get')
def test_get_stats_no_group(mock_get, firewalla_instance):
    mock_response = {
        "results": [{"id": 1, "stat": "Stat 1"}, {"id": 2, "stat": "Stat 2"}]
    }
    mock_get.return_value.json.return_value = mock_response
    mock_get.return_value.raise_for_status = lambda: None

    params = {"limit": 10}
    response = firewalla_instance.get_stats(params=params)
    assert response == mock_response
    mock_get.assert_called_once_with(
        "https://test_subdomain.firewalla.net/v2/stats",
        headers={
            "Authorization": "Token test_api_key",
            "Content-Type": "application/json"
        },
        params=params,
        timeout=10
    )

@patch('firewalla.requests.get')
def test_get_stats_no_limit(mock_get, firewalla_instance):
    mock_response = {
        "results": [{"id": 1, "stat": "Stat 1"}, {"id": 2, "stat": "Stat 2"}]
    }
    mock_get.return_value.json.return_value = mock_response
    mock_get.return_value.raise_for_status = lambda: None

    params = {"group": 1}
    response = firewalla_instance.get_stats(params=params)
    assert response == mock_response
    mock_get.assert_called_once_with(
        "https://test_subdomain.firewalla.net/v2/stats",
        headers={
            "Authorization": "Token test_api_key",
            "Content-Type": "application/json"
        },
        params=params,
        timeout=10
    )
    
@patch('firewalla.requests.get')
def test_get_simple_stats(mock_get, firewalla_instance):
    mock_response = {
        "results": [{"id": 1, "stat": "Simple Stat 1"}, {"id": 2, "stat": "Simple Stat 2"}]
    }
    mock_get.return_value.json.return_value = mock_response
    mock_get.return_value.raise_for_status = lambda: None

    params = {"group": 1}
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

@patch('firewalla.requests.get')
def test_get_simple_stats_no_group(mock_get, firewalla_instance):
    mock_response = {
        "results": [{"id": 1, "stat": "Simple Stat 1"}, {"id": 2, "stat": "Simple Stat 2"}]
    }
    mock_get.return_value.json.return_value = mock_response
    mock_get.return_value.raise_for_status = lambda: None

    params = {}
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
    
@patch('firewalla.requests.get')
def test_get_flow_trends_no_group(mock_get, firewalla_instance):
    mock_response = {
        "results": [{"id": 1, "trend": "Flow Trend 1"}, {"id": 2, "trend": "Flow Trend 2"}]
    }
    mock_get.return_value.json.return_value = mock_response
    mock_get.return_value.raise_for_status = lambda: None

    response = firewalla_instance.get_flow_trends()
    assert response == mock_response
    mock_get.assert_called_once_with(
        "https://test_subdomain.firewalla.net/v2/trends/flows",
        headers={
            "Authorization": "Token test_api_key",
            "Content-Type": "application/json"
        },
        params={"group": None},
        timeout=10
    )

@patch('firewalla.requests.get')
def test_get_flow_trends_with_group(mock_get, firewalla_instance):
    mock_response = {
        "results": [{"id": 1, "trend": "Flow Trend 1"}]
    }
    mock_get.return_value.json.return_value = mock_response
    mock_get.return_value.raise_for_status = lambda: None

    response = firewalla_instance.get_flow_trends(group=1)
    assert response == mock_response
    mock_get.assert_called_once_with(
        "https://test_subdomain.firewalla.net/v2/trends/flows",
        headers={
            "Authorization": "Token test_api_key",
            "Content-Type": "application/json"
        },
        params={"group": 1},
        timeout=10
    )
    
@patch('firewalla.requests.get')
def test_get_alarm_trends_no_group(mock_get, firewalla_instance):
    mock_response = {
        "results": [{"id": 1, "trend": "Alarm Trend 1"}, {"id": 2, "trend": "Alarm Trend 2"}]
    }
    mock_get.return_value.json.return_value = mock_response
    mock_get.return_value.raise_for_status = lambda: None

    response = firewalla_instance.get_alarm_trends()
    assert response == mock_response
    mock_get.assert_called_once_with(
        "https://test_subdomain.firewalla.net/v2/trends/alarms",
        headers={
            "Authorization": "Token test_api_key",
            "Content-Type": "application/json"
        },
        params={"group": None},
        timeout=10
    )

@patch('firewalla.requests.get')
def test_get_alarm_trends_with_group(mock_get, firewalla_instance):
    mock_response = {
        "results": [{"id": 1, "trend": "Alarm Trend 1"}]
    }
    mock_get.return_value.json.return_value = mock_response
    mock_get.return_value.raise_for_status = lambda: None

    response = firewalla_instance.get_alarm_trends(group=1)
    assert response == mock_response
    mock_get.assert_called_once_with(
        "https://test_subdomain.firewalla.net/v2/trends/alarms",
        headers={
            "Authorization": "Token test_api_key",
            "Content-Type": "application/json"
        },
        params={"group": 1},
        timeout=10
    )
    
@patch('firewalla.requests.get')
def test_get_rule_trends_no_group(mock_get, firewalla_instance):
    mock_response = {
        "results": [{"id": 1, "trend": "Rule Trend 1"}, {"id": 2, "trend": "Rule Trend 2"}]
    }
    mock_get.return_value.json.return_value = mock_response
    mock_get.return_value.raise_for_status = lambda: None

    response = firewalla_instance.get_rule_trends()
    assert response == mock_response
    mock_get.assert_called_once_with(
        "https://test_subdomain.firewalla.net/v2/trends/rules",
        headers={
            "Authorization": "Token test_api_key",
            "Content-Type": "application/json"
        },
        params={"group": None},
        timeout=10
    )

@patch('firewalla.requests.get')
def test_get_rule_trends_with_group(mock_get, firewalla_instance):
    mock_response = {
        "results": [{"id": 1, "trend": "Rule Trend 1"}]
    }
    mock_get.return_value.json.return_value = mock_response
    mock_get.return_value.raise_for_status = lambda: None

    response = firewalla_instance.get_rule_trends(group=1)
    assert response == mock_response
    mock_get.assert_called_once_with(
        "https://test_subdomain.firewalla.net/v2/trends/rules",
        headers={
            "Authorization": "Token test_api_key",
            "Content-Type": "application/json"
        },
        params={"group": 1},
        timeout=10
    )
