# Variables
PYTHONPATH := $(shell pwd)

run: clean
	@PYTHONPATH="${PYTHONPATH}" python ./src/main.py

linter: format
	poetry run bandit . && poetry run flake8 . && poetry run black --check .

format:
	poetry run isort . && poetry run black .

install:
	poetry env use python
	poetry lock
	poetry install
	# poetry run pre-commit install

migrate:
	@PYTHONPATH="${PYTHONPATH}" alembic -c ./alembic.ini upgrade head

revision:
	@PYTHONPATH="${PYTHONPATH}" alembic revision --autogenerate -m "${COMMENT}"

downgrade:
	@PYTHONPATH="${PYTHONPATH}" alembic -c ./alembic.ini downgrade -1

test: clean
	@PYTHONPATH="${PYTHONPATH}" ENVIRONMENT=unittest poetry run -vvv coverage run -vvv -m pytest && poetry run coverage report -m

test-all:
	@PYTHONPATH="${PYTHONPATH}" ENVIRONMENT=local python -m pytest tests

test-report:
	@PYTHONPATH="${PYTHONPATH}" poetry run coverage html || true && open ./htmlcov/index.html

build: clean
	docker compose -f docker-compose.yml build

build-test: clean
	docker compose -f docker-compose.yml build --build-arg INSTALL_ARGS="--with dev"

down-test: down
	docker volume ls | grep "postgres_data_test" | awk '{print $2}' | xargs docker volume rm || true

up: build up-containers
	docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d billing_service

down: 
	docker compose -f docker-compose.yml down -v -t 1

migrate-apply: build
	docker compose -f docker-compose.yml -f docker-compose.dev.yml run --rm --entrypoint "make migrate" billing_service

test-integrated: down-test build-test -test
	docker compose -f docker-compose.yml -f docker-compose.test.yml run --rm --entrypoint "make test-all" billing_service

up-containers:
	docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d db

update-poetry-and-all-dependencies:
	poetry self update
	poetry self add poetry-plugin-up
	poetry up --latest

create-stack-network: install-plugin-loki
	docker network inspect stack-network --format {{.Id}} 2>/dev/null || docker network create stack-network

install-plugin-loki:
	docker plugin inspect loki --format {{.Id}} 2>/dev/null || docker plugin install grafana/loki-docker-driver:latest --alias loki --grant-all-permissions

clean:
	@find . | egrep '.pyc|.pyo|pycache' | xargs rm -rf
	@find . | egrep '.pyc|.pyo|pycache|pytest_cache' | xargs rm -rf
	@rm -rf ./htmlcov
	@rm -rf ./pycache
	@rm -rf ./pycache
	@rm -rf ./.pytest_cache
	@rm -rf ./.mypy_cache
	@find . -name 'unit_test.db' -exec rm -r -f {} +
	@find . -name '.coverage' -exec rm -r -f {} +
