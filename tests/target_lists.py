import pytest
from classes.target_lists import TargetLists

@pytest.fixture
def target_lists():
    api_key = "test_api_key"
    domain = "test_domain"
    return TargetLists(api_key, domain)

def test_get_target_lists(target_lists, requests_mock):
    url = "https://test_domain/v2/target_lists"
    requests_mock.get(url, json={"data": "test_data"})
    
    response = target_lists.get_target_lists()
    assert response == {"data": "test_data"}

def test_create_target_list(target_lists, requests_mock):
    url = "https://test_domain/v2/target_lists"
    requests_mock.post(url, json={"data": "test_data"})
    
    response = target_lists.create_target_list({"name": "test_list"})
    assert response == {"data": "test_data"}

def test__delete_target_list(target_lists, requests_mock):
    target_list_id = 1
    url = f"https://test_domain/v2/target_lists/{target_list_id}"
    requests_mock.delete(url, json={"data": "deleted"})
    
    response = target_lists.delete_target_list(target_list_id)
    assert response == {"data": "deleted"}
