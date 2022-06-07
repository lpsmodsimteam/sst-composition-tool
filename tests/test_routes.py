from pathlib import Path

from app import create_app
from app.db.checkpoint import clear_checkpoints


# get the resources folder in the tests folder
RESOURCES = Path(__file__).parent / "resources"


def test_export_success():

    app = create_app()
    client = app.test_client()
    url = "/export"

    with open(RESOURCES / "sample_form.json") as fp:
        response = client.post(url, data={"drawflow_data": fp.read()})
        assert response.status_code == 200
        clear_checkpoints("library_name")
