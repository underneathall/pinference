import sys
from unittest.mock import MagicMock

import pytest

from pinferencia.handlers import TorchScriptHandler
from tests.models.sum_product_model import SumProductModel


def test_load(monkeypatch):
    torch_mock = MagicMock()
    model = MagicMock()
    torch_mock.jit.load.return_value = model
    monkeypatch.setitem(sys.modules, "torch", torch_mock)
    # define model path
    model_path = "model.pt"
    # load model
    handler = TorchScriptHandler(model_path=model_path, entrypoint="predict")
    handler.load_model()
    assert torch_mock.cuda.is_available.call_count == 1
    assert torch_mock.device.call_count == 1
    assert torch_mock.jit.load.call_count == 1
    assert model.eval.call_count == 1


def test_load_error(monkeypatch):
    torch_mock = MagicMock()
    monkeypatch.setitem(sys.modules, "torch", torch_mock)
    model = SumProductModel()
    handler = TorchScriptHandler(model=model)
    with pytest.raises(Exception) as exc:
        handler.load_model()
    assert "Model path not provided." == str(exc.value)


def test_predict_error(monkeypatch):
    torch_mock = MagicMock()
    monkeypatch.setitem(sys.modules, "torch", torch_mock)
    handler = TorchScriptHandler(model_path="abc")
    with pytest.raises(Exception) as exc:
        handler.predict([1, 2])
    assert "Model is not loaded." == str(exc.value)


def test_import_error(monkeypatch):
    handler = TorchScriptHandler(model_path="abc.pt")
    monkeypatch.setitem(sys.modules, "torch", None)
    with pytest.raises(Exception) as exc:
        handler.load_model()
    assert "pytorch not installed." == str(exc.value)
