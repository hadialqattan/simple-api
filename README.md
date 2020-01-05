# Simpe API


## wiki

Simple API is HTTP service that stores and returns configurations that satisfy certain conditions.

  
## Endpoints 

Following are the endpoints that implemented:

| Name   | Method      | URL
| ---    | ---         | ---
| List   | `GET`       | `/configs`
| Create | `POST`      | `/configs`
| Get    | `GET`       | `/configs/{name}`
| Update | `PUT` | `/configs/{name}`
| Delete | `DELETE`    | `/configs/{name}`


#### Schema

- **Config**
  - Name (string)
  - Metadata (nested key:value pairs where both key and value are strings)

# Tests

### There are two types of tests implemented:

### - **Unit tests**
```shell
$ pytest test -vv
```

### - **Integration tests**
```shell 
$ nosetests --verbosity=2 tests/test_integration.py
```


---
---
# SimpleAPI

SimpleAPI is a restful API provids simple service that stores and returns configurations using FastAPI and PostgreSQL.

The entire API is contained within the `app` folder.

`tests_runner.sh` runs command line script that provids you tests instructions.

All stuffs `dockerized` (build instructions described below).

<br>

# Endpoints and config schema

| Name   | Method      | URL
| ---    | ---         | ---
| List   | `GET`       | `/configs`
| Create | `POST`      | `/configs`
| Get    | `GET`       | `/configs/{name}`
| Update | `PUT` | `/configs/{name}`
| Delete | `DELETE`    | `/configs/{name}`


#### Schema

- **Config**
  - Name (string of length no more than 120 characters)
  - Metadata (nested key:value pairs where both key and value are strings of length no more than 160 characters)

---

## `GET /configs`

### Request

Get list of configs: 

- path params: 
    ```shell 
    none
    ```
- query params: 
    ```shell 
    none
    ```

### Response

if no configs added yet:
    
    status code: 200
    json response: {"Configs":"Empty"}

else:

    status code: 200
    json response: {"Configs":[ list of configs ]}

example:
    
    json response: {"Configs":[{'name':'car', 'metadata':{'speed':"15", 'weight': '1000kg', 'language':'english'}}...]}

---

## `POST /configs`

### Request

Create a new config: 

- path params: 
    ```shell 
    none
    ```
- query params: 
    ```shell 
    name: string
    metadata: json
    ```

### Response

- None-exists name 
    ```shell 
    data example: {'name':'car', 'metadata':{'speed':"15", 'weight': '1000kg', 'language':'english'}}
    
    status code: 200
    json response: {"New config has created":{'name':'car', 'metadata':{'speed':"15", 'weight': '1000kg', 'language':'english'}}}
    ```

- Exists name 
    ```shell 
    status code: 400
    json response: {"detail":"name already exists"}
    ```

---

## `GET /configs/{name}`

### Request

Get a specific config:

- path params:
    ```shell 
    name: string
    ```
- query params: 
    ```shell
    metadata: json
    ```

### Response

- Exists name 
    ```shell
    status code: 200
    json response: {"Config":{'name':'car', 'metadata':{'speed':"15", 'weight': '1000kg', 'language':'english'}}}
    ```

- None-exists name
    ```shell 
    status code: 404
    json response: {"detail":"name doesn't exists"}
    ```

---

## `UPDATE /configs/{name}`

### Request

Update specific config:

- path params:
    ```shell 
    name: string
    ```
- query params: 
    ```shell
    metadata: json
    ```

### Response

- Exists name
    ```shell
    data example: {'name':'car', 'metadata':{'speed':"150", 'weight': '1000kg', 'language':'arabic'}}

    status code: 200
    json response: {"The config has updated":{'name':'car', 'metadata':{'speed':"150", 'weight': '1000kg', 'language':'arabic'}}}
    ```

- None-exists name
    ```shell 
    status code: 404
    json response: {"detail":"name doesn't exists"}
    ```

---

## `Delete /configs/{name}`

### Request

Delete specific config

- path params:
    ```shell 
    name: string
    ```
- query params: 
    ```shell
    none
    ```

### Response

- Exists name
    ```shell
    status code: 200
    json response: {"The config has deleted": {"name":"config name"}}
    ```

- None-exists name
    ```shell 
    status code: 404
    json response: {"detail":"name doesn't exists"}
    ```

---

## Swagger UI documentation
- #### Swagger UI powerd by openAPI @ **/docs** endpoint ( http://localhost:5057/docs )
- #### Swagger UI powred by redoc @ **/redoc** endpoint ( http://localhost:5057/redoc )

<br>

# Dockerization

## Prerequisites:
    - docker 
    - docker-compose

## Dockerizing the app

- building the image
    ```shell
    $ docker build -t simpleapi .
    ```
- compose the image
    ```shell 
    $ docker-compose up
    ```