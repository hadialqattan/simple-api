from app import models


def BASE_URL():
    """
    summary: return base_url
    """
    return "http://127.0.0.1:5057"


def URLs(integration: bool):
    """
    summary: return URLs dict (funName:url)

    arguments: (integration: bool [test type])
    """
    URLs = {
        "get_access_token": "/token",
        "GetMe": "/users/me/",
        "ListUsers": "/users",
        "GetAdmins": "/users/admins",
        "CreateUser": "/user",
        "GetUser": "/user/%s",
        "UpdateUser": "/user/%s/%s",
        "DeleteUser": "/user/%s",
        "List": "/configs",
        "Create": "/configs",
        "Get": "/configs/%s",
        "Update": "/configs/%s",
        "Delete": "/configs/%s",
        "Query": "/search/metadata.%s=%s",
    }
    if integration:
        bUrl = BASE_URL()
        for key, value in URLs.items():
            URLs[key] = bUrl + value
    return URLs


def INPUTS_USERS():
    """
    summary: return tests inputs for user testcase dict

    arguments: None

    return: Inputs dict 
    """
    return {
        "test_01_get_access_token_success": {
            "headers": {
                "accept": "application/json",
                "Content-Type": "application/x-www-form-urlencoded",
            },
            "admin": {
                "grant_type": "",
                "username": "admin",
                "password": "admin",
                "scope": "",
                "client_id": "",
                "client_secret": "",
            },
            "user2": {
                "grant_type": "",
                "username": "user2",
                "password": "user2pass",
                "scope": "",
                "client_id": "",
                "client_secret": "",
            },
        },
        "test_02_get_access_token_401": {
            "headers": {
                "accept": "application/json",
                "Content-Type": "application/x-www-form-urlencoded",
            },
            "data": {
                "grant_type": "",
                "username": "admin",
                "password": "401pass",
                "scope": "",
                "client_id": "",
                "client_secret": "",
            },
        },
        "test_03_GetMe_success": {
            "headers": {"accept": "application/json", "Authorization": "Bearer %s"}
        },
        "test_04_ListUsers_success": {
            "headers": {"accept": "application/json", "Authorization": "Bearer %s"}
        },
        "test_05_ListUsers_401": {
            "headers": {"accept": "application/json", "Authorization": "Bearer %s"}
        },
        "test_06_GetAdmins_success": {
            "headers": {"accept": "application/json", "Authorization": "Bearer %s"}
        },
        "test_07_GetAdmins_401": {
            "headers": {"accept": "application/json", "Authorization": "Bearer %s"}
        },
        "test_08_CreateUser_success": {
            "headers": {"accept": "application/json", "Authorization": "Bearer %s"},
            "json": {"username": "test08", "isadmin": True, "password": "test08pass"},
        },
        "test_09_CreateUser_401": {
            "headers": {"accept": "application/json", "Authorization": "Bearer %s"},
            "json": {"username": "test09", "isadmin": True, "password": "test09pass"},
        },
        "test_10_CreateUser_400": {
            "headers": {"accept": "application/json", "Authorization": "Bearer %s"},
            "json": {"username": "test08", "isadmin": True, "password": "test08pass"},
        },
        "test_11_GetUser_success": {
            "headers": {"accept": "application/json", "Authorization": "Bearer %s"},
            "name": "test08",
        },
        "test_12_GetUser_401": {
            "headers": {"accept": "application/json", "Authorization": "Bearer %s"},
            "name": "test08",
        },
        "test_13_GetUser_404": {
            "headers": {"accept": "application/json", "Authorization": "Bearer %s"},
            "name": "404user",
        },
        "test_14_UpdateUser_success": {
            "username": "test08",
            "set_admin": "False",
            "headers": {"accept": "application/json", "Authorization": "Bearer %s"},
        },
        "test_15_UpdateUser_401": {
            "username": "test08",
            "set_admin": "False",
            "headers": {"accept": "application/json", "Authorization": "Bearer %s"},
        },
        "test_16_UpdateUser_404": {
            "username": "404user",
            "set_admin": "False",
            "headers": {"accept": "application/json", "Authorization": "Bearer %s"},
        },
        "test_17_Delete_success": {
            "username": "test08",
            "headers": {"accept": "application/json", "Authorization": "Bearer %s"},
        },
        "test_18_Delete_401": {
            "username": "test08",
            "headers": {"accept": "application/json", "Authorization": "Bearer %s"},
        },
        "test_19_Delete_404": {
            "username": "404user",
            "headers": {"accept": "application/json", "Authorization": "Bearer %s"},
        },
    }


