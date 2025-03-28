#!/bin/bash

for v in {465..5000}; do
  sed -i "s/version.*/version = '0.0.$v'/" pyproject.toml
  echo "v=$v" `grep version pyproject.toml`

  rm ./dist/*
  python3 -m build

  #python3 -m twine upload --verbose --repository-url https://us-central1-python.pkg.dev/gregherman2017/repo1/  dist/*

 # for pypi: https://pypi.org/help/#apitoken
 # gregh1
  python3 -m twine upload --verbose dist/* -u __token__ -p pypi-AgEIcHlwaS5vcmcCJGY4Yjk0YmRjLTBkNGQtNGM3ZS1hOTM3LTExMjYyMTVlM2VlMAACG1sxLFsiZXhhbXBsZTEtcmVwcm9pNTAwMCJdXQACLFsyLFsiODdkOTVmMTItNjE4OC00NGUyLTg1MzUtZjQ3MDgyZDZkYmFiIl1dAAAGIGvmykvtWaKDWcDRCu8m2Vy74keP-Mc8H6reHjEpqS2Q
done

