VENV=.venv
PYTHON=$(VENV)/bin/python
PIP=$(VENV)/bin/pip

.PHONY: help venv install format lint test clean build precommit publish

help:
	@echo "Makefile commands:"
	@echo "  make venv        - Create virtualenv"
	@echo "  make install     - Install dependencies"
	@echo "  make format      - Run black & isort"
	@echo "  make lint        - Run pre-commit"
	@echo "  make test        - Run tests"
	@echo "  make build       - Build package"
	@echo "  make clean       - Remove build artifacts"
	@echo "  make precommit   - Install pre-commit hooks"
	@echo "  make publish     - Publish to PyPI"

venv:
	python3 -m venv $(VENV)

install: venv
	$(PIP) install --upgrade pip
	$(PIP) install -e ".[dev,fastapi,flask,django,streamlit]"
	$(PIP) install build twine

format:
	$(VENV)/bin/black src tests examples
	$(VENV)/bin/isort src tests examples

lint:
	$(VENV)/bin/pre-commit run --all-files

test:
	$(VENV)/bin/pytest --cov=src --cov-report=term --cov-report=html

build:
	$(VENV)/bin/python -m build

clean:
	rm -rf dist build *.egg-info .pytest_cache .coverage htmlcov

precommit:
	$(VENV)/bin/pre-commit install

publish: build
	$(VENV)/bin/twine upload dist/*
