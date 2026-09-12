import os 
from contextlib import asynccontextmanager
import joblib
import time
import redis 
from fastapi import FastAPI, Response
from pydantic import BaseModel
MODEL_PATH = os.environ.get("MODEL_PATH", "model.joblib")
REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT = int(os.environ.get("REDIS_PORT", 6379))
CACHE_TTL_SECONDS = 300
model =None
cache=None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global model,cache
    model=joblib.load(MODEL_PATH)
    cache = redis.Redis(host=REDIS_HOST, port=REDIS_PORT,decode_responses=True)

    yield
app= FastAPI(lifespan=lifespan)

class PredictRequest(BaseModel):
    text:str
class PredictResponse(BaseModel):
    label:str
@app.post("/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    start = time.perf_counter()
    cache_key = f"predict:{req.text}"

    cached_label = cache.get(cache_key)
    if cached_label is not None:
        elapsed_ms = (time.perf_counter() - start) * 1000
        print(f"CACHE HIT  key={cache_key!r} took={elapsed_ms:.2f}ms")
        return {"label": cached_label}

    label = model.predict([req.text])[0]
    cache.setex(cache_key, CACHE_TTL_SECONDS, label)
    elapsed_ms = (time.perf_counter() - start) * 1000
    print(f"CACHE MISS key={cache_key!r} took={elapsed_ms:.2f}ms")
    return {"label": label}
@app.get("/healthz")
def healthz():
    if model is None:
        return Response(status_code=503)
    return {"status": "ok", "version": "v2"}
