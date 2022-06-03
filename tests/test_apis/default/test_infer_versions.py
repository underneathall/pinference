import pytest
from fastapi.testclient import TestClient

from .data import inference_data

TEST_URL = "/v1/models/{model_name}/versions/{version_name}/predict"


@pytest.mark.parametrize("inference_data", inference_data)
@pytest.mark.parametrize("version_name", ["default", "v1"])
def test_predict_json_model_versions(
    json_model_default_service,
    inference_data,
    version_name,
):
    client = TestClient(json_model_default_service)
    response = client.post(
        TEST_URL.format(model_name="json", version_name=version_name),
        json=inference_data["request"],
    )
    assert response.status_code == 200
    assert response.json()["data"] == inference_data["response"]["data"]


@pytest.mark.parametrize(
    "inference_data",
    [
        {
            "version_name": "add",
            "request": {"data": [2, 1]},
            "response": {"data": 3},
        },
        {
            "version_name": "substract",
            "request": {"data": [2, 1]},
            "response": {"data": 1},
        },
    ],
)
def test_different_entrypoint(
    add_substract_model_default_service,
    inference_data,
):
    client = TestClient(add_substract_model_default_service)
    response = client.post(
        TEST_URL.format(
            model_name="mymodel",
            version_name=inference_data["version_name"],
        ),
        json=inference_data["request"],
    )
    assert response.status_code == 200
    assert response.json()["data"] == inference_data["response"]["data"]