from fastapi import FastAPI

from problems.router import router_theme, router_problem
from auth.router import router as auth_router

app = FastAPI()

app.include_router(router_theme)
app.include_router(router_problem)
app.include_router(auth_router, prefix="/jwt")
