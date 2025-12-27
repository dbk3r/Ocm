import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .api import api_router
from .scheduler import start_scheduler

app = FastAPI()
app.mount("/", StaticFiles(directory="static", html=True), name="static")
app.include_router(api_router)

@app.on_event("startup")
def startup_event():
    start_scheduler()
