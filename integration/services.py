import requests

# local import
from .constants import BASE_URL, QUERY_URL


def get_configs():
    """
    return get request response with base_url 
    """
    response = requests.get(BASE_URL)
    return response


def get_config(name: str):
    """
    return get request response with base_url + name
    """
    response = requests.get(BASE_URL + "/" + name)
    return response


def post_create_config(body: dict):
    """
    return post request response with base_url + body
    """
    response = requests.post(BASE_URL, json=body)
    return response


def put_update_config(name: str, metadata: dict):
    """
    return put request response with base_url + name + body 
    """
    response = requests.put(BASE_URL + "/" + name, json=metadata)
    return response


def delete_config(name: str):
    """
    return delete request response with base_url + name
    """
    response = requests.delete(BASE_URL + "/" + name)
    return response


def get_query(keys: list, value: str):
    """
    return get request response with query_url + query param as metadata.key=value
    """
    response = requests.get(QUERY_URL + "/metadata." + ".".join(keys) + "=" + value)
    return response
