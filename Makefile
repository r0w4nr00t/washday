.PHONY: runserver
runserver:
	poetry run python3 -m washday.manage runserver

.PHONY: install
install:
	poetry install

.PHONY: migrate
migrate:
	poetry run python3 -m washday.manage migrate

.PHONY: migrations
migrations:
	poetry run python3 -m washday.manage makemigrations

.PHONY: superuser
superuser:
	poetry run python3 -m washday.manage createsuperuser


.PHONY: update
update: install migrate install-pre-commit;

.PHONY: install-pre-commit
install-pre-commit:
	poetry run pre-commit uninstall; poetry run pre-commit install

.PHONY: lint
lint:
	poetry run pre-commit run --all-files

.PHONY: up-dependencies-only
up-dependencies-only:
	test -f .env || touch .env
	docker-compose -f docker-compose.dev.yml up --force-recreate db
