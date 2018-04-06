Stupid Chess
============
From the Stupid Chess [homepage](https://stupidchess.jmn23.com):

```
This is a web-based board game running on a python-flask/mongo backend with a react frontend.
It is deployed on a raspberry pi cluster running kubernetes. Visit my github to view the salt-stack
configuration, build tools, and custom docker images I've built to deploy this and other projects
on this platform.

You can see this particular project at https://github.com/norwoodj/stupidchess
You might also visit my other project https://hashbash.jmn23.com

Stupid Chess is a variant on the popular Chess and checkers board games that John Norwood (that's me)
and some of his college friends invented when we stumbled across a chess board that had been ripped
in half and an incomplete set of pieces. It has a number of delightful rule changes over these earlier
inferior games, and you can learn how to play on this page
https://stupidchess.jmn23.com/how-to-play
```

### This Codebase
This code was largely written as an exploration of how to effectively build and deploy flask/mongo/react
projects as well as a way to get the rules of a game that I really enjoy codified in a meaningful way.

Additionally, I'm a professional software developer, and my hope is that you, dear recruiter, see this
as an indication of my skillset.

This project leverages docker and docker-compose to build and run the application locally requiring
installation of minimal requirements, and with great developer ease. The same docker images that are built
to do this can be deployed to a remote docker image repository as well and there is helm configuration to
deploy these images to a kubernetes cluster. This is how I deploy this project to
https://stupidchess.jmn23.com

All of this makes heavy use of other projects that I have written:

* [jconfigure](https://github.com/norwoodj/jconfigure) - python external configuration library
* [jscripts](https://github.com/norwoodj/jscripts) - utility bash scripts, build tools, release automation
* [rpi-salt](https://github.com/norwoodj/rpi-salt) - salt-stack configuration for setting up my raspberry pis
  as a kubernetes cluster

### Building and Developing Locally
In order to build, run and develop this project locally you'll need a number of things installed:

* docker - 17.06 or newer
* docker-compose - 1.16.1 or newer
* bash - 4.4 or newer
* git
* jq

After that you must install jscripts locally on your machine, and then in this repo:
```
cd
git clone https://github.com/norwoodj/jscripts.git .jscripts
cd /path/to/stupidchess
./_jscripts-ctl.sh install
```

Once you have the requirements and scripts installed, you can build all of the docker images necessary
to run locally with:
```
./jscripts/build-images.sh all
```

This should build the three images for running locally in parallel.

You can then run with:
```
./jscripts/run-local.sh start stupidchess
```

This starts the stupidchess http server running on port 80. You can go to a browser window and open
[localhost](http://localhost) to view stupidchess running locally.

This is setup to include local code changes in the running docker containers as volumes and to use auto-reload
for the flask python server and --watch for webpack. In this way your code will get rebuilt and the server
reloaded as you make changes.