# SimpleProject 1


## Problem definition

The aim of test is to create a simple HTTP service that stores and returns configurations that satisfy certain conditions.
The service should have a docker-compose file and everything is dockerized


## Instructions

1. Clone this repository.
2. Create a new branch.
3. Solve the task and commit your code. Commit often.
4. Do a pull request from your branch to the `master` branch.

In your pull request, make sure to write about your approach in the description.

I believe it will take 2 to 6 hours to develop this task.

### Endpoints

Your application **MUST** conform to the following endpoint structure and return the HTTP status codes appropriate to each operation.

Following are the endpoints that should be implemented:

| Name   | Method      | URL
| ---    | ---         | ---
| List   | `GET`       | `/configs`
| Create | `POST`      | `/configs`
| Get    | `GET`       | `/configs/{name}`
| Update | `PUT` | `/configs/{name}`
| Delete | `DELETE`    | `/configs/{name}`
| Query  | `GET`       | `/search?metadata.key=value`


#### Query

The query endpoint **MUST** return all configs that satisfy the query argument.

Query example-1:

```sh
curl http://config-service/search?metadata.monitoring.enabled=true
```

Response example:

```json
[
  {
    "name": "datacenter-1",
    "metadata": {
      "monitoring": {
        "enabled": "true"
      },
      "limits": {
        "cpu": {
          "enabled": "false",
          "value": "300m"
        }
      }
    }
  },
  {
    "name": "datacenter-2",
    "metadata": {
      "monitoring": {
        "enabled": "true"
      },
      "limits": {
        "cpu": {
          "enabled": "true",
          "value": "250m"
        }
      }
    }
  },
]
```


Query example-2:

```sh
curl http://config-service/search?metadata.limits.cpu.enabled=true
```

Response example-2:

```json
[
  {
    "name": "datacenter-2",
    "metadata": {
      "monitoring": {
        "enabled": "true"
      },
      "limits": {
        "cpu": {
          "enabled": "true",
          "value": "250m"
        }
      }
    }
  }
]
```

#### Schema

- **Config**
  - Name (string of length no more than 120 characters)
  - Metadata (nested key:value pairs where both key and value are strings of length no more than 160 characters)

### Deployment

Your application must be dockerized and have a docker compose file to describe all it needs and docker files for all parts of the application

## Rules

- You can use any language / framework / SDK of your choice.
- The API **MUST** return valid JSON and **MUST** follow the endpoints set out above.
- You **SHOULD** write testable code and demonstrate unit testing it.
- You **SHOULD** have both unit tests and integration tests
- You can use any testing, mocking libraries provided that you state the reasoning and it's simple to install and run.
- You **SHOULD** document your code and scripts.
- You need to have everything automated in scripts and use docker as a unit of deployment locally.
- You can use any database you want for this.

