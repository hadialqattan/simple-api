from nose.tools import assert_equal

# local import
from .services import (
    get_configs,
    get_config,
    post_create_config,
    put_update_config,
    delete_config,
    get_query,
)


# [list : GET : /configs] endpoint
def test_get_all_empty():
    """
    get all configs from empty table 
    """
    response = get_configs()
    assert_equal(response.status_code, 200)
    assert_equal(response.json(), {"Configs": "Empty"})


# [create : POST : /configs] endpoint
def test_create_config_success():
    """
    create new config (success case)
    """
    response = post_create_config(
        body={
            "name": "car",
            "metadata": {"speed": 15, "weight": "1000kg", "language": "english"},
        }
    )
    assert_equal(response.status_code, 200)
    assert_equal(
        response.json(),
        {
            "New config has created": {
                "name": "car",
                "metadata": {"speed": 15, "weight": "1000kg", "language": "english"},
            }
        },
    )


# [create : POST : /configs] endpoint
def test_create_config_name_already_exists():
    """ 
    create new config with exists name
    """
    response = post_create_config(
        body={
            "name": "car",
            "metadata": {"speed": 15, "weight": "1000kg", "language": "english"},
        }
    )
    assert_equal(response.status_code, 400)
    assert_equal(response.json(), {"detail": "name already exists"})


# [list : GET : /configs] endpoint
def test_get_all():
    """
    get all configs (success case)
    """
    response = get_configs()
    assert_equal(response.status_code, 200)
    assert_equal(
        response.json(),
        {
            "Configs": [
                {
                    "name": "car",
                    "metadata": {
                        "speed": 15,
                        "weight": "1000kg",
                        "language": "english",
                    },
                }
            ]
        },
    )


# [get : GET : /configs/{name}]
def test_get_config_by_name_success():
    """
    get config by name (success case)
    """
    response = get_config("car")
    assert_equal(response.status_code, 200)
    assert_equal(
        response.json(),
        {
            "Config": {
                "name": "car",
                "metadata": {"speed": 15, "weight": "1000kg", "language": "english"},
            }
        },
    )


# [get : GET : /configs/{name}]
def test_get_config_by_name_unexists_name():
    """
    get config by unexists name
    """
    response = get_config("ThisIsNotExists")
    assert_equal(response.status_code, 404)
    assert_equal(response.json(), {"detail": "name doesn't exists"})


# [update : PUT : /configs/{name}]
def test_update_config_by_name_success():
    """
    update config by name (success case)
    """
    response = put_update_config(
        "car", metadata={"speed": 150, "weight": "1000kg", "language": "arabic"}
    )
    assert_equal(response.status_code, 200)
    assert_equal(
        response.json(),
        {
            "The config has updated": {
                "name": "car",
                "metadata": {"speed": 150, "weight": "1000kg", "language": "arabic"},
            }
        },
    )


# [update : PUT : /configs/{name}]
def test_update_config_by_name_unexists_name():
    """
    update unexsists config by name 
    """
    response = put_update_config("ThisIsNotExists", metadata={"speed": 343})
    assert_equal(response.status_code, 404)
    assert_equal(response.json(), {"detail": "name doesn't exists"})


# [query : GET : /search?metadata.key=value]
def test_query_metadata_success():
    """
    query metadata by nested key and value (success case)
    """
    response = get_query(["language"], "arabic")
    assert_equal(response.status_code, 200)
    assert_equal(
        response.json(),
        {
            "Configs": [
                {
                    "name": "car",
                    "metadata": {
                        "speed": 150,
                        "weight": "1000kg",
                        "language": "arabic",
                    },
                }
            ]
        },
    )


# [delete : DELETE : /configs/{name}]
def test_delete_config_by_name_success():
    """ 
    delete config by name (success case)
    """
    response = delete_config("car")
    assert_equal(response.status_code, 200)
    assert_equal(response.json(), {"The config has deleted": {"name": "car"}})


# [delete : DELETE : /configs/{name}]
def test_delete_config_by_name_unexists_name():
    """ 
    delete unexists config by name
    """
    response = delete_config("ThisIsUnexists")
    assert_equal(response.status_code, 404)
    assert_equal(response.json(), {"detail": "name doesn't exists"})
