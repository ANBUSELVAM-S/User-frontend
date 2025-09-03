import json
import os
import random
import numpy as np
import torch

def set_seed(seed: int = 42):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)

def ensure_dir(path: str):
    os.makedirs(path, exist_ok=True)

def save_class_names(class_names, out_path: str):
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(class_names, f, indent=2)

def load_class_names(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def get_device():
    return "cuda" if torch.cuda.is_available() else "cpu"
