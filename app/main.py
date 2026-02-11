import os
import time
from fastapi import FastAPI

app = FastAPI(title="myapp")

APP_NAME = os.getenv("APP_NAME", "myapp")
ENV = os.getenv("ENV", "dev")

@app.get("/healthz")
def healthz():
    return {"status": "All Good My G", "app": APP_NAME, "env": ENV}

@app.get("/")
def root():
    return {"message": f"Hello from {APP_NAME}", "env": ENV}

@app.get("/work")
def work(ms: int = 200):
    """
    Lite CPU-arbeid for å gjøre det enklere å trigge HPA (bruk /work?ms=500 osv).
    """
    end = time.time() + (ms / 1000.0)
    x = 0
    while time.time() < end:
        x = (x * 17 + 11) % 1000003
    return {"did_work_ms": ms, "result": x, "env": ENV}
