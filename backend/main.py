from fastapi import FastAPI
from sqlalchemy.exc import IntegrityError

from views.participants import participants_router
from exc_handlers.base import value_error_handler, related_errors_handler

app = FastAPI(title="Test participants app")

exc_handlers = {
    ValueError: value_error_handler,
    IntegrityError: related_errors_handler,
}
routers = {
    "/clients": participants_router,
}

for exception, handler in exc_handlers.items():
    app.add_exception_handler(exception, handler)

for prefix, router in routers.items():
    app.include_router(router, prefix=prefix, tags=["api/"])
