from nose.tools import assert_is_not_none, assert_equal, assert_list_equal
from unittest.mock import Mock, patch

# local import 
from services import get_configs, get_config, post_create_config, put_update_config, delete_config


# [list : GET : /configs] endpoint
@patch('tests.services.requests.get')
def test_get_all_empty(mock_get):
    """
    get all configs from empty table 
    """
    jsonres = [{"Configs":"Empty"}]
    mock_get.return_value.ok = True
    mock_get.return_value.json.return_value = jsonres
    response = get_configs()
    assert_is_not_none(response)
    assert_list_equal(response.json(), jsonres)


# [create : POST : /configs] endpoint
@patch('tests.services.requests.post')
def test_create_config_success(mock_post):
    """
    create new config (success case)
    """
    jsonres = [{"New config has created":{'name':'car', 'metadata':{'speed':15, 'weight': '1000kg', 'language':'english'}}}]
    mock_post.return_value.ok = True
    mock_post.return_value.json.return_value = jsonres
    response = post_create_config(body={'name':'car', 'metadata':{'speed':15, 'weight': '1000kg', 'language':'english'}})
    assert_is_not_none(response)
    assert_list_equal(response.json(), jsonres)


# [create : POST : /configs] endpoint
@patch('tests.services.requests.post')
def test_create_config_name_already_exists(mock_post):
    """ 
    create new config with exists name
    """
    jsonres = [{"detail":"name already exists"}]
    mock_post.return_value.ok = True
    mock_post.return_value.json.return_value = jsonres
    response = post_create_config(body={'name':'car', 'metadata':{'speed':15, 'weight': '1000kg', 'language':'english'}})
    assert_is_not_none(response)
    assert_list_equal(response.json(), jsonres)


# [list : GET : /configs] endpoint
@patch('tests.services.requests.get')
def test_get_all(mock_get):
    """
    get all configs (success case)
    """
    jsonres = [{"Configs":[{'name':'car', 'metadata':{'speed':15, 'weight': '1000kg', 'language':'english'}}]}]
    mock_get.return_value.ok = True
    mock_get.return_value.json.return_value = jsonres
    response = get_configs()
    assert_is_not_none(response)
    assert_list_equal(response.json(), jsonres)


# [get : GET : /configs/{name}]
@patch('tests.services.requests.get')
def test_get_config_by_name_success(mock_get):
    """
    get config by name (success case)
    """
    jsonres = [{"Config":{'name':'car', 'metadata':{'speed':15, 'weight': '1000kg', 'language':'english'}}}]
    mock_get.return_value.ok = True
    mock_get.return_value.json.return_value = jsonres
    response = get_config('car')
    assert_is_not_none(response)
    assert_list_equal(response.json(), jsonres)


# [get : GET : /configs/{name}]
@patch('tests.services.requests.get')
def test_get_config_by_name_unexists_name(mock_get):
    """
    get config by unexists name
    """
    jsonres = [{"detail":"name doesn't exists"}]
    mock_get.return_value.ok = True
    mock_get.return_value.json.return_value = jsonres
    response = get_config('ThisIsNotExists')
    assert_is_not_none(response)
    assert_list_equal(response.json(), jsonres)


# [update : PUT : /configs/{name}]
@patch('tests.services.requests.put')
def test_update_config_by_name_success(mock_put):
    """
    update config by name (success case)
    """
    jsonres = [{"The config has updated":{'name':'car', 'metadata':{'speed':150, 'weight': '1000kg', 'language':'arabic'}}}]
    mock_put.return_value.ok = True
    mock_put.return_value.json.return_value = jsonres
    response = put_update_config('car', metadata={'speed':150, 'weight': '1000kg', 'language':'arabic'})
    assert_is_not_none(response)
    assert_list_equal(response.json(), jsonres)


# [update : PUT : /configs/{name}]
@patch('tests.services.requests.put')
def test_update_config_by_name_unexists_name(mock_put):
    """
    update unexsists config by name 
    """
    jsonres = [{"detail":"name doesn't exists"}]
    mock_put.return_value.ok = True
    mock_put.return_value.json.return_value = jsonres
    response = put_update_config('ThisIsNotExists', metadata={'speed':343})
    assert_is_not_none(response)
    assert_list_equal(response.json(), jsonres)


# [delete : DELETE : /configs/{name}]
@patch('tests.services.requests.delete')
def test_delete_config_by_name_success(mock_delete):
    """ 
    delete config by name (success case)
    """
    jsonres = [{"The config has deleted": {"name":"car"}}]
    mock_delete.return_value.ok = True
    mock_delete.return_value.json.return_value = jsonres
    response = delete_config('car')
    assert_is_not_none(response)
    assert_list_equal(response.json(), jsonres)


# [delete : DELETE : /configs/{name}]
@patch('tests.services.requests.delete')
def test_delete_config_by_name_unexists_name(mock_delete):
    """ 
    delete unexists config by name
    """
    jsonres = [{"detail":"name doesn't exists"}]
    mock_delete.return_value.ok = True
    mock_delete.return_value.json.return_value = jsonres
    response = delete_config('ThisIsUnexists')
    assert_is_not_none(response)
    assert_list_equal(response.json(), jsonres)


# clean the DB
def pytest_sessionfinish(session, exitstatus):
    """
    clean the Database after unit test
    """
    from app.main import Depends, get_db
    from app import models
    db = Depends(get_db)
    db.query(models.Config).delete()
