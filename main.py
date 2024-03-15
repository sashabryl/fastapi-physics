from fastapi import FastAPI

from problems.router import router as problems_router

app = FastAPI()

app.include_router(problems_router)
