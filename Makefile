DOCKER_REPOSITORY := jnorwood

# Nothing to do for the build target, since dh-virtualenv packages the python files
build:
	:

release:
	./scripts/release.sh

deb: version.json
	mv version.json stupidchess
	debuild

version.json:
	echo '{"build_timestamp": "$(shell date --utc --iso-8601=seconds)", "git_revision": "$(shell git rev-parse HEAD)", "version": "$(shell git describe)"}' | jq . > version.json

uwsgi: version.json
	mv version.json stupidchess
	docker-compose build uwsgi

push: uwsgi
	docker tag $(DOCKER_REPOSITORY)/stupidchess-uwsgi $(DOCKER_REPOSITORY)/stupidchess-uwsgi:$(shell git tag -l | tail -n1)
	docker push $(DOCKER_REPOSITORY)/stupidchess-uwsgi:$(shell git tag -l | tail -n1)

run:
	docker-compose up

down:
	docker-compose down --volumes

clean:
	rm -vf version.json stupidchess/version.json
