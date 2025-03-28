#!/bin/bash

for v in {90..5000}; do
  sed -i "s/version.*/version = '0.0.$v'/" pyproject.toml
  echo "v=$v" `grep version pyproject.toml`

  rm ./dist/*
  python3 -m build

  #python3 -m twine upload --verbose --repository-url https://us-central1-python.pkg.dev/gregherman2017/repo1/  dist/*

 # for pypi: https://pypi.org/help/#apitoken
 # gregh1
  python3 -m twine upload --verbose dist/* -u __token__ -p pypi-AgEIcHlwaS5vcmcCJDFhNmI1ZjVkLTAyNzktNDM3NS1hNDM4LTZmZjMzMjk0NmEwNAACG1sxLFsiZXhhbXBsZTEtcmVwcm9pNTAwMCJdXQACLFsyLFsiODdkOTVmMTItNjE4OC00NGUyLTg1MzUtZjQ3MDgyZDZkYmFiIl1dAAAGIL2Cv3J6Lc7w-XdjnkKEormZj9RZDVfoycuTBXVIsZ74
done

