from fastapi import FastAPI
from src.routes.report import report 

app = FastAPI()


app.include_router(report)
