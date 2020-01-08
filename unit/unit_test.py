from starlette.testclient import TestClient
from unittest.mock import Mock, patch

# local import
from app.main import app
from app.models import Config


client = TestClient(app)


# [list : GET : /configs] endpoint
@patch("app.crud.get_configs")
def test_get_all_empty(mock):
    """
    get all configs from empty table 
    """
    mock.return_value = []
    response = client.get("/configs")
    assert response.status_code == 200
    assert response.json() == {"Configs": "Empty"}


# [create : POST : /configs] endpoint
@patch("app.crud.create_config")
def test_create_config_success(mock):
    """
    create new config (success case)
    """
    mock.return_value = [
        {
            "name": "car",
            "metadata": {"speed": "15", "weight": "1000kg", "language": "english"},
        }
    ]
    response = client.post(
        "/configs",
        json={
            "name": "car",
            "metadata": {"speed": "15", "weight": "1000kg", "language": "english"},
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "New config has created": {
            "name": "car",
            "metadata": {"speed": "15", "weight": "1000kg", "language": "english"},
        }
    }


# [create : POST : /configs] endpoint
@patch("app.crud.get_config")
def test_create_config_name_already_exists(mock):
    """ 
    create new config with exists name
    """
    mock.return_value = [{"name": "exists", "metadata": {"python": "3"}}]
    response = client.post(
        "/configs",
        json={
            "name": "car",
            "metadata": {"speed": "15", "weight": "1000kg", "language": "english"},
        },
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "name already exists"}


# [list : GET : /configs] endpoint
@patch("app.crud.get_configs")
def test_get_all(mock):
    """
    get all configs (success case)
    """
    mconfig = Config()
    mconfig.name = "car"
    mconfig.metadatac = {"speed": "15", "weight": "1000kg", "language": "english"}
    mock.return_value = [mconfig]
    response = client.get("/configs")
    assert response.status_code == 200
    assert response.json() == {
        "Configs": [
            {
                "name": "car",
                "metadata": {"speed": "15", "weight": "1000kg", "language": "english"},
            }
        ]
    }


# [get : GET : /configs/{name}]
@patch("app.crud.get_config")
def test_get_config_by_name_success(mock):
    """
    get config by name (success case)
    """
    mconfig = Config()
    mconfig.name = "car"
    mconfig.metadatac = {"speed": "15", "weight": "1000kg", "language": "english"}
    mock.return_value = mconfig
    response = client.get("/configs/car")
    assert response.status_code == 200
    assert response.json() == {
        "Config": {
            "name": "car",
            "metadata": {"speed": "15", "weight": "1000kg", "language": "english"},
        }
    }


# [get : GET : /configs/{name}]
@patch("app.crud.get_config")
def test_get_config_by_name_unexists_name(mock):
    """
    get config by unexists name
    """
    mock.return_value = False
    response = client.get("/configs/ThisIsNotExists")
    assert response.status_code == 404
    assert response.json() == {"detail": "name doesn't exists"}


# [update : PUT : /configs/{name}]
@patch("app.crud.update_config")
def test_update_config_by_name_success(mock):
    """
    update config by name (success case)
    """
    mock.return_value = [{"speed": "150", "weight": "1000kg", "language": "arabic"}]
    response = client.put(
        "/configs/car", json={"speed": "150", "weight": "1000kg", "language": "arabic"}
    )
    assert response.status_code == 200
    assert response.json() == {
        "The config has updated": {
            "name": "car",
            "metadata": {"speed": "150", "weight": "1000kg", "language": "arabic"},
        }
    }


# [update : PUT : /configs/{name}]
@patch("app.crud.update_config")
def test_update_config_by_name_unexists_name(mock):
    """
    update unexsists config by name 
    """
    mock.return_value = False
    response = client.put("/configs/ThisIsNotExists", json={"speed": 343})
    assert response.status_code == 404
    assert response.json() == {"detail": "name doesn't exists"}


# [delete : DELETE : /configs/{name}]
@patch("app.crud.delete_config")
def test_delete_config_by_name_success(mock):
    """
    delete config by name (success case)
    """
    mock.return_value = [{"name": "car"}]
    response = client.delete("/configs/car")
    assert response.status_code == 200
    assert response.json() == {"The config has deleted": {"name": "car"}}


# [query : GET : /search?metadata.key=value]
@patch("app.crud.query_metadata")
def test_query_metadata_success(mock):
    """
    query metadata by nested key and value (success case)
    """
    mconfig = Config()
    mconfig.name = "car"
    mconfig.metadatac = {"speed": 150, "weight": "1000kg", "language": "arabic"}
    mock.return_value = [mconfig]
    response = client.get("/search?metadata.language=arabic")
    assert response.status_code == 200
    assert response.json() == {
        "Configs": [
            {
                "name": "car",
                "metadata": {"speed": 150, "weight": "1000kg", "language": "arabic"},
            }
        ]
    }


# [query : GET : /search?metadata.key=value]
# @patch("app.crud.query_metadata")
def test_query_metadata_unproccessable_entity():
    """
    query metadata by nested key and value (422)
    """
    response = client.get("/search?metadata.key=value.value")
    assert response.status_code == 422
    assert response.json() == {
        "detail": "Unprocessable Entity, valid format: metadata.key=value"
    }
