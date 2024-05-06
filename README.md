# Python FastAPI Logging Application

![python](https://img.shields.io/badge/python-3.12.3-informational)
![fastapi-0.110.3-informational](https://img.shields.io/badge/fastapi-0.109.0-informational)
![semver](https://img.shields.io/badge/semver-2.0.0-blue)
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
[![🧪 Run unit tests](https://github.com/kwame-mintah/python-fastapi-logging-application/actions/workflows/run-unit-tests.yml/badge.svg)](https://github.com/kwame-mintah/python-fastapi-logging-application/actions/workflows/run-unit-tests.yml)

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
As mentioned earlier, API specification and constraints can be found on `/docs` endpoint, it is **recommended** to read
through the swagger documentation and try out each endpoint.

## Roadmap

More work needs to be completed for the final version of the application. Below are additional things required for a
clearer vision of what is envisioned of this application.

### Implementing MongoDB

As of version [v1.1.0](https://github.com/kwame-mintah/python-fastapi-logging-application/commit/cd423356da7193c37fae5ac7eb6dcf2a31634cb1), [`pickle`](https://docs.python.org/3.12/library/pickle.html)
was introduced to the codebase as a placeholder for storing and querying log events on runtime. Ideally, [MongoDB](https://www.mongodb.com/docs/upcoming/release-notes/7.3/) will be
used as a datastore for log events. This is because log events received are in `JSON` format and MongoDB stores data as [`BSON`](https://www.mongodb.com/json-and-bson)
as both are closely related, storing will be much easier without having to do many additional steps.

The following tasks will need to be completed to accomplish this:

1. Select an appropriate Object Document Mapper (ODM), most likely [Motor](https://www.mongodb.com/docs/drivers/motor/).
2. Configure credentials for [connecting](https://www.mongodb.com/docs/drivers/motor/#connect-to-a-mongodb-server-on-your-local-machine)
   to MongoDB using environment variables and store values in a suitable [pass](https://www.passwordstore.org/) store
   or secrets manager etc.
3. Create a new database for storing log events. A new Pydantic model will be created to represent the Database model e.g.
   `EventLogsCollection` re-using the existing model `EventLog` encapsulated as a list.
4. Update existing endpoints and services to use `CRUD` operations against MongoDB.

> [!NOTE]
> Due to `pickle` being used, duplicate `event_id` can be inserted, so using the `/v1/event/get/{event_id}` will
> only return one result and not the duplicate log events. This is the intended behaviour in the final version,
> as the MongoDB `_id` for the document will use the `event_id` when being saved into the database.

### Deploying to Kubernetes using Helm charts

A `Dockerfile` is included to start the FastAPI server within a docker container. The next step is to use
the docker image created as part of deployment to a [Kubernetes](https://kubernetes.io/) cluster using [Helm](https://helm.sh/).
Most major cloud providers e.g. Google, AWS, Azure etc. provide a Kubernetes service, deploying to any of the providers
will demonstrate a scalable and highly available FastAPI application.

The following tasks will need to be completed to accomplish this:

1. A new continuous integration (CI) / continuous delivery (CD) pipeline that will build and push new docker images to
   a remote repository, so it can be pulled down later for deployments to Kubernetes.
2. Configure a Kubernetes cluster within the chosen cloud provider using [Terraform](https://www.terraform.io/).
3. Create necessary `.yaml` configuration files to specify docker image, networking, environment variables etc.
4. Deploy to the Kubernetes namespace using helm.

### API Improvements

The current query parameters supported as [v1.0.0](https://github.com/kwame-mintah/python-fastapi-logging-application/commit/640dd23fa0ec3fdfff4026c1f075314707db7547)
for the `/v1/endpoints/all` endpoint is `?size=`. Although there is a size limit of 1000, does not mean that there is a
maximum of 1000 log event stored within the database. Providing the ability to Paginate the log events returned, allows
end users to potentially scroll through all log events without being an expense operation against the database.

The following tasks will need to be completed to accomplish this:

1. Create a new Pydantic model to represent the Paginated response e.g. `PaginatedEventResponse`. Detailing, the size,
   from, total etc.
2. Update existing endpoint `response_model` to reflect the new response.
3. Implement MongoDB [`MotorCursor.skip()`](https://motor.readthedocs.io/en/stable/api-tornado/cursors.html#motor.motor_tornado.MotorCursor.skip)
   to include how many documents to fetch, offset etc.

## Prerequisite

You will need to create a virtual environment, please follow the official [Python guide](https://docs.python.org/3.12/library/venv.html) how on doing this.

## Project structure

The project file structure follows the same blueprint [documented](https://fastapi.tiangolo.com/tutorial/bigger-applications/#an-example-file-structure) by FastAPI.

```markdown
.
├── app/
│ ├── __init__.py
│ ├── main.py
│ ├── dependencies.py
│ ├── data/
│ ├── exceptions/
│ ├── models/
│ ├── routers/
│ └── services/
└── tests/
├── integration/
└── unit/
```

## Usage

All commands snippets are run within the root directory of the project. After cloning the repository, please change directories.

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

To shut down the docker containers:

```console
docker-compose down --remove-orphans
```

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

Additionally, a coverage report can be generated using [`pytest-cov`](https://pypi.org/project/pytest-cov/):

```console
pytest --cov=app tests/unit --cov-report=html:coverage_report
```

Will generate a coverage HTML file, in the `/coverage_report/` directory, simply open the `index.html` in your chosen web browser [^2].

Integration tests are located in `/tests/integration` directory, run integration using:

```console
pytest tests/integration
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
- '🚧 Bump version' (`run-version-bump.yml`): To create a new GitHub tag based on [semantic versioning](https://semver.org/) using [commitizen](https://commitizen-tools.github.io/commitizen/).

[^1]: A [`platform`](https://docs.docker.com/compose/compose-file/build/#platforms) has been specified to ensure the host machine, uses the correct platform during docker image build.
[^2]: The GitHub workflow ['🧪 Run unit tests'](https://github.com/kwame-mintah/python-fastapi-logging-application/actions/workflows/run-unit-tests.yml) provides a brief overview of coverage for each file, when viewing the step 'Run tests with pytest with coverage'.
