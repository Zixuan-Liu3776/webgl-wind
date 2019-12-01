#!/bin/bash

python convertGeoTiff.py th_2017.tif vs_2017.tif

DIR=`dirname $0`
node ${DIR}/prepare.js ${1}/output

rm tmp.json
