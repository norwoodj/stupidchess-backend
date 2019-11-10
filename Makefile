DOCKER_REPOSITORY := jnorwood
PYTHON_IMAGE := python:3.7-slim
VERSION_PLACEHOLDER := _VERSION
VERSION_FILES := setup.py debian/changelog debian/control


default:
	@echo "Available Targets:"
	@echo
	@echo "  clean      - Delete all build artifacts and clean up versioning"
	@echo "  deb        - Build debian archive"
	@echo "  down       - Tear down the local docker database"
	@echo "  uwsgi      - Build the stupidchess-uwsgi docker image"
	@echo "  push       - Push the uwsgi docker image"
	@echo "  run-docker - Run the app locally in docker"


##
# Versioning targets
##
version.txt:
	docker run --rm --entrypoint date $(PYTHON_IMAGE) --utc "+%y.%m%d.0" > version.txt

update-versions: version.txt
	sed -i "s|$(VERSION_PLACEHOLDER)|$(shell cat version.txt)|g" $(VERSION_FILES)
	touch update-versions


##
# Docker images
##
.PHONY: uwsgi
uwsgi: update-versions
	docker-compose build

.PHONY: push
push: image
	docker tag $(DOCKER_REPOSITORY)/stupidchess-uwsgi:current $(DOCKER_REPOSITORY)/stupidchess-uwsgi:$(shell cat version.txt)
	docker push $(DOCKER_REPOSITORY)/stupidchess-uwsgi:$(shell cat version.txt)


##
# debian packaging
##
.PHONY: deb
deb: update-versions
	dpkg-buildpackage -us -uc

.PHONY: clean
clean: version.txt
	sed -i "s|$(shell cat version.txt)|$(VERSION_PLACEHOLDER)|g" $(VERSION_FILES)
	rm -f version.txt update-versions


##
# Run application
##
.PHONY: run-docker
run-docker:
	docker-compose up

.PHONY: down
down:
	docker-compose down
