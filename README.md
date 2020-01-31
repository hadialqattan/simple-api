# SimpleAPI
![](https://github.com/HadiZakiAlQattan/simple-api/workflows/SimpleAPI%28CI%2FCD%29/badge.svg) <a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>

### SimpleAPI is a restful API provids simple service that stores and returns configurations with simple jwt authentication using FastAPI and PostgreSQL.

<br>

# Project structure
```shell
.
├── app/
├── gcp/
├── tests/
│   ├── unit/
│   └── integration/
├── tests_runner.sh
├── Dockerfile
├── docker-compose.yml
└── .env
```

- app/ contains the entire API :
  - [Users endpoints](#users)
  - [Configs endpoints](#configs)

- gcp/ contains GCP Kubernetes deployment *.yml files -> [GCP deployment](#cloud-deployment-(google-cloud-platform))

- tests/ contains the entire CI tests : -> [run instructions](#tests)
  - unit/
  - integration/ 
  - `tests_runner.sh` full automated script aim to run tests inside docker container.

- Dockerfile & docker-compose -> [Dockerizing](#local-deployment-(-dockerizing-))

- .env contains env vars include (app & db) (host & port).

<br>

# Endpoints and schemas

## Users

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
  + Id (integer)
  + public_id (string of length no more than 50 characters)
  + name (string of length no more than 50 characters)
  + password (string of length no more than 50 characters)

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
  + User_id (integer)
  + Name (string of length no more than 120 characters)
  + Metadata (nested key:value pairs where both key and value are strings of length no more than 160 characters)
  + Note (string of arbitrary length)

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
  We made full CI/CD pipeline using Github actions to Kubernetes cluster at GCP.
  ```shell 
  .
  |
  ├── gcp # GCP Kubernetes services (postgresdb & app) yaml files 
  │   ├── api-config.yaml # api service configs contained env vars
  │   ├── api-deployment.yaml # api deployment config
  │   ├── api-service.yaml  # api service describe
  │   ├── postgres-config.yaml  # postgres service configs contained env vars
  │   ├── postgres-deployment.yaml # postgres deployment config
  │   ├── postgres-service.yaml # postgres service describe
  │   └── postgres-volume.yaml # postgres persistent volume config
  |
  └── .github
       └── workflows 
           └── cicd.yml # CI/CD using github actions
  ```

![CI/CD-workflow](https://www.draw.io/?lightbox=1&highlight=0000ff&edit=_blank&layers=1&nav=1&title=cd%20(2).drawio#R7V1bc6M4Fv41rtp9CIXEzTw6cdLT1d272enpmu2nFDEyZoIRAzhx%2BtePBAiDJC62wXZ3YlclRhKyON%2B56ehInmg36%2B2H2IlWX7CLgglU3e1Em08g1FVTI%2F9oyWteAlXNyku82HfzMrAr%2BOr%2FQEWhWpRufBcltYYpxkHqR%2FXCBQ5DtEhrZU4c45d6syUO6t8aOR4SCr4unEAs%2FdN301VRCkx7V%2FEb8r1V8dVTWDzf2mGNiydJVo6LXypF2u1Eu4kxTvNP6%2B0NCij1GF3y%2B%2B4aasuBxShM%2B9xwp%2F8ZfIQ%2FfsdfZp%2B%2BfFpoa816uQKMzs9OsCkeuRhu%2BspoEONN6CLajTrRrl9Wfoq%2BRs6C1r4Q2EnZKl0H5AqQj4HziIJrZ%2FHkZbfd4ADHpCrEIWl%2FvcRhWoAMCAWuncD3QnKxIA%2BBSLtr8amKB31GcYq2laLiKT8gvEZp%2FEqasFq7eKaS5%2FLLlx1%2BU%2FbYqwp0QNWLUqdgGq%2Fse0dX8qEgrZzM3%2F9HHtb7r21F%2Fv23rXv%2F5VuCr%2ByBiVwlo06uvcBJkuLWpR8EjOoTqGkmfZPyJI3xE6rX2Jo7DM3htE7zEoMK0U1dQnTdGovmhDAi0c0gpaSInLBGffPvDRXDjK5XSUbYGWkAYLQl%2FzISqVndSzF0Wmup6u5O8smj%2Fz%2F46WrzSJ9nkfo4TNhXkkfIvzVvdhz8NbgrrEDrKGY%2B0V%2BzQrJSHIlMcZe9BoKeFzcLKrolog8l6GuWpRjaSAwAZVLXwQAZ4a%2BSnPIU5BDHaycQcb75SMZ0M6fPiOOnZUA0O1T%2FhWmv0SZZ%2FXt83DlEIX330bDNeqCBdWiHxYDhAPyiqXV%2BKa%2BrzKLKmGU09Qw1gVMovmOIqBSSKolLG3qPE5%2BqkGpDhtBnrsHad116dwOEQ6AGjDpqmqkwslWAg4YhAgdtTbGssbAT1fzN%2FIzYjYaACTi50UW5gZZEbkoFfQzt5d5jo4J97GVedWJeM5XKKdfPPqESfTDyXMTwBs4TmlYU6uMw2pTToFNwq4E7mYKEc4sqpHz8lfJl9pK4Y0PImw4VTuKmhgJEuwplqtIwR0KcdXwU5ALe30Kf4p2iJE3ePM66qSn22XGejoHzR6IzvdjJjNY73AWEhkSNnxRrKFPjxyCwwrH%2Fg9DOYQUtjmWFvLwl5WCxs9c401Vz2nO6OogPKpc4EQU2l%2BSwSFZORD%2F66yx2VaW8nNBNXuMjTlO87ozZZN8zS6I8vEbxd9jF0t9SprguhjJfpSmNy80oKeDdwg1VxV%2FgcOkT5omVBfkyeOc6qUP%2B0fKEzo5W%2FjK9CrCH09cI0RKNUjJ%2F9isAp0oUei1hDaJPXB%2FtOKUh0JSNcPeI9YaVfuc6fQvceDzLGRaosRyUTHv0qchxrGxwhjOH8N4EFX%2B98QOX1Lp48UT8YzKGjDXelpY39Qt03Uw4Bt73m4T66OkK7bBWU0z%2BfLj5%2FY3DfhGenNkcBj0C9jmKAvxaQv3plvxdBJuEzonfNujn9%2BdMq9ufQ66HmHXDcboi5jd0gttdqWBAK3ig0J3RpTXqQgREz%2F%2Bx8sO8%2BM4PWKM6wjlUbAUN5q2L7vWs3onT2jUfpNRnU0MjNa6TrMpuGxyXKpOgrZ%2F%2BnzYnfnd%2B9Z09Bvk83xY9ZRev7CIkOFRuopffq3W727Irdl8jOyV4Ey9QC2ZsadOJPZS2eYkF01D8Wrmzwn2AcV%2BMAjL3eka1ocnYr%2BjuHudxGLaaC%2BtOs877wvlTFnftmFjoyOjqKCeD0BFhOue10iyiDZKWAetQ%2Bj1N4%2BpoTz7kI9iJZknwI6RVNtN%2Bu9J6csljEtUtetMzip5Rl5hSgvYWva6OGkRvKG5n8el3bq%2FaJmaNvtfs1LC2qX%2BmRbfITHuKDJtinkNkBE7nEw36ikwZB2rqaCBrZXDWxygsQ6Moc%2Bvu%2B7bXrHZraPGTWOsE1tDqEYt8e%2FphH9%2F1cLE2%2BzqhLJJwDrG2NM53NA4U62lXR2NbQjHn4A1z%2BhFcC%2FtyrX5OruWCBMAuI0P7Mq7Q16kZ1%2FgFGVeHU%2F3uEMYV3KpRZzDSDBijpwCc0RnTOGcMTA%2FU2kLyWM%2F5y77OGOSsAzDanSW%2BfZdzxYcaTuNcickbZcKiIMIp2qZ1uRRYnV9tLLPQYpT4P5zHrCvK2wW1Sb%2FG9cSYt0qWNFariTFddU7fk86FunYdxod5y40Exegn1Vx9Wfj3SlU0w6rzyiAicwV0RdfqHau2okO78qp3ipfLBI2j83%2FFINWAOv%2FSYsxH2QnLPp%2Bh4GPM4FD3vtxXwDrqOWs%2FQGLaiF0RGC%2FLcZPq2pNldFT16zFpHbAzrSNbRXReUEIoSS6BZVMaL7CLqjkdHRlAjUkbjUKwRyYWlwLEDHiFqWXJtENsV2mVugrH%2FOa4Pil5jJ1wITLNSLuyNAkOA5Bb2CUCRHpDQ0JwXgEMRvApFAj%2BxckXsM9O8uPpbRo96G2elN6yRISfzIcoPQVQXNw7KeGYMAdN1VrdjOM8C6vqWpTeRJdroWcZkzvnQlFhWdDgYGRX9yj2Cex0DEdGFZle63Q7mDxewmLBwW4HL3ZCR0MtbVuW9Hsag0b8%2FkzjBPPNabMTRG9%2BSxPOUvkNMeEENhcCvBpmyqnrZVCSdQwVus218uI2a4435ZyKwYoPGHsBzS8sE9jicjtmgDeuWHxP6LHE8foYj1vYW9e4%2BW68NGqt09%2F2MtpcJRs%2FTSg75FnUEDx4D7TsIa9%2FIN7K00OC4md%2FgR6yr2tOsS6tUs8U66Z8fSbGAVqmgviImx3j3BcZxMfnooWmZFe6ARTJlsVd6fB%2BUI9YypCOJrdP2KJvCXrd%2B4QN0wDWULMvDhlLkjUp3QQMDa1MpR4emh7nNNTJUhC5PNsDCE5l3enMzNpjgoNNimbxggFAS8sruBemRdFhMlqeAzDGORx9MAaabApiK23G6yiImQaQmBXeeHzaPBLXnjjBiVh3G3o%2BITDPHLVIYt2wq5O2nGYDFJOEJvbKrNV669FjdhRvEUFlhbYfF1RjXkdx%2FmHuPaEHHD5EMaIxIAJe2qFjO00ap7sbbSM9McEPvc9Zs7khcpo1o2%2BOI%2BUzi3bR7Ga%2Fgt1UpsFrKkXCbWXDYycRnOsET%2BUq2YOsyNZtzq7NZ0xDjhkb%2FYXS9LUAz9mkuJcdas3YLyfHwyuqzpmpXVCpc2Zq980c6M1Ax6mwQfL73%2BFubNg3x%2F5EcPdwSt7hPgLuvnndJ4JbDEtXHRF1XcSoG2cMYMjQtHRmwPkuJcpS36UJ6sH31wJdMevRC8sSD6gBlqqYpugFWGNts7X3mu69afB2Uab6VmlbslX69DjKTj55x7GOo6XaiqYJCSoXhWOPZaifHMchDxArKwbgDo1mvVZf%2BuWxB2C652dephwuL%2FvyU51ac727nT%2FY0%2FkbYdHRNrno9KH7aYHa1dNAq478liALtK86mnwEEJxg1RGo4s6K%2F2BXDNaJC45ynSsGW%2FsvTMpsR1229zMf4sEGI1hxbVqH2VbFSJrscCQ%2BF3tApSwa7XdI93KwufX%2FC4BUDFq%2BQ7qXr20JE94LQLX5fEjXf64hWztvZums%2FeA1P3GGrmjjgIwNkkHQtX5nTQEpmi%2BIUfSzJL0QvfCV%2BS1rHOLiCOfy4G7uUO%2BsIvBDdLWqnOgN2YGkqnAOdBTnvfEH4Rx0pLisowgnqRfTnzqY2YqpwEnTAdJlcUbQzvN1jp7BtET1GpaWD1uL1A36lk6RhrZv3GYdW5L7C2S5qKMd%2FgdUWUz%2FXW7e5eaS5MaClyc3zefU9pabUhiyiXImKkyQuIqs8Y38Fpl0CfftJKz2qxINvzghlzNWKxU1QTy%2B%2BusoQLP7j%2B8CMIAXDbUeAmCdUgDALxCuqgWlxsqfPyBcBSa11PkydjV4uMrue6AOAGeMV%2FEHyICy4%2F0DVvzuvJECVnwAqvyJp6aR8TG5vW8wDU6mx4hwMS6oCP1t6G4SybqwkGMcVXZ2kO%2FyowRVNnu0pt%2BXWY6qILR5%2BtcfWS4BlVWWV80ymv21Rx418B%2FJX%2FrLSM%2FowfVjMjJMOe4ucKIURw%2BLgGp%2FJXn2WsW9zNg%2FuYXp3qBYHd4AFodnYInBYT%2Bxd5JdigD8AsfWHLKLy76l72OtUMUG9T7n7WRWqFQrVTPUtrn5LBvEOSN06EEivDHj%2Bxn5EB0g%2BXW6O4TcR8JYgjxd1M6oNvUo8l6HEhlkN5TFFoPLzNvjOO2YhF1yuftFz7z57odRtdt%2FAA%3D%3D)

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
