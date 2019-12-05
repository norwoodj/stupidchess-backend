DOCKER_REPOSITORY := jnorwood
VERSION_PLACEHOLDER := _VERSION
VERSION_FILES := setup.py


##
# Build targets
##
.PHONY: help
help:
	@echo "Available Targets:"
	@echo
	@echo "  clean      - Delete all build artifacts and clean up versioning"
	@echo "  deb        - Build debian archive"
	@echo "  down       - Tear down the local docker database"
	@echo "  uwsgi      - Build the stupidchess-uwsgi docker image"
	@echo "  push       - Push the uwsgi docker image"
	@echo "  run-docker - Run the app locally in docker"

release: push
	git tag $(cat version.txt)
	git push --tags


##
# Versioning targets
##
version.txt:
	date --utc "+%y.%m%d.0" > version.txt

update-versions: version.txt
	sed -i "s|$(VERSION_PLACEHOLDER)|$(shell cat version.txt)|g" $(VERSION_FILES)
	touch update-versions

update-deb-version: version.txt
	sed -i "s|$(VERSION_PLACEHOLDER)|$(shell cat version.txt)|g" debian/changelog
	touch update-deb-version



##
# debian packaging
##
.PHONY: deb
deb: update-deb-version update-versions
	debuild


##
# Docker images
##
.PHONY: uwsgi
uwsgi: update-versions
	docker-compose build

.PHONY: push
push: uwsgi
	docker tag $(DOCKER_REPOSITORY)/stupidchess-uwsgi:current $(DOCKER_REPOSITORY)/stupidchess-uwsgi:$(shell cat version.txt)
	docker push $(DOCKER_REPOSITORY)/stupidchess-uwsgi:$(shell cat version.txt)


##
# Run application
##
.PHONY: run-docker
run-docker:
	docker-compose up

.PHONY: down
down:
	docker-compose down


##
# Cleanup
##
.PHONY: clean
clean: version.txt
	sed -i "s|$(shell cat version.txt)|$(VERSION_PLACEHOLDER)|g" $(VERSION_FILES)
	rm -f version.txt update-versions

.PHONY: cleaner
cleaner: version.txt
	sed -i "s|$(shell cat version.txt)|$(VERSION_PLACEHOLDER)|g" $(VERSION_FILES) debian/changelog
	rm -rf dist version.json src/version.json version.txt update-versions update-deb-versions
