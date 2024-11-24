# uob-sepp-prototype
Prototype for UOB Software Engineering &amp; Professional Practice Module
## Prerequesites
Check you have the following installed:
- [python 3.12+](https://www.python.org/downloads/) (Check with `python --version`)
- [Poetry](https://python-poetry.org/) (Check with `poetry --version`)
## Install Project Dependencies
Go to the directory with pyproject.toml (this should be the directory you cloned the repo to), and run
```
poetry install
```
This will automatically install the correct versions of required dependencies
## Running the Application
Poetry will automatically create a virtual environment for your project. Acviate it with:
```
poetry shell
```
Once the virtual environment is activated, you can run the app with:
```
poetry run python app.py
```
This will run the application.
