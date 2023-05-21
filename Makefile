.PHONY: venv build check-lint lint

venv:
	python -m venv .venv

build:
	python -m pip install --upgrade pip
	python -m pip install -r beer_challenge/requirements.txt

build-test:
	python -m pip install --upgrade pip
	python -m pip install -r requirements.txt

build-all: build build-test

check-lint:
	sqlfluff lint .

lint:
	sqlfluff fix . -f

build-docker-image:
	docker build -t gergobig/beer-challenge-db .

open-db-for-localhost:
	docker run -p 5432:5432 gergobig/beer-challenge-db
