from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError

from problems.router import router_theme, router_problem
from auth.router import router_jwt, router_user


app = FastAPI()


app.include_router(router_theme)
app.include_router(router_problem)
app.include_router(router_jwt, prefix="/jwt")
app.include_router(router_user, prefix="/users")
