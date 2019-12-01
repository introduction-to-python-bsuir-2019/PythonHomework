#!/bin/bash

# Run this script to launch the tests
nosetests --with-coverage --cover-erase --cover-package=rss_reader --cover-html --traverse-namespace
