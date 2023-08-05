Stupid Chess
============

![active-game](board.png)

From the Stupid Chess homepage:

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


### Building and Developing Locally
There is a docker-compose setup for running locally. To start run the following,
then navigate to http://localhost:23180 in your browser.
```
make run
```

This is setup to include local code changes in the running docker containers as volumes and to use auto-reload
for the flask python server and --watch for webpack. In this way your code will get rebuilt and the server
reloaded as you make changes.

### Releasing
There's a make target for releasing
```
make release
```

This is only tested on linux and requires you have installed some dependencies with:
```
sudo apt install git-buildpackage
```

### Building Debian Package
There's a make target for building this project's debian package
```
make deb
```

This is only tested on linux and requires you have installed some dependencies with:
```
sudo apt install devscripts debhelper dh-virtualenv
```

