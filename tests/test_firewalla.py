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
    assert response == mock_response["results"]

@patch('firewalla.requests.get')
def test_get_boxes_with_group(mock_get, firewalla_instance):
    mock_response = {
        "results": [{"id": 1, "name": "Box 1"}]
    }
    mock_get.return_value.json.return_value = mock_response
    mock_get.return_value.raise_for_status = lambda: None

    response = firewalla_instance.get_boxes(group=1)
    assert response == mock_response["results"]

@patch('firewalla.requests.get')
def test_get_alarms(mock_get, firewalla_instance):
    mock_response = {
        "results": [{"id": 1, "alarm": "Alarm 1"}, {"id": 2, "alarm": "Alarm 2"}]
    }
    mock_get.return_value.json.return_value = mock_response
    mock_get.return_value.raise_for_status = lambda: None

    response = firewalla_instance.get_alarms()
    assert response == mock_response["results"]

@patch('firewalla.requests.get')
def test_get_alarm(mock_get, firewalla_instance):
    mock_response = {
        "results": [{"id": 1, "alarm": "Alarm 1"}]
    }
    mock_get.return_value.json.return_value = mock_response
    mock_get.return_value.raise_for_status = lambda: None

    response = firewalla_instance.get_alarm(box_id="box1", alarm_id="alarm1")
    assert response == mock_response["results"]

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
    assert response == mock_response["results"]

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
    
@patch('firewalla.requests.post')
def test_post_rules_pause(mock_post, firewalla_instance):
    mock_response = {"status": "paused"}
    mock_post.return_value.json.return_value = mock_response
    mock_post.return_value.raise_for_status = lambda: None

    response = firewalla_instance._Firewalla__post_rules(endpoint="pause", id=1, query={"group": "foo", "limit": 10})
    assert response == mock_response
