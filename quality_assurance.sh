#poetry run pylint src/*.py
poetry run flake8 --max-line-length 120 --ignore=E131,E126,E123
poetry run coverage run -m pytest
poetry run coverage report
