#!/bin/bash
if [ -f .coverage ]; then
    echo "delete old .coverage-file..."
    rm .coverage
fi
echo "run coverage test..."
poetry run coverage run -m pytest
poetry run coverage annotate --directory=tests/coverage/report
echo "generate coverage report..."
poetry run coverage report
echo "-----------------------------------------------------------------------"
echo "available report file/s"
rm .coverage
cd tests/coverage/report || exit
ls
echo "-----------------------------------------------------------------------"
echo "Go to tests/coverage/report to open a file for further information
about covered and not covered code lines"
cd ../../../
if [ -d ".pytest_cache" ]; then
  read -r -p "do you want to remove .pytest_cache (y/n)?" decision
  if [[ "$decision" == "y" ]] || [[ "$decision" == "Y" ]]; then
    echo "deleting pytest cache..."
    rm -r .pytest_cache
  else
    echo "Die .coverage-Datei wurde nicht gelöscht."
  fi
fi
