# SimpleAPI
![](https://github.com/HadiZakiAlQattan/simple-api/workflows/SimpleAPI%28CI%2FCD%29/badge.svg) <a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>

#### SimpleAPI is a restful API provids simple service that stores and returns configurations with simple jwt authentication using FastAPI and PostgreSQL.

<br>

# Project structure
```shell
.
├── app/
├── gcp/
├── tests/
│   ├── unit/
│   ├── integration/
│   └── tests_runner.sh
├── Dockerfile
├── docker-compose.yml
└── .env
``` 

- app/ contains the entire API :
  - [Users endpoints](#users)
  - [Configs endpoints](#configs)

- gcp/ contains GCP Kubernetes deployment *.yml files -> [GCP deployment](#deployment)

- tests/ contains the entire CI tests : -> [run instructions](#tests)
  - unit/
  - integration/ 
  - `tests_runner.sh` full automated script aim to run tests inside docker container.

- Dockerfile & docker-compose -> [Dockerizing](#deployment)

- .env contains env vars include (app & db) (host & port).

<br>

# Endpoints and schemas

## Users
Default admin user will created automatically if there's no admin in the DB :->(username=admin, password=admin, isadmin=true)

| Name   | Method      | URL
| ---    | ---         | ---
| get_access_token       | `POST` |  `/token`
| GetMe       | `GET` | `/users/me/`
| ListUsers   | `GET` | `/users` 
| GetAdmins   | `GET` | `/users/admins`
| CreateUser | `POST` | `/user` 
| GetUser    | `GET` | `/user/{name}` 
| UpdateUser | `PUT` | `/user/{name}` 
| DeleteUser | `DELETE` | `/user/{name}`

#### Schema

* **User**
  + username (string of length no more than 50 characters)
  + password (password hash - string - of length no more than 80 characters)
  + isadmin (boolean value)
  + configs (relationship with user configs in configs table)

<br>

---

## `get_access_token POST /token`

### Request
```shell 
$ curl -X POST "http://127.0.0.1:5057/token" -H "accept: application/json" -H "Content-Type: application/x-www-form-urlencoded" -d "grant_type=&username=admin&password=admin&scope=&client_id=&client_secret="
```

### Response
```shell 
200 ok
________________________________________________________

content-length: 165 
content-type: application/json 
date: Fri, 31 Jan 2020 11:14:38 GMT 
server: uvicorn 
________________________________________________________

{
"access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTU4MDQ3MTA3OX0.Dy2-LeV7OWeffE-SneTAYYvgxmbjcSET4lWy2XKMJx0",
"token_type": "bearer"
}
```

---
## `GetMe GET /users/me`

### Request
```shell 
$ curl -X GET "http://127.0.0.1:5057/users/me/" -H "accept: application/json" -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTU4MDQ3MTQ1NX0.AVrdoL2hIBGsiPJ6AisO-5jL1XgL-Q-IEMLkofsd0g8"
```

### Response
```shell 
200 ok
________________________________________________________

content-length: 48 
content-type: application/json 
date: Fri, 31 Jan 2020 11:21:04 GMT 
server: uvicorn 
________________________________________________________

{
  "username": "admin",
  "isadmin": true,
  "configs": []
}
```
---
## `ListUsers GET /users`

### Request (:: admin permission required)
```shell 
$ curl -X GET "http://127.0.0.1:5057/users" -H "accept: application/json" -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTU4MDQ3MTQ1NX0.AVrdoL2hIBGsiPJ6AisO-5jL1XgL-Q-IEMLkofsd0g8"
```

### Response (:: admin permission required)
```shell 
200 ok
________________________________________________________

content-length: 60 
content-type: application/json 
date: Fri, 31 Jan 2020 11:22:04 GMT 
server: uvicorn 
________________________________________________________

{
  "Users": [
    {
      "username": "admin",
      "isadmin": true,
      "configs": []
    }
  ]
}
```

---
## `GetAdmins GET /users/admins`

### Request (:: admin permission required)
```shell 
$ curl -X GET "http://127.0.0.1:5057/users/admins" -H "accept: application/json" -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTU4MDQ3MTQ1NX0.AVrdoL2hIBGsiPJ6AisO-5jL1XgL-Q-IEMLkofsd0g8"
```

### Response (:: admin permission required)
```shell 
200 ok
________________________________________________________

content-length: 61 
content-type: application/json 
date: Fri, 31 Jan 2020 11:22:49 GMT 
server: uvicorn 
________________________________________________________

{
  "Admins": [
    {
      "username": "admin",
      "isadmin": true,
      "configs": []
    }
  ]
}
```
---
## `CreateUser POST /user`

### Request (:: admin permission required)
```shell 
$ curl -X POST "http://127.0.0.1:5057/user" -H "accept: application/json" -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTU4MDQ3MTQ1NX0.AVrdoL2hIBGsiPJ6AisO-5jL1XgL-Q-IEMLkofsd0g8" -H "Content-Type: application/json" -d "{\"username\":\"user2\",\"isadmin\":true,\"password\":\"user2pass\"}"
```

### Response (:: admin permission required)
```shell 
200 ok
________________________________________________________

content-length: 60 
content-type: application/json 
date: Fri, 31 Jan 2020 11:24:03 GMT 
server: uvicorn 
________________________________________________________

{
  "created": {
    "username": "user2",
    "isadmin": true,
    "configs": []
  }
}
```
---
## `GetUser GET /user/{name}`

### Request (:: admin permission required)
```shell 
$ curl -X GET "http://127.0.0.1:5057/user/user2" -H "accept: application/json" -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTU4MDQ3MTQ1NX0.AVrdoL2hIBGsiPJ6AisO-5jL1XgL-Q-IEMLkofsd0g8"
```

### Response (:: admin permission required)
```shell 
200 ok
________________________________________________________

content-length: 48 
content-type: application/json 
date: Fri, 31 Jan 2020 11:24:48 GMT 
server: uvicorn 
________________________________________________________

{
  "username": "user2",
  "isadmin": true,
  "configs": []
}
```
---
## `UpdateUser PUT /user/{name}`

### Request (:: admin permission required)
```shell 
$ curl -X PUT "http://127.0.0.1:5057/user/user2/false" -H "accept: application/json" -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTU4MDQ3MTQ1NX0.AVrdoL2hIBGsiPJ6AisO-5jL1XgL-Q-IEMLkofsd0g8"
```

### Response (:: admin permission required)
```shell 
200 ok
________________________________________________________

content-length: 48 
content-type: application/json 
date: Fri, 31 Jan 2020 11:25:36 GMT 
server: uvicorn
________________________________________________________

{
  "Updated": {
    "username": "user2",
    "isadmin": false
  }
}
```
---
## `DeleteUser DELETE /user/{name}`

### Request (:: admin permission required)
```shell 
$ curl -X DELETE "http://127.0.0.1:5057/user/user2" -H "accept: application/json" -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTU4MDQ3MTQ1NX0.AVrdoL2hIBGsiPJ6AisO-5jL1XgL-Q-IEMLkofsd0g8"
```

### Response (:: admin permission required)
```shell 
200 ok
________________________________________________________

content-length: 32 
content-type: application/json 
date: Fri, 31 Jan 2020 11:26:21 GMT 
server: uvicorn
________________________________________________________

{
  "Deleted": {
    "username": "user2"
  }
}
```
---
<br>

## Configs

| Name   | Method      | URL
| ---    | ---         | ---
| List   | `GET` | `/configs` 
| Create | `POST` | `/configs` 
| Get    | `GET` | `/configs/{name}` 
| Update | `PUT` | `/configs/{name}` 
| Delete | `DELETE` | `/configs/{name}`
| Query  | `GET`  | `/search/metadata.key=value`

#### Schema

* **Config**
  + id (integer auto increment)
  + owner (foreign key of user.username - string - of length no more than 50 characters)
  + name (string of length no more than 120 characters)
  + metadata (nested key:value pairs where both key and value are strings of length no more than 160 characters)
  + note (string of arbitrary length)

<br>

---
## `List GET /configs` 

### Request (without 'owner' query param :: without admin permission)
```shell 
$ curl -X GET "http://127.0.0.1:5057/configs" -H "accept: application/json" -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1c2VyMiIsImV4cCI6MTU4MDQ3MjYyOX0.4hdblMjb51nWQ9C6gO_4AzTvMZS4P9VJsVqq8omFFq8"
```

### Response (without 'owner' query param :: without admin permission)
```shell 
200 ok
________________________________________________________

content-length: 186 
content-type: application/json 
date: Fri, 31 Jan 2020 11:40:35 GMT 
server: uvicorn 
________________________________________________________

{
  "Configs": [
    {
      "owner": "user2",
      "name": "datacenter-2",
      "metadata": {
        "limits": {
          "cpu": {
            "value": "250m",
            "enabled": "true"
          }
        },
        "monitoring": {
          "enabled": "true"
        }
      },
      "note": "the cpu has already enabled"
    }
  ]
}
```

### Request (without 'owner' query param :: with admin permission)
```shell 
$ curl -X GET "http://127.0.0.1:5057/configs" -H "accept: application/json" -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTU4MDQ3MjE3Nn0.irXQwbe9ZuHHiH3mZqVXrgdjZMYj6Xn9AdBLQTGBltQ"
```

### Response (without 'owner' query param :: with admin permission)
```shell 
200 ok
________________________________________________________

content-length: 360 
content-type: application/json 
date: Fri, 31 Jan 2020 11:34:52 GMT 
server: uvicorn
________________________________________________________

{
  "Configs": [
    {
      "owner": "admin",
      "name": "datacenter-1",
      "metadata": {
        "limits": {
          "cpu": {
            "value": "300m",
            "enabled": "false"
          }
        },
        "monitoring": {
          "enabled": "true"
        }
      },
      "note": "the cpu has not enabled yet"
    },
    {
      "owner": "user2",
      "name": "datacenter-2",
      "metadata": {
        "limits": {
          "cpu": {
            "value": "250m",
            "enabled": "true"
          }
        },
        "monitoring": {
          "enabled": "true"
        }
      },
      "note": "the cpu has already enabled"
    }
  ]
}
```

### Request (with 'owner' query param :: admin permission required)
```shell 
$ curl -X GET "http://127.0.0.1:5057/configs?owner=admin" -H "accept: application/json" -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTU4MDQ3MjE3Nn0.irXQwbe9ZuHHiH3mZqVXrgdjZMYj6Xn9AdBLQTGBltQ"
```

### Response (with 'owner' query param :: admin permission required)
```shell 
200 ok
________________________________________________________

content-length: 187 
content-type: application/json 
date: Fri, 31 Jan 2020 11:38:25 GMT 
server: uvicorn 
________________________________________________________

{
  "Configs": [
    {
      "owner": "admin",
      "name": "datacenter-1",
      "metadata": {
        "limits": {
          "cpu": {
            "value": "300m",
            "enabled": "false"
          }
        },
        "monitoring": {
          "enabled": "true"
        }
      },
      "note": "the cpu has not enabled yet"
    }
  ]
}
```

---

## `Create POST /configs` 

### Request
```shell 
$ curl -X POST "http://127.0.0.1:5057/configs" -H "accept: application/json" -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTU4MDQ3MTQ1NX0.AVrdoL2hIBGsiPJ6AisO-5jL1XgL-Q-IEMLkofsd0g8" -H "Content-Type: application/json" -d "{\"owner\":\"admin\",\"note\":\"the cpu has not enabled yet\",\"name\":\"datacenter-1\",\"metadata\":{\"monitoring\":{\"enabled\":\"true\"},\"limits\":{\"cpu\":{\"enabled\":\"false\",\"value\":\"300m\"}}}}"
```

### Response
```shell 
200 ok
________________________________________________________

content-length: 185 
content-type: application/json 
date: Fri, 31 Jan 2020 11:30:57 GMT 
server: uvicorn 
________________________________________________________

{
  "Created": {
    "owner": "admin",
    "name": "datacenter-1",
    "metadata": {
      "limits": {
        "cpu": {
          "value": "300m",
          "enabled": "false"
        }
      },
      "monitoring": {
        "enabled": "true"
      }
    },
    "note": "the cpu has not enabled yet"
  }
}
```

---

## `Get GET /configs/{name}` 

### Request (without owner query param)
```shell 
$ curl -X GET "http://127.0.0.1:5057/configs/datacenter-1" -H "accept: application/json" -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1c2VyMiIsImV4cCI6MTU4MDQ3MjYyOX0.4hdblMjb51nWQ9C6gO_4AzTvMZS4P9VJsVqq8omFFq8"
```

### Response (without owner query param)
```shell 
200 ok
________________________________________________________

content-length: 173 
content-type: application/json 
date: Fri, 31 Jan 2020 11:44:12 GMT 
server: uvicorn 
________________________________________________________

{
  "metadata": {
    "limits": {
      "cpu": {
        "value": "300m",
        "enabled": "false"
      }
    },
    "monitoring": {
      "enabled": "true"
    }
  },
  "note": "the cpu has not enabled yet",
  "owner": "admin",
  "name": "datacenter-1"
}
```

### Request (with owner query param :: admin permission required)
```shell 
$ curl -X GET "http://127.0.0.1:5057/configs/datacenter-2?owner=user2" -H "accept: application/json" -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTU4MDQ3MjkwN30.-zj87zhB_bJLVNKvdvPKGtp1tjaQYQ_isNH-QzcymmU"
```

### Response (with owner query param :: admin permission required)
```shell 
200 ok
________________________________________________________

content-length: 172 
content-type: application/json 
date: Fri, 31 Jan 2020 11:45:05 GMT 
server: uvicorn 
________________________________________________________

{
  "metadata": {
    "limits": {
      "cpu": {
        "value": "250m",
        "enabled": "true"
      }
    },
    "monitoring": {
      "enabled": "true"
    }
  },
  "note": "the cpu has already enabled",
  "owner": "user2",
  "name": "datacenter-2"
}
```

---

## `Update UPDATE /configs/{name}` 

### Request (without owner query param)
```shell 
$ curl -X PUT "http://127.0.0.1:5057/configs/datacenter-1" -H "accept: application/json" -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTU4MDQ3MjkwN30.-zj87zhB_bJLVNKvdvPKGtp1tjaQYQ_isNH-QzcymmU" -H "Content-Type: application/json" -d "{\"metadata\":{\"monitoring\":{\"enabled\":\"true\"},\"limits\":{\"cpu\":{\"enabled\":\"true\",\"value\":\"300m\"}}},\"note\":\"the cpu has enabled\"}"
```

### Response (without owner query param)
```shell 
200 ok
________________________________________________________

content-length: 175 
content-type: application/json 
date: Fri, 31 Jan 2020 11:51:25 GMT 
server: uvicorn 
________________________________________________________

{
  "Update": {
    "owner": "admin",
    "name": "datacenter-1",
    "metadata": {
      "limits": {
        "cpu": {
          "value": "300m",
          "enabled": "true"
        }
      },
      "monitoring": {
        "enabled": "true"
      }
    },
    "note": "the cpu has enabled"
  }
}
```

### Request (without owner query param :: admin permission required)
```shell 
$ curl -X PUT "http://127.0.0.1:5057/configs/datacenter-2?owner=user2" -H "accept: application/json" -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTU4MDQ3MjkwN30.-zj87zhB_bJLVNKvdvPKGtp1tjaQYQ_isNH-QzcymmU" -H "Content-Type: application/json" -d "{\"metadata\":{\"monitoring\":{\"enabled\":\"true\"},\"limits\":{\"cpu\":{\"enabled\":\"false\",\"value\":\"250m\"}}},\"note\":\"the cpu has disabled\"}"
```

### Response (without owner query param :: admin permission required)
```shell 
200 ok
________________________________________________________

content-length: 177 
content-type: application/json 
date: Fri, 31 Jan 2020 11:53:50 GMT 
server: uvicorn 
________________________________________________________

{
  "Update": {
    "owner": "user2",
    "name": "datacenter-2",
    "metadata": {
      "limits": {
        "cpu": {
          "value": "250m",
          "enabled": "false"
        }
      },
      "monitoring": {
        "enabled": "true"
      }
    },
    "note": "the cpu has disabled"
  }
}
```

---

## `Delete DELETE /configs/{name}` 

### Request (without owner query param)
```shell 
$ curl -X DELETE "http://127.0.0.1:5057/configs/datacenter-1" -H "accept: application/json" -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTU4MDQ3Mzc0MH0.QaxTlU-1dJQGO_GpTTjJvSeuDnAdSkut0wkP3sHeTfM"
```

### Response (without owner query param)
```shell 
200 ok
________________________________________________________

content-length: 50 
content-type: application/json 
date: Fri, 31 Jan 2020 12:05:02 GMT 
server: uvicorn 
________________________________________________________

{
  "Delete": {
    "owner": "admin",
    "name": "datacenter-1"
  }
}
```

### Request (with admin query param :: admin permission required)
```shell 
$ curl -X DELETE "http://127.0.0.1:5057/configs/datacenter-2?owner=user2" -H "accept: application/json" -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTU4MDQ3Mzc0MH0.QaxTlU-1dJQGO_GpTTjJvSeuDnAdSkut0wkP3sHeTfM"
```

### Response (with admin query :: admin permission required)
```shell 
200 ok
________________________________________________________

content-length: 50 
content-type: application/json 
date: Fri, 31 Jan 2020 12:06:30 GMT 
server: uvicorn 
________________________________________________________

{
  "Delete": {
    "owner": "user2",
    "name": "datacenter-2"
  }
}
```
---
## `Query GET /search/metadata.key=value` 

### Request (without owner query param :: all query param => default value = false)
```shell 
$ curl -X GET "http://127.0.0.1:5057/search/metadata.monitoring.enabled=true" -H "accept: application/json" -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTU4MDQ3Mzc0MH0.QaxTlU-1dJQGO_GpTTjJvSeuDnAdSkut0wkP3sHeTfM"
```

### Response (without owner query param :: all query param => default value = false)
```shell 
200 ok
________________________________________________________

content-length: 178 
content-type: application/json 
date: Fri, 31 Jan 2020 11:56:22 GMT 
server: uvicorn 
________________________________________________________

{
  "Configs": [
    {
      "owner": "admin",
      "name": "datacenter-1",
      "metadata": {
        "limits": {
          "cpu": {
            "value": "300m",
            "enabled": "true"
          }
        },
        "monitoring": {
          "enabled": "true"
        }
      },
      "note": "the cpu has enabled"
    }
  ]
}
```

### Request (without owner query param :: with all query param => true :: admin permission required)
```shell 
$ curl -X GET "http://127.0.0.1:5057/search/metadata.monitoring.enabled=true?all=true" -H "accept: application/json" -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTU4MDQ3Mzc0MH0.QaxTlU-1dJQGO_GpTTjJvSeuDnAdSkut0wkP3sHeTfM"
```

### Response (without owner query param :: with all query param => true :: admin permission required)
```shell 
200 ok
________________________________________________________

content-length: 345 
content-type: application/json 
date: Fri, 31 Jan 2020 12:00:11 GMT 
server: uvicorn 
________________________________________________________

{
  "Configs": [
    {
      "owner": "admin",
      "name": "datacenter-1",
      "metadata": {
        "limits": {
          "cpu": {
            "value": "300m",
            "enabled": "true"
          }
        },
        "monitoring": {
          "enabled": "true"
        }
      },
      "note": "the cpu has enabled"
    },
    {
      "owner": "user2",
      "name": "datacenter-2",
      "metadata": {
        "limits": {
          "cpu": {
            "value": "250m",
            "enabled": "false"
          }
        },
        "monitoring": {
          "enabled": "true"
        }
      },
      "note": "the cpu has disabled"
    }
  ]
}
```

### Request (with owner query param :: all query param => default value = false :: admin permission required)
```shell 
$ curl -X GET "http://127.0.0.1:5057/search/metadata.limits.cpu.enabled=false?owner=user2" -H "accept: application/json" -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTU4MDQ3Mzc0MH0.QaxTlU-1dJQGO_GpTTjJvSeuDnAdSkut0wkP3sHeTfM"
```

### Response (with owner query param :: all query param => default value = false :: admin permission required)
```shell 
200 ok
________________________________________________________

content-length: 180 
content-type: application/json 
date: Fri, 31 Jan 2020 12:02:55 GMT 
server: uvicorn 
________________________________________________________

{
  "Configs": [
    {
      "owner": "user2",
      "name": "datacenter-2",
      "metadata": {
        "limits": {
          "cpu": {
            "value": "250m",
            "enabled": "false"
          }
        },
        "monitoring": {
          "enabled": "true"
        }
      },
      "note": "the cpu has disabled"
    }
  ]
}
```
---
<br>

## Swagger UI documentation

* #### Swagger UI powerd by openAPI (tests include) @ **/docs** endpoint ( http://localhost:5057/docs )

<br>

# Deployment

- ## Cloud deployment (Google cloud platform)
We made full CI/CD pipeline using Github actions to Kubernetes cluster at GCP : 

![CI/CD workflow diagram](https://github.com/HadiZakiAlQattan/simple-api/blob/Hadi/gcp/cicd-diagram.jpg)

```shell 
.
├── gcp # GCP Kubernetes services (postgresdb & app) yaml files 
│   ├── api-config.yaml # api service configs contained env vars
│   ├── api-deployment.yaml # api deployment config
│   ├── api-service.yaml  # api service describe
│   ├── postgres-config.yaml  # postgres service configs contained env vars
│   ├── postgres-deployment.yaml # postgres deployment config
│   ├── postgres-service.yaml # postgres service describe
│   └── postgres-volume.yaml # postgres persistent volume config
└── .github
      └── workflows 
          └── cicd.yml # CI/CD using github actions
```

<br>

- ## Local deployment ( Dockerizing )

  ### Prerequisites:

  * docker 
  * docker-compose

  ### Build the image and run docker-compose services
  ``` shell
  $ docker-compose up
  ```

<br>

# Tests

### Run instructions:

* Unit tests :
  - run unit tests :
    ```shell
    $ ./tests_runner.sh u
    ```

* Integration tests :
  - run integration tests :
    ```shell
    $ ./tests_runner.sh i
    ```
