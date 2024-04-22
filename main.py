from fastapi import FastAPI

from problems.router import router_theme, router_problem, router_question
from auth.router import router_jwt, router_user


app = FastAPI()


app.include_router(router_theme)
app.include_router(router_problem)
app.include_router(router_question)
app.include_router(router_jwt, prefix="/jwt")
app.include_router(router_user, prefix="/users")
