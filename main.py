from fastapi import FastAPI

from problems.router import router_theme, router_problem

app = FastAPI()

app.include_router(router_theme)
app.include_router(router_problem)
