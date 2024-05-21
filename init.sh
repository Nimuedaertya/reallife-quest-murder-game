#!/bin/sh

# TODO check for tasks, players

# clean if exists, create directory for qr_codes
rm -rf qr_codes
mkdir qr_codes

# run script to create qr_codes
poetry run python3 src/qr_codes.py