def OUTPUTS_USERS():
    """
    summary: return tests expected outputs for users testcase dict

    arguments: None

    return: Output dict
    """
    return {
        "test_01_get_access_token_success": {"status_code": 200},
        "test_02_get_access_token_401": {
            "status_code": 401,
            "json": {"detail": "Incorrect username or password"},
        },
        "test_03_GetMe_success": {
            "status_code": 200,
            "json": {"username": "admin", "isadmin": True, "configs": []},
        },
        "test_04_ListUsers_success": {
            "status_code": 200,
            "json": {
                "Users": [
                    {"username": "admin", "isadmin": True, "configs": []},
                    {"username": "user2", "isadmin": False, "configs": []},
                ]
            },
        },
        "test_05_ListUsers_401": {
            "status_code": 401,
            "json": {"detail": "Only admins can perform this function"},
        },
        "test_06_GetAdmins_success": {
            "status_code": 200,
            "json": {
                "Admins": [{"username": "admin", "isadmin": True, "configs": []},]
            },
        },
        "test_07_GetAdmins_401": {
            "status_code": 401,
            "json": {"detail": "Only admins can perform this function"},
        },
        "test_08_CreateUser_success": {
            "status_code": 200,
            "json": {"created": {"configs": [], "isadmin": True, "username": "test08"}},
        },
        "test_09_CreateUser_401": {
            "status_code": 401,
            "json": {"detail": "Only admins can perform this function"},
        },
        "test_10_CreateUser_400": {
            "status_code": 400,
            "json": {"detail": "username already exists"},
        },
        "test_11_GetUser_success": {
            "status_code": 200,
            "json": {"username": "test08", "isadmin": True, "configs": []},
        },
        "test_12_GetUser_401": {
            "status_code": 401,
            "json": {"detail": "Only admins can perform this function"},
        },
        "test_13_GetUser_404": {
            "status_code": 404,
            "json": {"detail": "The user doesn't exists"},
        },
        "test_14_UpdateUser_success": {
            "status_code": 200,
            "json": {"Updated": {"username": "test08", "isadmin": False}},
        },
        "test_15_UpdateUser_401": {
            "status_code": 401,
            "json": {"detail": "Only admins can perform this function"},
        },
        "test_16_UpdateUser_404": {
            "status_code": 404,
            "json": {"detail": "The user doesn't exists"},
        },
        "test_17_Delete_success": {
            "status_code": 200,
            "json": {"Deleted": {"username": "test08"}},
        },
        "test_18_Delete_401": {
            "status_code": 401,
            "json": {"detail": "Only admins can perform this function"},
        },
        "test_19_Delete_404": {
            "status_code": 404,
            "json": {"detail": "The user doesn't exists"},
        },
    }


