MAKEFLAGS += --warn-undefined-variables
SHELL := bash
.SHELLFLAGS := -eu -o pipefail -c
.DEFAULT_GOAL := all
.DELETE_ON_ERROR:
.SUFFIXES:

# include makefiles
export SELF ?= $(MAKE)
PROJECT_PATH ?= $(shell 'pwd')
include $(PROJECT_PATH)/Makefile.*

all: python/venv python/build docker/build docker/run
.PHONY: all

REPO_NAME ?= $(shell basename $(CURDIR))
SRC_DIR := tfver
TEST_DIR := tests

#-------------------------------------------------------------------------------
# python
#-------------------------------------------------------------------------------

PYTHON_VERSION ?= 3.12

# -- python venv --
VIRTUALENV_DIR ?= .venv

VENV_CFG := $(VIRTUALENV_DIR)/pyvenv.cfg
$(VENV_CFG):
	@echo "[INFO] Creating python virtual env under directory: [$(VIRTUALENV_DIR)]"
	@python$(PYTHON_VERSION) -m venv '$(VIRTUALENV_DIR)'

## Python configure virtual environment
python/venv: $(VENV_CFG)
.PHONY: python/venv

# -- python venv export path --
VIRTUALENV_BIN_DIR ?= $(VIRTUALENV_DIR)/bin

# -- python install packages from requirements file --
PYTHON_REQUIREMENTS := requirements.txt
PYTHON_DEV_REQUIREMENTS := requirements-dev.txt
PYTHON_SRC_REQUIREMENTS := $(PYTHON_REQUIREMENTS) $(PYTHON_DEV_REQUIREMENTS)

## Python install packages from requirements file(s)
python/packages: $(PYTHON_SRC_REQUIREMENTS)
	@for i in $(^); do \
		echo "[INFO] Installing python dependencies file: [$$i]"; \
		source '$(VIRTUALENV_BIN_DIR)/activate' && \
			pip install -r "$$i"; \
	done
.PHONY: python/packages

## Create virtual environment and install requirements
venv: python/venv python/packages
.PHONY: venv

#-------------------------------------------------------------------------------
# build
#-------------------------------------------------------------------------------

DIST_DIR ?= dist

## Python build package
python/build: clean/build
	@echo "[INFO] Building python package. Storing artificat in dist directory: [$(DIST_DIR)]"
	@$(VIRTUALENV_BIN_DIR)/python -m build --sdist --outdir '${DIST_DIR}'
.PHONY: python/build

## Build python package
build: python/venv python/packages python/build
.PHONY: build

#-------------------------------------------------------------------------------
# publish
#-------------------------------------------------------------------------------

