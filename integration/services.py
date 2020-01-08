from urllib.parse import urljoin
import requests

# local import
from .constants import BASE_URL, QUERY_URL


def get_configs():
    """
    return get request response with base_url 
    """
    response = requests.get(BASE_URL)
    return response if response.ok else None


def get_config(name: str):
    """
    return get request response with base_url + name
    """
    response = requests.get(urljoin(BASE_URL, name))
    return response if response.ok else None


def post_create_config(body: dict):
    """
    return post request response with base_url + body
    """
    response = requests.post(BASE_URL, json=body)
    return response if response.ok else None


def put_update_config(name: str, metadata: dict):
    """
    return put request response with base_url + name + body 
    """
    response = requests.put(urljoin(BASE_URL, name), json=metadata)
    return response if response.ok else None


def delete_config(name: str):
    """
    return delete request response with base_url + name
    """
    response = requests.delete(urljoin(BASE_URL, name))
    return response if response.ok else None


def get_query(keys: list, value: str):
    """
    return get request response with query_url + query param as metadata.key=value
    """
    response = requests.get(QUERY_URL + "?" + "metadata" + ".".join(keys) + "=" + value)
    return response if response.ok else None