def INPUTS_CONFIGS():
    """
    summary: return tests inputs for configs testcase dict

    arguments: None

    return: Inputs dict 
    """
    return {
        "test_00_create_access_token_for_admin_and_user2": {
            "headers": {
                "accept": "application/json",
                "Content-Type": "application/x-www-form-urlencoded",
            },
            "admin": {
                "grant_type": "",
                "username": "admin",
                "password": "admin",
                "scope": "",
                "client_id": "",
                "client_secret": "",
            },
            "user2": {
                "grant_type": "",
                "username": "user2",
                "password": "user2pass",
                "scope": "",
                "client_id": "",
                "client_secret": "",
            },
        },
        "test_01_List_success": {
            "headers": {"accept": "application/json", "Authorization": "Bearer %s"},
        },
        "test_02_List_success_owner": {
            "headers": {"accept": "application/json", "Authorization": "Bearer %s"},
            "owner": "user2",
        },
        "test_03_List_401": {
            "headers": {"accept": "application/json", "Authorization": "Bearer %s"},
            "owner": "notme",
        },
        "test_04_Create_success": {
            "headers": {"accept": "application/json", "Authorization": "Bearer %s"},
            "json": {
                "owner": "admin",
                "name": "api-3",
                "metadata": {
                    "name": "SimpleAPI",
                    "url": "http://127.0.0.1:5057",
                    "database": {
                        "name": "apidb",
                        "type": "sql",
                        "ms": "postgresql",
                        "host": "0.0.0.0",
                        "port": "5432",
                        "enabled": True,
                        "running": True,
                    },
                    "enabled": True,
                    "running": True,
                },
                "note": "everything is running.",
            },
        },
        "test_05_Create_400": {
            "headers": {"accept": "application/json", "Authorization": "Bearer %s"},
            "json": {
                "owner": "admin",
                "name": "api-3",
                "metadata": {
                    "name": "SimpleAPI",
                    "url": "http://127.0.0.1:5057",
                    "database": {
                        "name": "apidb",
                        "type": "sql",
                        "ms": "postgresql",
                        "host": "0.0.0.0",
                        "port": "5432",
                        "enabled": True,
                        "running": True,
                    },
                    "enabled": True,
                    "running": True,
                },
                "note": "everything is running.",
            },
        },
        "test_06_Get_success": {
            "headers": {"accept": "application/json", "Authorization": "Bearer %s"},
            "name": "api-1",
        },
        "test_07_Get_success_owner": {
            "headers": {"accept": "application/json", "Authorization": "Bearer %s"},
            "name": "api-1",
            "owner": "user2",
        },
        "test_08_Get_401": {
            "headers": {"accept": "application/json", "Authorization": "Bearer %s"},
            "name": "api-1",
            "owner": "notme",
        },
        "test_09_Get_404": {
            "headers": {"accept": "application/json", "Authorization": "Bearer %s"},
            "name": "404config",
            "owner": "user2",
        },
        "test_10_Update_success": {
            "headers": {"accept": "application/json", "Authorization": "Bearer %s"},
            "json": {
                "metadata": {
                    "name": "SimpleAPI",
                    "url": "http://127.0.0.1:5057",
                    "database": {
                        "name": "apidb",
                        "type": "sql",
                        "ms": "postgresql",
                        "host": "0.0.0.0",
                        "port": "5432",
                        "enabled": False,
                        "running": True,
                    },
                    "enabled": False,
                    "running": True,
                },
                "note": "every thing has disabled.",
                "name": "api-3",
                "owner": "admin",
            },
            "name": "api-3",
        },
        "test_11_Update_success_owner": {
            "headers": {"accept": "application/json", "Authorization": "Bearer %s"},
            "json": {
                "metadata": {
                    "name": "SimpleAPI",
                    "url": "http://127.0.0.1:5057",
                    "database": {
                        "name": "apidb",
                        "type": "sql",
                        "ms": "postgresql",
                        "host": "0.0.0.0",
                        "port": "5432",
                        "enabled": False,
                        "running": False,
                    },
                    "enabled": False,
                    "running": False,
                },
                "note": "every thing has disabeld and nothing is running.",
            },
            "test_12_Update_401": {
                "headers": {"accept": "application/json", "Authorization": "Bearer %s"},
                "json": {
                    "metadata": {
                        "name": "SimpleAPI",
                        "url": "http://127.0.0.1:5057",
                        "database": {
                            "name": "apidb",
                            "type": "sql",
                            "ms": "postgresql",
                            "host": "0.0.0.0",
                            "port": "5432",
                            "enabled": False,
                            "running": True,
                        },
                        "enabled": False,
                        "running": True,
                    },
                    "note": "every thing has disabled.",
                },
                "name": "api-3",
                "owner": "admin",
            },
            "test_13_Update_404": {
                "headers": {"accept": "application/json", "Authorization": "Bearer %s"},
                "json": {
                    "metadata": {
                        "name": "SimpleAPI",
                        "url": "http://127.0.0.1:5057",
                        "database": {
                            "name": "apidb",
                            "type": "sql",
                            "ms": "postgresql",
                            "host": "0.0.0.0",
                            "port": "5432",
                            "enabled": False,
                            "running": True,
                        },
                        "enabled": False,
                        "running": True,
                    },
                    "note": "every thing has disabled.",
                },
                "name": "404config",
                "owner": "admin",
            },
            "test_14_Delete_success": {
                "headers": {"accept": "application/json", "Authorization": "Bearer %s"},
                "name": "api-3",
            },
            "test_15_Delete_success_owner": {
                "headers": {"accept": "application/json", "Authorization": "Bearer %s"},
                "name": "api-2",
                "owner": "user2",
            },
            "test_16_Delete_401": {
                "headers": {"accept": "application/json", "Authorization": "Bearer %s"},
                "name": "doesnotmatter",
                "owner": "notme",
            },
            "test_17_Delete_404": {
                "headers": {"accept": "application/json", "Authorization": "Bearer %s"},
                "name": "404config",
                "owner": "404user",
            },
            "test_18_Query_success": {
                "headers": {"accept": "application/json", "Authorization": "Bearer %s"},
                "key": "database.enabled",
                "value": "True",
                "all": "False",
            },
            "test_19_Query_success_all": {
                "headers": {"accept": "application/json", "Authorization": "Bearer %s"},
                "key": "running",
                "value": "True",
                "all": "True",
            },
            "test_20_Query_success_owner": {
                "headers": {"accept": "application/json", "Authorization": "Bearer %s"},
                "key": "database.running",
                "value": "True",
                "all": "False",
                "owner": "admin",
            },
            "test_21_Query_401": {
                "headers": {"accept": "application/json", "Authorization": "Bearer %s"},
                "key": "database.running",
                "value": "True",
                "all": "True",
            },
        },
    }


