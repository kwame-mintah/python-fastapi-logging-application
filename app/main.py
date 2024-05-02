import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from app.exceptions.events_exceptions import validation_exception_handler
from app.routers import events

app = FastAPI()
app.include_router(events.router)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000)
