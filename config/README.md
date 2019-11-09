Stupid Chess Configuration
==========================
This directory is copied into docker images and used as a volume when running locally in order
to configure the stupidchess application. The configuration uses a number of custom yaml tags
that are implemented in and supported by my other project [jconfigure](https://github.com/norwoodj/jconfigure)
which is a python library for configuring applications using files like these.

### Files
The files of note in here are:

* `defaults.yaml` - Read to configure the app in all environments, thus the name defaults
* `logging.yaml` - Read to configure the loggers for this project in all environments
* `LCL.yaml` - Read to configure the app running locally
* `RPI.yaml` - Read to configure this app running in "production" on my raspberry pi cluster
  at home. For info how I do this visit my other projects at my [github](https://github.com/norwoodj)