def OUTPUTS_CONFIGS():
    """
    summary: return tests expected outputs for configs testcase dict

    arguments: None

    return: Output dict
    """
    return {
        "test_00_create_access_token_for_admin_and_user2": {"status_code": 200,},
        "test_01_List_success": {
            "status_code": 200,
            "json": {
                "Configs": [
                    {
                        "owner": "admin",
                        "name": "api-1",
                        "metadata": {
                            "name": "SimpleAPI",
                            "url": "http://127.0.0.1:5057",
                            "database": {
                                "name": "apidb",
                                "type": "sql",
                                "ms": "postgresql",
                                "host": "0.0.0.0",
                                "port": "5432",
                                "enabled": True,
                                "running": True,
                            },
                            "enabled": True,
                            "running": True,
                        },
                        "note": "The api has been enabled.",
                    },
                    {
                        "owner": "user2",
                        "name": "api-2",
                        "metadata": {
                            "name": "SimpleAPI",
                            "url": "http://127.0.0.1:5057",
                            "database": {
                                "name": "apidb",
                                "type": "sql",
                                "ms": "postgresql",
                                "host": "0.0.0.0",
                                "port": "5432",
                                "enabled": True,
                                "running": False,
                            },
                            "enabled": True,
                            "running": False,
                        },
                        "note": "The api has been enabled without the DB!",
                    },
                ]
            },
        },
        "test_02_List_success_owner": {
            "status_code": 200,
            "json": {
                "Configs": [
                    {
                        "owner": "user2",
                        "name": "api-2",
                        "metadata": {
                            "name": "SimpleAPI",
                            "url": "http://127.0.0.1:5057",
                            "database": {
                                "name": "apidb",
                                "type": "sql",
                                "ms": "postgresql",
                                "host": "0.0.0.0",
                                "port": "5432",
                                "enabled": True,
                                "running": False,
                            },
                            "enabled": True,
                            "running": False,
                        },
                        "note": "The api has been enabled without the DB!",
                    }
                ]
            },
        },
        "test_03_List_401": {
            "status_code": 401,
            "json": {"detail": "Only admins can perform this function"},
        },
        "test_04_Create_success": {
            "status_code": 200,
            "json": {
                "Created": {
                    "owner": "admin",
                    "name": "api-3",
                    "metadata": {
                        "name": "SimpleAPI",
                        "url": "http://127.0.0.1:5057",
                        "database": {
                            "name": "apidb",
                            "type": "sql",
                            "ms": "postgresql",
                            "host": "0.0.0.0",
                            "port": "5432",
                            "enabled": True,
                            "running": True,
                        },
                        "enabled": True,
                        "running": True,
                    },
                    "note": "everything is running.",
                }
            },
        },
        "test_05_Create_400": {
            "status_code": 400,
            "json": {"detail": "name already exists"},
        },
        "test_06_Get_success": {
            "status_code": 200,
            "json": {
                "owner": "admin",
                "name": "api-1",
                "metadata": {
                    "name": "SimpleAPI",
                    "url": "http://127.0.0.1:5057",
                    "database": {
                        "name": "apidb",
                        "type": "sql",
                        "ms": "postgresql",
                        "host": "0.0.0.0",
                        "port": "5432",
                        "enabled": True,
                        "running": True,
                    },
                    "enabled": True,
                    "running": True,
                },
                "note": "The api has been enabled.",
            },
            "test_07_Get_success_owner": {
                "status_code": 200,
                "json": {
                    "owner": "admin",
                    "name": "api-1",
                    "metadata": {
                        "name": "SimpleAPI",
                        "url": "http://127.0.0.1:5057",
                        "database": {
                            "name": "apidb",
                            "type": "sql",
                            "ms": "postgresql",
                            "host": "0.0.0.0",
                            "port": "5432",
                            "enabled": True,
                            "running": True,
                        },
                        "enabled": True,
                        "running": True,
                    },
                    "note": "The api has been enabled.",
                },
                "test_08_Get_401": {
                    "status_code": 401,
                    "json": {"detail": "Only admins can perform this function"},
                },
                "test_09_Get_404": {
                    "status_code": 404,
                    "json": {"detail": "name doesn't exists"},
                },
                "test_10_Update_success": {
                    "status_code": 200,
                    "json": {
                        "Update": {
                            "owner": "admin",
                            "name": "api-3",
                            "metadata": {
                                "name": "SimpleAPI",
                                "url": "http://127.0.0.1:5057",
                                "database": {
                                    "name": "apidb",
                                    "type": "sql",
                                    "ms": "postgresql",
                                    "host": "0.0.0.0",
                                    "port": "5432",
                                    "enabled": True,
                                    "running": True,
                                },
                                "enabled": True,
                                "running": True,
                            },
                            "note": "everything is running.",
                        }
                    },
                },
                "test_11_Update_success_owner": {
                    "status_code": 200,
                    "json": {
                        "Update": {
                            "owner": "admin",
                            "name": "api-3",
                            "metadata": {
                                "name": "SimpleAPI",
                                "url": "http://127.0.0.1:5057",
                                "database": {
                                    "name": "apidb",
                                    "type": "sql",
                                    "ms": "postgresql",
                                    "host": "0.0.0.0",
                                    "port": "5432",
                                    "enabled": True,
                                    "running": True,
                                },
                                "enabled": True,
                                "running": True,
                            },
                            "note": "everything is running.",
                        }
                    },
                },
                "test_12_Update_401": {
                    "status_code": 401,
                    "json": {"detail": "Only admins can perform this function"},
                },
                "test_13_Update_404": {
                    "status_code": 404,
                    "json": {"detail": "name doesn't exists"},
                },
                "test_14_Delete_success": {
                    "status_code": 200,
                    "json": {"Delete": {"owner": "admin", "name": "api-3"}},
                },
                "test_15_Delete_success_owner": {
                    "status_code": 200,
                    "json": {"Delete": {"owner": "user2", "name": "api-2"}},
                },
                "test_16_Delete_401": {
                    "status_code": 401,
                    "json": {"detail": "Only admins can perform this function"},
                },
                "test_17_Delete_404": {
                    "status_code": 404,
                    "json": {"detail": "name doesn't exists"},
                },
                "test_18_Query_success": {
                    "status_code": 200,
                    "json": {
                        "Configs": [
                            {
                                "owner": "admin",
                                "name": "api-1",
                                "metadata": {
                                    "name": "SimpleAPI",
                                    "url": "http://127.0.0.1:5057",
                                    "database": {
                                        "name": "apidb",
                                        "type": "sql",
                                        "ms": "postgresql",
                                        "host": "0.0.0.0",
                                        "port": "5432",
                                        "enabled": True,
                                        "running": True,
                                    },
                                    "enabled": True,
                                    "running": True,
                                },
                                "note": "The api has been enabled.",
                            }
                        ]
                    },
                },
                "test_19_Query_success_all": {
                    "status_code": 200,
                    "json": {
                        "Configs": [
                            {
                                "owner": "admin",
                                "name": "api-1",
                                "metadata": {
                                    "name": "SimpleAPI",
                                    "url": "http://127.0.0.1:5057",
                                    "database": {
                                        "name": "apidb",
                                        "type": "sql",
                                        "ms": "postgresql",
                                        "host": "0.0.0.0",
                                        "port": "5432",
                                        "enabled": True,
                                        "running": True,
                                    },
                                    "enabled": True,
                                    "running": True,
                                },
                                "note": "The api has been enabled.",
                            }
                        ]
                    },
                },
                "test_20_Query_success_owner": {
                    "status_code": 200,
                    "json": {
                        "Configs": [
                            {
                                "owner": "admin",
                                "name": "api-1",
                                "metadata": {
                                    "name": "SimpleAPI",
                                    "url": "http://127.0.0.1:5057",
                                    "database": {
                                        "name": "apidb",
                                        "type": "sql",
                                        "ms": "postgresql",
                                        "host": "0.0.0.0",
                                        "port": "5432",
                                        "enabled": True,
                                        "running": True,
                                    },
                                    "enabled": True,
                                    "running": True,
                                },
                                "note": "The api has been enabled.",
                            }
                        ]
                    },
                },
                "test_21_Query_401": {
                    "status_code": 401,
                    "json": {"detail": "Only admins can perform this function"},
                },
            },
        },
    }


