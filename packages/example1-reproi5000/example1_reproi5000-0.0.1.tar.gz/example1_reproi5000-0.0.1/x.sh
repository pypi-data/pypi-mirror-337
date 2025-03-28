#!/bin/bash

for v in {11..9000}; do
  sed -i "s/version.*/version = '0.0.$v'/" pyproject.toml
  echo "v=$v" `grep version pyproject.toml`

  rm ./dist/*
  python3 -m build

  python3 -m twine upload --verbose --repository-url https://us-central1-python.pkg.dev/gregherman2017/repo1/  dist/*
done

