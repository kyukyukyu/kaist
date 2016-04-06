#!/bin/bash

run() {
    python dataClassifier.py $@
}

run -c GDA -t 2000
run -c GDA -t 1000
run -c GDA -t 500
run -c GDA -t 300

run -c GDA -t 60 -d faces
run -c GDA -t 100 -d faces
run -c GDA -t 200 -d faces
run -c GDA -t 400 -d faces
