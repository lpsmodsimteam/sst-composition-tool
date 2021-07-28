# SST Hierarchical Composition Tool

## Installation

The application runs on the basic dependencies required by Flask. Install the dependencies through pip: `pip install flask`.

### Setup and execution

Basic configurations are required to set up Flask and run the application. The following environment variables must be set:
```shell
export FLASK_APP=app/__init__.py
export FLASK_ENV=development
```

To avoid setting these variables every time, use Python-dotenv. Install through pip `pip install python-dotenv` and save a file named `.env` on the root directory with the following content:
```
FLASK_APP=app/__init__.py
FLASK_ENV=development
DEBUG=True
FLASK_RUN_PORT=8000
```

Once the Flask variables are set, execute `flask run` and use the application on your browser.
