from pathlib import Path

from app import create_app

# get the resources folder in the tests folder
resources = Path(__file__).parent / "resources"


def test_export_drawflow_data_success():

    app = create_app()
    client = app.test_client()
    url = "/export_drawflow_data"

    with open(resources / "sample_form.json") as fp:
        response = client.post(url, data={"drawflow_data": fp.read()})
        assert response.status_code == 200
