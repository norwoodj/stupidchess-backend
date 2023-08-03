DOCKER_REPOSITORY := jnorwood

.PHONY: help
help:
	@echo "Available Targets:"
	@echo
	@echo "  release - Create a new release commit and tag"
	@echo "  deb     - Build debian archive"
	@echo "  down    - Tear down the local docker database"
	@echo "  uwsgi   - Build the stupidchess-uwsgi docker image"
	@echo "  push    - Push the uwsgi docker image"
	@echo "  run     - Run the app locally in docker"

release:
	./release.sh

deb:
	debuild

uwsgi:
	docker-compose build uwsgi

push: uwsgi
	docker tag $(DOCKER_REPOSITORY)/stupidchess-uwsgi:current $(DOCKER_REPOSITORY)/stupidchess-uwsgi:$(shell git tag -l | tail -n1)
	docker push $(DOCKER_REPOSITORY)/stupidchess-uwsgi:$(shell git tag -l | tail -n1)

run:
	docker-compose up

down:
	docker-compose down --volumes
