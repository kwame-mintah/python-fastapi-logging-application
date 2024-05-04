# Python FastAPI Logging Application

![fastapi-0.110.3-informational](https://img.shields.io/badge/fastapi-0.109.0-informational)
[![🧪 Run unit tests](https://github.com/kwame-mintah/python-fastapi-logging-application/actions/workflows/run-unit-tests.yml/badge.svg)](https://github.com/kwame-mintah/python-fastapi-logging-application/actions/workflows/run-unit-tests.yml)
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>

This project aims to demonstrate an external application receiving logs, from another system. Logs received will be stored
within the applications' database. Storing and retrieval of log events will be exposed via endpoints using the
[FastAPI](https://fastapi.tiangolo.com/) framework.

## Development

- [Python](https://www.python.org/downloads/release/python-3123/)
- [Docker](https://docs.docker.com/compose/install/)
- [Pre-commit](https://pre-commit.com/#install)

## API Specification

The application exposes `/v1/events/*` endpoints, which accommodates two types of log events: user and system. Both of which
can be consumed and/or returned in the same API request. The expected log event structure for these events is the following:

- User:
  ```json
  {
    "type": "user",
    "timestamp": "2023-10-01T13:45:00.000Z",
    "event_id": "u_001",
    "event": {
      "username": "my_user",
      "email": "my_user@email.com",
      "operation": "write"
    }
  }
  ```
- System:
  ```json
  {
    "type": "system",
    "timestamp": "2023-10-01T13:45:00.000Z",
    "event_id": "s_123",
    "event": {
      "system_id": "id_123",
      "location": "europe",
      "operation": "read"
    }
  }
  ```

[Pydantic](https://docs.pydantic.dev/2.7/) is used heavily within this project, for schema validation and serialisation.
All endpoints have been annotated with their models and through FastAPI swagger [documentation](https://fastapi.tiangolo.com/features/#automatic-docs)
(`/docs`), end users are able to easily identify limitations, expected responses and errors for each endpoint.

Through Pydantic and FastAPI, API constraints have been addressed, for example ensuring the number of records inserted or returned
cannot surpass 1000 and should return a [400 BAD request](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/400).
As mentioned earlier, API specification and constraints can be found on `/docs` endpoint, it is recommended to read
through and try out each endpoint.

## Usage

1. Install python packages used for the service:

   ```console
   pip install -r requirements.txt
   ```

2. Run the FastAPI server, which will start on port 8000:

   ```console
   python app/main.py
   ```

   Endpoint documentation is available on: http://127.0.0.1:8000/docs

## Running with Docker

Running the `docker-compose.yml` file, will build a new image. Named and tagged as: `python-fastapi-logging-application-fastapi:latest`
using the [`Dockerfile`](https://docs.docker.com/develop/develop-images/guidelines/), this docker image will be used for
the `fastapi` service docker container [^1]:

```console
docker-compose up --build -d
```

Endpoint documentation is available on: http://localhost:8080/docs

> [!NOTE]
> The command provided ensures that a new image is built ([`--build`](https://docs.docker.com/reference/cli/docker/compose/build/)),
> each time to facilitate potential code changes in between container runs. If not provided, the same docker image will
> be re-used and not reflect code changes. Additionally, no logs will be output in your console due to ([`-d`](https://docs.docker.com/reference/cli/docker/compose/up/#options))
> instead FastAPI logs can be found within your Docker for desktop application.

## Tests

Unit tests are located in `/tests/unit` directory, run unit tests using:

```console
pytest tests/unit
```

## Contributing

Git hook scripts are very helpful for identifying simple issues before pushing any changes.
Hooks will run on every commit automatically pointing out issues in the code e.g. trailing whitespace.

To help with the maintenance of these hooks, [pre-commit](https://pre-commit.com/) is used, along with [pre-commit-hooks](https://pre-commit.com/#adding-pre-commit-plugins-to-your-project).

Please following [these instructions](https://pre-commit.com/#install) to install `pre-commit` locally and ensure that you have run
`pre-commit install` to install the hooks for this project.

Additionally, once installed, the hooks can be updated to the latest available version with `pre-commit autoupdate`.

## GitHub Actions (CI/CD)

GitHub project has three workflow set up, found in `.github/workflows/`:

- '🧹 Run linter' (`run-linter.yml`): To run [Flake8](https://flake8.pycqa.org/en/latest/) and check Python code system and comply with various style guides.
- '🧪 Run unit tests' (`run-unit-tests.yml`): To run unit tests within a continuous integration (CI) environment, using [`pytest`](https://docs.pytest.org/en/8.2.x/).
- '🚧 Bump version' (`run-version-bump`): To create a new GitHub tag based on [semantic versioning](https://semver.org/) using [commitizen](https://commitizen-tools.github.io/commitizen/).

[^1]: A [`platform`](https://docs.docker.com/compose/compose-file/build/#platforms) has been specified to ensure the host machine, uses the correct platform during docker image build.
