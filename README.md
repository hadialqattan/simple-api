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

# Swagger UI documentation

### There are two different swagger UI documentation:

- #### Swagger UI powerd by openAPI at **/docs** endpoint ( http://127.0.0.1:8000/docs )
- #### Swagger UI powred by redoc at **/redoc** endpoint ( http://127.0.0.1:8000/redoc )
