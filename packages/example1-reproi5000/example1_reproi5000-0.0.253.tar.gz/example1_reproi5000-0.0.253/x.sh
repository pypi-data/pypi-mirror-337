#!/bin/bash

for v in {154..5000}; do
  sed -i "s/version.*/version = '0.0.$v'/" pyproject.toml
  echo "v=$v" `grep version pyproject.toml`

  rm ./dist/*
  python3 -m build

  #python3 -m twine upload --verbose --repository-url https://us-central1-python.pkg.dev/gregherman2017/repo1/  dist/*

 # for pypi: https://pypi.org/help/#apitoken
 # gregh1
  python3 -m twine upload --verbose dist/* -u __token__ -p pypi-AgEIcHlwaS5vcmcCJGZhZTgxYTY0LTRkZTctNGFjZC04MjY0LTMxNTc1MjZjNWVkMwACG1sxLFsiZXhhbXBsZTEtcmVwcm9pNTAwMCJdXQACLFsyLFsiODdkOTVmMTItNjE4OC00NGUyLTg1MzUtZjQ3MDgyZDZkYmFiIl1dAAAGIMEjgyk8819goOSE-N-c39qrPBjyvWFKzjdiV-cfXd_J
done

