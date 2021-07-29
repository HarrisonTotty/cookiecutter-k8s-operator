#!/usr/bin/env bash
# A handy script for building the operator image.

set -e

trap 'exit 100' INT

VERSION=$(grep -oP '^version\s*=\s*"\d+\.\d+\.\d+"$' pyproject.toml | awk -F '"' '{ print $2 }')

docker build -t "{{ cookiecutter.crd_group }}/{{ cookiecutter.project_name }}:${VERSION}" .
