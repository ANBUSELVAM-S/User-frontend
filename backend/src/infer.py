import io
import json
from typing import List, Tuple

import torch
import torch.nn.functional as F
from PIL import Image
from model import get_model  # model.py is in the same folder

def load_model(weights_path: str, classes_path: str, device: str = None):
    device = device or ("cuda" if torch.cuda.is_available() else "cpu")
    checkpoint = torch.load(weights_path, map_location=device)
    num_classes = checkpoint.get("num_classes")
    model, _ = get_model(num_classes)
    model.load_state_dict(checkpoint["model_state"], strict=True)
    model.to(device)
    model.eval()

    # Use the same transforms as training weights
    from model import get_weights
    preprocess = get_weights().transforms()

    with open(classes_path, "r", encoding="utf-8") as f:
        class_names = json.load(f)

    return model, preprocess, class_names, device

@torch.no_grad()
def predict_bytes(model, preprocess, class_names: List[str], image_bytes: bytes, device: str) -> Tuple[str, float]:
    from PIL import Image
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    x = preprocess(image).unsqueeze(0).to(device)
    logits = model(x)
    probs = F.softmax(logits, dim=1).squeeze(0)
    conf, idx = torch.max(probs, dim=0)
    label = class_names[idx.item()]
    return label, conf.item()
