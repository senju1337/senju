#!/bin/bash
sphinx-apidoc -o source/_modules ../senju
poetry run make clean
poetry run make html