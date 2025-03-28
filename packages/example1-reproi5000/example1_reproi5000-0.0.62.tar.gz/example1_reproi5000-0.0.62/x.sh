#!/bin/bash

for v in {2..5000}; do
  sed -i "s/version.*/version = '0.0.$v'/" pyproject.toml
  echo "v=$v" `grep version pyproject.toml`

  rm ./dist/*
  python3 -m build

  #python3 -m twine upload --verbose --repository-url https://us-central1-python.pkg.dev/gregherman2017/repo1/  dist/*

 # for pypi: https://pypi.org/help/#apitoken
 # gregh1
  python3 -m twine upload --verbose dist/* -u __token__ -p pypi-AgEIcHlwaS5vcmcCJGJkNDk0MDE0LWY5YjItNGVhNC05ZDQwLTgzYzY2ZDdkZDRiMwACKlszLCJlYzEyNjcyOC02M2RhLTRmOTQtOTljMi1hZDA3NzY4ODM5YmMiXQAABiA_ExUs4GwHUxhffsnMJ2dmXjx8Bu8wkZGYCpILSv6sKw
done

