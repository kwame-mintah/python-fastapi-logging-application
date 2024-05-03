from fastapi import Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.models.event_models import EventsErrorMessage


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Override the default RequestValidationError exception, we want to return HTTP status code of 400
    and provide details. Rather than default of HTTP status code of 422
    """
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder(
            EventsErrorMessage(
                detail=[
                    error["msg"] + " found in " + str(error["loc"])
                    for error in exc.errors()
                ]
            )
        ),
    )
