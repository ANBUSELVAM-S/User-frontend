# ML Image Type Classifier

Classify images as **carpenter**, **restroom**, **electrical**, **vending_machine**, or **plumbing** using a fine-tuned ResNet-18.
Includes:
- PyTorch training pipeline
- FastAPI inference server
- Minimal HTML front-end
- Safety-first, high-level "step-by-step" guidance shown with predictions

## Project Structure
```
ml-image-type-classifier/
├── README.md
├── requirements.txt
├── .gitignore
├── data/
│   ├── train/
│   │   ├── carpenter/ ... images
│   │   ├── restroom/  ... images
│   │   ├── electrical/...
│   │   ├── vending_machine/...
│   │   └── plumbing/  ...
│   └── val/
│       └── (same subfolders as train)
├── weights/
│   └── best.pt                 (saved after training)
├── src/
│   ├── dataset.py
│   ├── model.py
│   ├── train.py
│   ├── infer.py
│   ├── utils.py
│   └── procedures.json
├── app/
│   ├── main.py                 (FastAPI app)
│   ├── procedures.json         (copied for app use)
│   └── static/
│       ├── index.html
│       ├── script.js
│       └── style.css
└── docker/
    └── Dockerfile
```

## Quickstart

> Python 3.9+ recommended

1. **Create & activate a virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Organize your dataset** into `data/train/<class>/` and `data/val/<class>/`.
   Classes (folders) must be: `carpenter, restroom, electrical, vending_machine, plumbing`

4. **Train the model**
   ```bash
   python src/train.py --data_dir data --epochs 10 --batch_size 32 --lr 3e-4
   ```
   The best checkpoint will be saved to `weights/best.pt` and class names to `weights/classes.json`.

5. **Run the API & Web UI**
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```
   Open http://127.0.0.1:8000 in your browser, upload an image, and see the prediction & high-level steps.

## Notes
- The included "steps" are **general, high-level** checklists — not a substitute for a licensed professional, especially for **electrical** and **plumbing** work. Always follow local codes and safety standards.
- You can edit `src/procedures.json` to change the steps shown for each class.
- For better accuracy, collect at least 200–500 images per class and keep validation data separate.

## Export / Docker (optional)
- Export to TorchScript/ONNX (extend `src/infer.py` as needed).
- Build a Docker image:
  ```bash
  docker build -t image-type-classifier -f docker/Dockerfile .
  docker run -it --rm -p 8000:8000 image-type-classifier
  ```

Good luck!
