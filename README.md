# Python Service Template

This repository is a way of how I would implement a microservice using python together with the fastAPI framework, asynchronous connection with database and logs.

This microservice simulates the creation of payment slips for the company XPTO.

No data is real and you can try to make the implementation very simple, just follow the guidelines below.

## Dependencies

- Python 3.11
- Poetry
- Direnv

Ps: Suggested IDE: vscode or pycharm-community with plugins Better Direnv, Docker and Makefile Language

Before starting to configure your project, create a file with the name `.venv`, where you will install your dependencies for python

## Features

- [x] Environment Variables
- [x] Logging
- [x] Database session with async driver postgres
- [x] Database migration
- [x] Automated unittests, e2e tests and integrated tests
- [x] Linters, formatters e checkers
- [x] Hooks with pre-commit
- [x] Dockerization app
- [x] Setup apis rest
- [x] Setup tests e tools for code coverage
- [x] Helpers cache and date
- [x] Rate limit http and workers
- [x] Pagination with driver async

## How to run

### Install dependencies
```bash
make install
```

### For first run of service in workspace
```bash
make up-containers
make migrate
```

### Running the service
```bash
make run
```

### Running the service via docker for the first time
```bash
make up
make migrate-apply

# To shut down containers:
make down
```

### Running the service via docker
```bash
make up
```

### Running all tests via docker
```bash
make test-integrated
```

### Running tests on the workspace
**Ps**: The e2e and integrated tests will be executed using the sqlite database to speed up the development.
```bash
make test
```

### Running tests in the workspace using real resources
```bash
make test-all
```

### Verifying project test coverage.
```bash
make test-report
```


### Project Structure

```shell
   |-src                      Application source code.
   |---domain
   |---entrypoints
   |-----routes
   |-------v1                 Versioned FastApi http routes.
   |---infra                  Beginning of the abstraction we must apply the dependency inversion principle: high-level modules (the domain) must not depend on low-level ones (the infrastructure).
   |-----adapters
   |-------database
   |---------migration
   |-----------versions
   |---------repositories
   |-----------models         ORM implementation with sqlaclhemy for the database.
   |-----------settings.py    Engine configuration, repositories session and database connection for the app and tests.
   |-------logging
   |---------settings.py      Configuration of the log framework for the service.
   |-------repositories
   |-------trace
   |---------settings.py      Trace configuration and metrics with open telemetry.
   |---schemas                Implementation of service schemas and validations.
   |---services               Implementing the route handler classes, our services must connect routers with database and domain/schema validations.
   |---constants.py           Suggestion for writing app constants.
   |---settings.py            Configuration of app envs and properties.
   |-tests                    Application testing source code.
   |---e2e                    API test, verifying that calls to endpoints have the expected return.
   |-----entrypoints
   |-------routes
   |---------v1
   |---integration            Testing the database abstraction layer and other integrations, verifying that the methods correctly reflect these services and vice versa.
   |---manual                 Files that assist in manual testing of the services, if necessary.
   |---unit                   Test small units of code, isolating them from external dependencies such as the database or an external cache.
   |---__init__.py            Resources for configuring logs and database for testing.
   |---conftest.py            Fixtures shared between tests.
   |-.env-dev                 File with environment variables for running the service in the workspace.
   |-.envrc                   Direnv file conf.
   |-alembic.ini              Contains all the basic configuration information for the alembic database migration tool.
   |-docker-compose.dev.yml   Override envs for running the app in containers.
   |-docker-compose.test.yml  Overwrites the envs for running the apps e2e and integrated tests.
   |-docker-compose.yml       Configuration for the containers that run our application and also the tests (for CI), telemetry and database services.
   |-Dockerfile               Configuration for app containers.
   |-Makefile                 Provides the entry point for all the typical commands a developer (or a CI server) might want to run during their normal workflow: make build, make test.
   |-poetry.lock              Dependencies versioning file.
   |-pyproject.toml           App configuration file, dependency management, test framework configuration, coverage and plugins for linters and formatters.
   |-README.md                It is an essential guide that provides other developers with a detailed description of your project.
   |-.flake8                  It has Flake8 rules.

```