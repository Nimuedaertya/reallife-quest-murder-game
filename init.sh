#!/bin/bash

# https://stackoverflow.com/questions/29436275/how-to-prompt-for-yes-or-no-in-bash#29436423
function yes_or_no {
    while true; do
        read -p "$* [y/n]: " yn
        case $yn in
            [Yy]*) return 0  ;;
            [Nn]*) echo "Aborted" ; return  1 ;;
        esac
    done
}

# installing required packages
pip install poetry
poetry install

yes_or_no "Have you added all players in config/players.yml ?"

yes_or_no "Have you added and configured all roles in config/roles.yml ?"

yes_or_no "Have you added all tasks in config/tasks/*.yml ?"

echo "Generating QR Codes"

# clean if exists, create directory for qr_codes
rm -rf qr_codes
mkdir qr_codes

# run script to create qr_codes
poetry run python3 src/qr_codes.py

echo "PDFs (for printing) or single QR codes as png in directory qr_codes"