## Python upload check
upload/check:
	@echo "[INFO] Checking whether the long description will render correctly on PyPI."
	@$(VIRTUALENV_BIN_DIR)/twine check --strict dist/*
.PHONY: upload/check

## Python upload package to testpypi
upload/testpypi: upload/check
	@echo "[INFO] Uploading python package to testpypi"
	@$(VIRTUALENV_BIN_DIR)/twine upload --repository testpypi dist/*
.PHONY: upload/testpypi

## Python upload package to pypi
upload/pypi: upload/check
	@echo "[INFO] Uploading python package to pypi"
	@$(VIRTUALENV_BIN_DIR)/twine upload dist/*
.PHONY: upload/pypi

#-------------------------------------------------------------------------------
# lint
#-------------------------------------------------------------------------------

# -- pylint --
PYLINT_DISABLE_IDS ?= W0511
PYTHON_LINTER_MAX_LINE_LENGTH ?= 80
## Python linter
lint/pylint: $(SRC_DIR)
	-@for i in $(^); do \
		echo "[INFO] running pylint on dir: [$$i]"; \
		$(VIRTUALENV_BIN_DIR)/pylint \
			--max-line-length="$(PYTHON_LINTER_MAX_LINE_LENGTH)" \
			--disable="$(PYLINT_DISABLE_IDS)" \
			"$$i"; \
	done
.PHONY: lint/pylint

# -- flake8 --
## Python styleguide enforcement
lint/flake8: $(SRC_DIR)
	-@for i in $(^); do \
		echo "[INFO] running flake8 on dir: [$$i]"; \
		$(VIRTUALENV_BIN_DIR)/flake8 \
			--max-line-length="$(PYTHON_LINTER_MAX_LINE_LENGTH)" \
			"$$i"; \
	done
.PHONY: lint/flake8

# -- mypy --
## Python static typing
lint/mypy: $(SRC_DIR)
	-@for i in $(^); do \
		echo "[INFO] running mypy on dir: [$$i]"; \
		$(VIRTUALENV_BIN_DIR)/mypy \
			"$$i"; \
	done
.PHONY: lint/mypy

# -- black --
## Python code formatter
lint/black: $(SRC_DIR)
	-@for i in $(^); do \
		echo "[INFO] running black on dir: [$$i]"; \
		$(VIRTUALENV_BIN_DIR)/black \
			--check \
			--diff \
			--line-length="$(PYTHON_LINTER_MAX_LINE_LENGTH)" \
			"$$i"; \
	done
.PHONY: lint/black

# -- bandit --
## Python security linter
lint/bandit: $(SRC_DIR)
	-@for i in $(^); do \
		echo "[INFO] running bandit on dir: [$$i]"; \
		$(VIRTUALENV_BIN_DIR)/bandit \
			--recursive \
			"$$i"; \
	done
.PHONY: lint/bandit

## Run all linters, validators, and security analyzers
lint: lint/pylint lint/flake8 lint/mypy lint/black lint/bandit
.PHONY: lint

#-------------------------------------------------------------------------------
# test
#-------------------------------------------------------------------------------

# -- pytest --
## Python Test Framework
test/pytest: $(TEST_DIR)
	-@for i in $(^); do \
		echo "[INFO] running pytest on dir: [$$i]"; \
		$(VIRTUALENV_BIN_DIR)/pytest \
			"$$i"; \
	done
.PHONY: test/pytest

# -- codecov --
## Python CodeCov Testing
test/codecov: $(TEST_DIR)
	-@for i in $(^); do \
		echo "[INFO] running DOCKER_BUILD_ARGSodecov on dir: [$$i]"; \
		$(VIRTUALENV_BIN_DIR)/pytest \
			--cov="$(SRC_DIR)" \
			"$$i"; \
	done
.PHONY: test/codecov

## Run all tests
test: test/pytest test/codecov
.PHONY: test

#-------------------------------------------------------------------------------
# git
#-------------------------------------------------------------------------------

GIT_BRANCH ?= $(shell git branch --show-current)
GIT_HASH := $(shell git rev-parse --short HEAD)

#-------------------------------------------------------------------------------
# docker
#-------------------------------------------------------------------------------

DOCKER_USER ?= hansohn
DOCKER_REPO ?= $(REPO_NAME)
DOCKER_TAG_BASE ?= $(DOCKER_USER)/$(DOCKER_REPO)

DOCKER_TAGS ?=
DOCKER_TAGS += --tag $(DOCKER_TAG_BASE):$(GIT_HASH)
ifeq ($(GIT_BRANCH), main)
DOCKER_TAGS += --tag $(DOCKER_TAG_BASE):latest
endif

DOCKER_BUILD_PATH ?= .
DOCKER_BUILD_ARGS ?=
DOCKER_BUILD_ARGS += --build-arg PYTHON_VERSION=$(PYTHON_VERSION)
DOCKER_BUILD_ARGS += $(DOCKER_TAGS)

DOCKER_PUSH_ARGS ?=
DOCKER_PUSH_ARGS += --all-tags

## Lint Dockerfile
docker/lint:
	-@if docker info > /dev/null 2>&1; then \
		echo "[INFO] Linting '$(DOCKER_BUILD_PATH)/Dockerfile'."; \
		docker run --rm -i hadolint/hadolint < $(DOCKER_BUILD_PATH)/Dockerfile; \
	else \
		echo "[ERROR] Docker 'lint' failed. Docker daemon is not Running."; \
	fi
.PHONY: docker/lint

## Docker build image
docker/build:
	-@if docker info > /dev/null 2>&1; then \
		echo "[INFO] Building '$(DOCKER_USER)/$(DOCKER_REPO)' docker image."; \
		docker build $(DOCKER_BUILD_ARGS) $(DOCKER_BUILD_PATH)/; \
	else \
		echo "[ERROR] Docker 'build' failed. Docker daemon is not Running."; \
	fi
.PHONY: docker/build

## Docker run image
docker/run:
	-@if docker info > /dev/null 2>&1; then \
		echo "[INFO] Running '$(DOCKER_USER)/$(DOCKER_REPO)' docker image"; \
		docker run -it --rm "$(DOCKER_TAG_BASE):$(GIT_HASH)" bash; \
	else \
		echo "[ERROR] Docker 'run' failed. Docker daemon is not Running."; \
	fi
.PHONY: docker/run

## Docker push image
docker/push:
	-@if docker info > /dev/null 2>&1; then \
		echo "[INFO] Pushing '$(DOCKER_USER)/$(DOCKER_REPO)' docker image"; \
		docker push $(DOCKER_PUSH_ARGS) $(DOCKER_TAG_BASE); \
	else \
		echo "[ERROR] Docker 'push' failed. Docker daemon is not Running."; \
	fi
.PHONY: docker/push

## Docker launch testing environment
docker: python/venv python/packages python/build docker/lint docker/build docker/run
.PHONY: docker

#-------------------------------------------------------------------------------
# clean
#-------------------------------------------------------------------------------

## Clean python build directories
clean/build:
	-@if [ -d '$(DIST_DIR)' ]; then \
		echo "[INFO] Cleaning python build directory '$(DIST_DIR)'"; \
		rm -rf '$(DIST_DIR)/'*; \
	fi
.PHONY: clean/build

## Clean docker build images
clean/docker:
	-@if docker info > /dev/null 2>&1; then \
		if docker inspect --type=image "$(DOCKER_TAG_BASE):$(GIT_HASH)" > /dev/null 2>&1; then \
			echo "[INFO] Removing docker image '$(DOCKER_USER)/$(DOCKER_REPO)'"; \
			docker rmi -f $$(docker inspect --format='{{ .Id }}' --type=image $(DOCKER_TAG_BASE):$(GIT_HASH)); \
		fi; \
	fi
.PHONY: clean/docker

## Clean python cache files
clean/python:
	@echo "[INFO] Cleaning python cache files";
	@find . -name "__pycache__" -type d -exec rm -rf {} +
	@find . -name ".pytest_cache" -type d -exec rm -rf {} +
	@find . -name "*.pyc" -delete
.PHONY: clean/python

## Clean virtual environment directory
clean/venv:
	@echo "[INFO] Cleaning python virtualenv directory '$(VIRTUALENV_DIR)'";
	@[ -d '$(VIRTUALENV_DIR)' ] && rm -rf '$(VIRTUALENV_DIR)/'*
.PHONY: clean/venv

## Clean everything
clean: clean/build clean/python clean/venv clean/docker
.PHONY: clean
