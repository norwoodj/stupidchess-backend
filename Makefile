PYTHON_IMAGE=python:3.7.3-slim
DOCKER_REPOSITORY=jnorwood


.PHONY: all
all: uwsgi nginx webpack_builder

version.txt:
	echo release-$(shell docker run --rm --entrypoint date $(PYTHON_IMAGE) --utc "+%Y%m%d-%H%M") > version.txt

_version.json: version.txt
	cat version.txt > _version.json

.PHONY: nginx
nginx: _version.json
	cp _version.json web/src/
	docker build -t $(DOCKER_REPOSITORY)/stupidchess-nginx:current -f docker/Dockerfile-nginx .

.PHONY: uwsgi
uwsgi:
	docker build -t $(DOCKER_REPOSITORY)/stupidchess-uwsgi:current -f docker/Dockerfile-uwsgi .

.PHONY: webpack_builder
webpack_builder:
	docker build -t $(DOCKER_REPOSITORY)/stupidchess-webpack_builder:current -f docker/Dockerfile-webpack_builder .

.PHONY: push
push: nginx uwsgi version.txt
	docker tag $(DOCKER_REPOSITORY)/stupidchess-uwsgi:current $(DOCKER_REPOSITORY)/stupidchess-uwsgi:$(shell cat version.txt)
	docker tag $(DOCKER_REPOSITORY)/stupidchess-nginx:current $(DOCKER_REPOSITORY)/stupidchess-nginx:$(shell cat version.txt)
	docker push $(DOCKER_REPOSITORY)/stupidchess-uwsgi:$(shell cat version.txt)
	docker push $(DOCKER_REPOSITORY)/stupidchess-nginx:$(shell cat version.txt)

.PHONY: run
run: all
	docker-compose -f docker/docker-compose.yaml up

.PHONY: run-no-build
run-no-build:
	docker-compose -f docker/docker-compose.yaml up

.PHONY: clear-data
clear-data:
	docker-compose -f docker/docker-compose.yaml down

.PHONY: clean
clean:
	rm -f version.txt _version.json web/src/_version.json
