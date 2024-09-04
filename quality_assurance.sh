#!/bin/bash

#poetry run pylint src/*.py
poetry run flake8 --max-line-length 120 --ignore=E131,E126,E123
poetry run coverage run -m pytest
poetry run coverage report
poetry run djlint src/templates/* --profile=jinja

shellcheck init.sh
shellcheck run.sh
shellcheck quality_assurance.sh

# ( poetry run python3 src/endpoints.py --port 5001) &
# PID1=$!
# ( poetry run python3 src/endpoints.py -s) & 
# PID2=$!
# sleep 5
# kill $PID1
# kill $PID2
