PYTHON_IMAGE := python:3.7.3-slim
DOCKER_REPOSITORY := jnorwood
CURRENT_VERSION := $(shell echo release-$(shell docker run --rm --entrypoint date $(PYTHON_IMAGE) --utc "+%Y%m%d-%H%M") > version.txt)


default:
	@echo "Available Targets:"
	@echo
	@echo "  clean      - Delete all build artifacts and clean up versioning"
	@echo "  clear-data - Tear down the local docker database"
	@echo "  image      - Build the stupidchess-uwsgi docker image"

.PHONY: image
image:
	docker-compose build

.PHONY: run-docker
run-docker:
	docker-compose up

.PHONY: clean
clean: 
	sed -i "" "s|$(CURRENT_VERSION)|$(VERSION_PLACEHOLDER)|g" setup.py

.PHONY: clear-data
clear-data:
	docker-compose down