def MOCK_USERS():
    """
    Mock db for users tests
    """
    return {
        "admin": models.User(
            **{"username": "admin", "password": "admin", "isadmin": True, "configs": []}
        ),
        "user2": models.User(
            **{
                "username": "user2",
                "password": "user2pass",
                "isadmin": False,
                "configs": [],
            }
        ),
        "test08": models.User(
            **{
                "username": "test08",
                "password": "test08pass",
                "isadmin": True,
                "configs": [],
            }
        ),
    }


def MOCK_CONFIGS():
    """
    Mock db for configs tests
    """
    return {
        "admin": models.User(
            **{"username": "admin", "password": "admin", "isadmin": True, "configs": []}
        ),
        "user2": models.User(
            **{
                "username": "user2",
                "password": "user2pass",
                "isadmin": False,
                "configs": [],
            }
        ),
        "api-1": models.Config(
            **{
                "owner": "admin",
                "name": "api-1",
                "metadatac": {
                    "name": "SimpleAPI",
                    "url": "http://127.0.0.1:5057",
                    "database": {
                        "name": "apidb",
                        "type": "sql",
                        "ms": "postgresql",
                        "host": "0.0.0.0",
                        "port": "5432",
                        "enabled": True,
                        "running": True,
                    },
                    "enabled": True,
                    "running": True,
                },
                "note": "The api has been enabled.",
            }
        ),
        "api-2": models.Config(
            **{
                "owner": "user2",
                "name": "api-2",
                "metadatac": {
                    "name": "SimpleAPI",
                    "url": "http://127.0.0.1:5057",
                    "database": {
                        "name": "apidb",
                        "type": "sql",
                        "ms": "postgresql",
                        "host": "0.0.0.0",
                        "port": "5432",
                        "enabled": True,
                        "running": False,
                    },
                    "enabled": True,
                    "running": False,
                },
                "note": "The api has been enabled without the DB!",
            }
        ),
        "api-3": models.Config(
            **{
                "owner": "admin",
                "name": "api-3",
                "metadata": {
                    "name": "SimpleAPI",
                    "url": "http://127.0.0.1:5057",
                    "database": {
                        "name": "apidb",
                        "type": "sql",
                        "ms": "postgresql",
                        "host": "0.0.0.0",
                        "port": "5432",
                        "enabled": True,
                        "running": True,
                    },
                    "enabled": True,
                    "running": True,
                },
                "note": "everything is running.",
            }
        ),
        "api-32": models.Config(
            **{
                "owner": "admin",
                "name": "api-3",
                "metadatac": {
                    "name": "SimpleAPI",
                    "url": "http://127.0.0.1:5057",
                    "database": {
                        "name": "apidb",
                        "type": "sql",
                        "ms": "postgresql",
                        "host": "0.0.0.0",
                        "port": "5432",
                        "enabled": False,
                        "running": True,
                    },
                    "enabled": False,
                    "running": True,
                },
                "note": "every thing has disabled.",
            }
        ),
        "api-33": models.Config(
            **{
                "owner": "admin",
                "name": "api-3",
                "metadatac": {
                    "name": "SimpleAPI",
                    "url": "http://127.0.0.1:5057",
                    "database": {
                        "name": "apidb",
                        "type": "sql",
                        "ms": "postgresql",
                        "host": "0.0.0.0",
                        "port": "5432",
                        "enabled": False,
                        "running": False,
                    },
                    "enabled": False,
                    "running": False,
                },
                "note": "every thing has disabeld and nothing is running.",
            }
        ),
    }
