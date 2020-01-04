from starlette.testclient import TestClient

# local import 
from app.main import app


client = TestClient(app)


# [list : GET : /configs] endpoint
def test_get_all_empty():
    """
    get all configs from empty table 
    """
    response = client.get('/configs')
    assert response.status_code == 200
    assert response.json() == {"Configs":"Empty"}


# [create : POST : /configs] endpoint
def test_create_config_success():
    """
    create new config (success case)
    """
    response = client.post('/configs', json={'name':'car', 'metadata':{'speed':"15", 'weight': '1000kg', 'language':'english'}})
    assert response.status_code == 200
    assert response.json() == {"New config has created":{'name':'car', 'metadata':{'speed':"15", 'weight': '1000kg', 'language':'english'}}}


# [create : POST : /configs] endpoint
def test_create_config_name_already_exists():
    """ 
    create new config with exists name
    """
    response = client.post('/configs', json={'name':'car', 'metadata':{'speed':"15", 'weight': '1000kg', 'language':'english'}})
    assert response.status_code == 400
    assert response.json() == {"detail":"name already exists"}


# [list : GET : /configs] endpoint
def test_get_all():
    """
    get all configs (success case)
    """
    response = client.get('/configs')
    assert response.status_code == 200
    assert response.json() == {"Configs":[{'name':'car', 'metadata':{'speed':"15", 'weight': '1000kg', 'language':'english'}}]}


# [get : GET : /configs/{name}]
def test_get_config_by_name_success():
    """
    get config by name (success case)
    """
    response = client.get('/configs/car')
    assert response.status_code == 200 
    assert response.json() == {"Config":{'name':'car', 'metadata':{'speed':"15", 'weight': '1000kg', 'language':'english'}}}


# [get : GET : /configs/{name}]
def test_get_config_by_name_unexists_name():
    """
    get config by unexists name
    """
    response = client.get('/configs/ThisIsNotExists')
    assert response.status_code == 404
    assert response.json() == {"detail":"name doesn't exists"}


# [update : PUT : /configs/{name}]
def test_update_config_by_name_success():
    """
    update config by name (success case)
    """
    response = client.put('/configs/car', json={'speed':"150", 'weight': '1000kg', 'language':'arabic'})
    assert response.status_code == 200
    assert response.json() == {"The config has updated":{'name':'car', 'metadata':{'speed':"150", 'weight': '1000kg', 'language':'arabic'}}}


# [update : PUT : /configs/{name}]
def test_update_config_by_name_unexists_name():
    """
    update unexsists config by name 
    """
    response = client.put('/configs/ThisIsNotExists', json={'speed':343})
    assert response.status_code == 404
    assert response.json() == {"detail":"name doesn't exists"}


# [delete : DELETE : /configs/{name}]
def test_delete_config_by_name_success():
    """ 
    delete config by name (success case)
    """
    response = client.delete('/configs/car')
    assert response.status_code == 200
    assert response.json() == {"The config has deleted": {"name":"car"}}


# [delete : DELETE : /configs/{name}]
def test_delete_config_by_name_unexists_name():
    """ 
    delete unexists config by name
    """
    response = client.delete('/configs/ThisIsUnexists')
    assert response.status_code == 404
    assert response.json() == {"detail":"name doesn't exists"}

