#!/bin/bash

PROJECT_PATH='/home/victor/coding/projects/hnstats'

VIRTUAL_ENV="${PROJECT_PATH}/env"
export VIRTUAL_ENV

PATH="$VIRTUAL_ENV/bin:$PATH"
export PATH

PAGES_TO_FETCH=5

# Execute script.
cd $PROJECT_PATH
python scraper.py $@
#python scraper.py --pages $PAGES_TO_FETCH --save