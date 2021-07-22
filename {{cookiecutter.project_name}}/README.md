# {{ cookiecutter.project_title }}

{{ cookiecutter.project_desc }}


## Building Instructions

### Locally (Package Only)

To build the operator package locally, you need to ensure that you have
[poetry](https://python-poetry.org/) installed on your machine, along with an
appropriate version of python. To get started, install the package dependencies
via executing the following command within this directory:

```bash
$ poetry install --no-dev --no-root
```

If you wish to be able to run tests on the package (see below), you can omit the
`--no-dev` flag.

Next, build the package by running the following:

```bash
$ poetry build -f wheel
```

The above command will generate a `.whl` package within the `dists` directory.
From there you may install the package via `pip install`.


### Using Docker (For Kubernetes)

To build a container image which may be leveraged within a kubernetes cluster,
execute the `build-image.sh` script within this directory. Ensure that you have
`docker` installed on your machine. This script will create an image of the form:

```
{{ cookiecutter.crd_group }}/{{ cookiecutter.project_name }}:VERSION
```

where `VERSION` corresponds to the value of the `version` variable within
`pyproject.toml`. Note that the docker build process will automatically run
`pytest` on the package, and that development dependencies are stripped from the
container image before completion.

Before deploying the image to a registry, be sure to re-tag it as `latest` by
executing the following:

```bash
$ docker tag '{{ cookiecutter.crd_group }}/{{ cookiecutter.project_name }}:VERSION' '{{ cookiecutter.crd_group }}/{{ cookiecutter.project_name }}:latest'
```

again, replacing `VERSION` with the version defined within `pyproject.toml`.
