import json
import os
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
from pathlib import Path
import sys

# ---------------- Path Setup ----------------
APP_DIR = Path(__file__).parent.resolve()
ROOT_DIR = APP_DIR.parent.resolve()

# Add src folder to sys.path
sys.path.append(str(ROOT_DIR / "src"))

# Lazy imports for torch
from typing import Optional
_model = None
_preprocess = None
_class_names = None
_device = None

WEIGHTS_PATH = ROOT_DIR / "weights" / "best.pt"
CLASSES_PATH = ROOT_DIR / "weights" / "classes.json"
PROCEDURES_PATH = APP_DIR / "procedures.json"

# Correct imports from src
from infer import load_model, predict_bytes

# ---------------- FastAPI ----------------
app = FastAPI(title="Image Type Classifier", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static UI
app.mount("/static", StaticFiles(directory=APP_DIR / "static"), name="static")


def _load_model():
    global _model, _preprocess, _class_names, _device
    if _model is None:
        if not WEIGHTS_PATH.exists() or not CLASSES_PATH.exists():
            raise RuntimeError("Model weights/classes not found. Train the model first.")
        _model, _preprocess, _class_names, _device = load_model(
            str(WEIGHTS_PATH), str(CLASSES_PATH)
        )


@app.get("/", response_class=HTMLResponse)
def index():
    # Serve the index.html
    html_path = APP_DIR / "static" / "index.html"
    return HTMLResponse(html_path.read_text(encoding="utf-8"))


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        _load_model()
        if not file.content_type or "image" not in file.content_type:
            raise HTTPException(status_code=400, detail="Please upload an image file.")
        image_bytes = await file.read()

        label, confidence = predict_bytes(
            _model, _preprocess, _class_names, image_bytes, _device
        )

        procedures = json.loads(PROCEDURES_PATH.read_text(encoding="utf-8"))
        steps = procedures.get(label, [])

        return JSONResponse(
            {
                "label": label,
                "confidence": round(float(confidence), 4),
                "steps": steps,
            }
        )
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")
