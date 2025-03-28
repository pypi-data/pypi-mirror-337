#!/bin/bash

for v in {342..5000}; do
  sed -i "s/version.*/version = '0.0.$v'/" pyproject.toml
  echo "v=$v" `grep version pyproject.toml`

  rm ./dist/*
  python3 -m build

  #python3 -m twine upload --verbose --repository-url https://us-central1-python.pkg.dev/gregherman2017/repo1/  dist/*

 # for pypi: https://pypi.org/help/#apitoken
 # gregh1
  python3 -m twine upload --verbose dist/* -u __token__ -p pypi-AgEIcHlwaS5vcmcCJDJkM2VhMTg5LTgyMmYtNDExMS04YTZlLTFjNDYzYTVjOTg3ZQACG1sxLFsiZXhhbXBsZTEtcmVwcm9pNTAwMCJdXQACLFsyLFsiODdkOTVmMTItNjE4OC00NGUyLTg1MzUtZjQ3MDgyZDZkYmFiIl1dAAAGIFC1z-y25qSPUVgQYMJP2vWCPw7bZFb5_WsM-BIdVPf7
done

