from fastapi import APIRouter, Request

from pinferencia.apis.kserve.v1.config import SCHEME
from pinferencia.apis.kserve.v1.models import Request as InferenceRequest
from pinferencia.apis.kserve.v1.models import Response as InferenceResponse
from pinferencia.apis.kserve.v1.parsers import InputParser, OutputParser
from pinferencia.context import PredictContext

router = APIRouter()


@router.post(
    "/models/{model_name}/infer",
    response_model=InferenceResponse,
    response_model_exclude_unset=True,
    response_model_exclude_none=True,
)
async def model_predict(
    request: Request,
    model_name: str,
    inference_request: InferenceRequest,
):
    return {
        "id": inference_request.id,
        "model_name": model_name,
        "predictions": OutputParser(
            request.app.model.predict(
                model_name,
                data=InputParser(inference_request).data,
                parameters=inference_request.parameters,
                context=PredictContext(
                    scheme=SCHEME, request_data=inference_request.dict()
                ),
            ),
        ).data,
    }


@router.post(
    "/models/{model_name}/versions/{version_name}/infer",
    response_model=InferenceResponse,
    response_model_exclude_unset=True,
    response_model_exclude_none=True,
)
async def model_version_predict(
    request: Request,
    model_name: str,
    version_name: str,
    inference_request: InferenceRequest,
):
    return {
        "id": inference_request.id,
        "model_name": model_name,
        "model_version": version_name,
        "predictions": OutputParser(
            request.app.model.predict(
                model_name,
                data=InputParser(inference_request).data,
                parameters=inference_request.parameters,
                version_name=version_name,
                context=PredictContext(
                    scheme=SCHEME, request_data=inference_request.dict()
                ),
            ),
        ).data,
    }
