# SST Hierarchical Composition Tool

## Installation

The application runs on the micro web framework, [Flask](https://flask.palletsprojects.com/en/2.0.x/), which can be installed through pip:

`pip install flask`

Basic configurations are required to set up Flask and run the application. The following environment variables must be set:

```shell
export FLASK_APP=app/__init__.py
export FLASK_ENV=development
```

To avoid setting these variables every time, use Python-dotenv. Install through pip

`pip install python-dotenv`

and save a file named `.env` in the root directory with the following content:

```
FLASK_APP=app/__init__.py
FLASK_ENV=development
DEBUG=True
FLASK_RUN_PORT=8000
```

Once the Flask variables are set, execute `flask run` and run the application on the specified port in your browser.

## Testing

The application can be tested with `pytest`. Install through pip

`pip install pytest`

Run the tests located in `/tests`

`pytest -v`
