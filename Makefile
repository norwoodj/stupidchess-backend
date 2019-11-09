DOCKER_REPOSITORY := jnorwood
PYTHON_IMAGE := python:3.7.3-slim
VERSION_PLACEHOLDER := _VERSION


default:
	@echo "Available Targets:"
	@echo
	@echo "  clean - Delete all build artifacts and clean up versioning"
	@echo "  down  - Tear down the local docker database"
	@echo "  image - Build the stupidchess-uwsgi docker image"

version.txt:
	docker run --rm --entrypoint date $(PYTHON_IMAGE) --utc "+%y.%m%d.0" > version.txt

.PHONY: update-setup-py
update-setup-py: version.txt
	sed -i "" "s|$(VERSION_PLACEHOLDER)|$(shell cat version.txt)|g" setup.py

.PHONY: image
image: update-setup-py
	docker-compose build

.PHONY: run-docker
run-docker:
	docker-compose up

.PHONY: clean
clean: version.txt
	sed -i "" "s|$(shell cat version.txt)|$(VERSION_PLACEHOLDER)|g" setup.py
	rm -f version.txt

.PHONY: down
down:
	docker-compose down
