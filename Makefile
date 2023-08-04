DOCKER_REPOSITORY := jnorwood

# Nothing to do for the build target, since dh-virtualenv packages the python files
build:
	:

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
