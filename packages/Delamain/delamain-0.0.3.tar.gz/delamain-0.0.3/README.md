# Delamain

[![Release](https://img.shields.io/github/v/release/ai-zerolab/Delamain)](https://img.shields.io/github/v/release/ai-zerolab/Delamain)
[![Build status](https://img.shields.io/github/actions/workflow/status/ai-zerolab/Delamain/main.yml?branch=main)](https://github.com/ai-zerolab/Delamain/actions/workflows/main.yml?query=branch%3Amain)
[![codecov](https://codecov.io/gh/ai-zerolab/Delamain/branch/main/graph/badge.svg)](https://codecov.io/gh/ai-zerolab/Delamain)
[![Commit activity](https://img.shields.io/github/commit-activity/m/ai-zerolab/Delamain)](https://img.shields.io/github/commit-activity/m/ai-zerolab/Delamain)
[![License](https://img.shields.io/github/license/ai-zerolab/Delamain)](https://img.shields.io/github/license/ai-zerolab/Delamain)

This is a template repository for Python projects that use uv for their dependency management.

- **Github repository**: <https://github.com/ai-zerolab/Delamain/>
- **Documentation** <https://ai-zerolab.github.io/Delamain/>

## Getting started with your project

### 1. Create a New Repository

First, create a repository on GitHub with the same name as this project, and then run the following commands:

```bash
git init -b main
git add .
git commit -m "init commit"
git remote add origin git@github.com:ai-zerolab/Delamain.git
git push -u origin main
```

### 2. Set Up Your Development Environment

Then, install the environment and the pre-commit hooks with

```bash
make install
```

This will also generate your `uv.lock` file

### 3. Run the pre-commit hooks

Initially, the CI/CD pipeline might be failing due to formatting issues. To resolve those run:

```bash
uv run pre-commit run -a
```

### 4. Commit the changes

Lastly, commit the changes made by the two steps above to your repository.

```bash
git add .
git commit -m 'Fix formatting issues'
git push origin main
```

You are now ready to start development on your project!
The CI/CD pipeline will be triggered when you open a pull request, merge to main, or when you create a new release.

To finalize the set-up for publishing to PyPI, see [here](https://fpgmaas.github.io/cookiecutter-uv/features/publishing/#set-up-for-pypi).
For activating the automatic documentation with MkDocs, see [here](https://fpgmaas.github.io/cookiecutter-uv/features/mkdocs/#enabling-the-documentation-on-github).
To enable the code coverage reports, see [here](https://fpgmaas.github.io/cookiecutter-uv/features/codecov/).

## Releasing a new version

- Create an API Token on [PyPI](https://pypi.org/).
- Add the API Token to your projects secrets with the name `PYPI_TOKEN` by visiting [this page](https://github.com/ai-zerolab/Delamain/settings/secrets/actions/new).
- Create a [new release](https://github.com/ai-zerolab/Delamain/releases/new) on Github.
- Create a new tag in the form `*.*.*`.

For more details, see [here](https://fpgmaas.github.io/cookiecutter-uv/features/cicd/#how-to-trigger-a-release).

______________________________________________________________________

Repository initiated with [wh1isper/cookiecutter-uv](https://github.com/wh1isper/cookiecutter-uv).
