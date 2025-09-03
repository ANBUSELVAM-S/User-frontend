import argparse
import os
from time import time

import torch
from torch import nn
from torch.optim import AdamW
from torch.optim.lr_scheduler import OneCycleLR
from torch.utils.tensorboard import SummaryWriter

from model import get_model, get_weights
from dataset import build_dataloaders
from utils import set_seed, ensure_dir, save_class_names, get_device

def accuracy(logits, labels):
    preds = torch.argmax(logits, dim=1)
    return (preds == labels).float().mean().item()

def train_one_epoch(model, train_loader, criterion, optimizer, device, step_fn=None):
    model.train()
    running_loss = 0.0
    running_acc = 0.0
    for step, (x, y) in enumerate(train_loader, 1):
        x, y = x.to(device), y.to(device)
        optimizer.zero_grad()
        logits = model(x)
        loss = criterion(logits, y)
        loss.backward()
        optimizer.step()
        running_loss += loss.item()
        running_acc += accuracy(logits, y)
        if step_fn:
            step_fn()
    n = len(train_loader) if len(train_loader) > 0 else 1
    return running_loss / n, running_acc / n

@torch.no_grad()
def evaluate(model, val_loader, criterion, device):
    model.eval()
    running_loss = 0.0
    running_acc = 0.0
    for x, y in val_loader:
        x, y = x.to(device), y.to(device)
        logits = model(x)
        loss = criterion(logits, y)
        running_loss += loss.item()
        running_acc += accuracy(logits, y)
    n = len(val_loader) if len(val_loader) > 0 else 1
    return running_loss / n, running_acc / n

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_dir", type=str, default="data")
    parser.add_argument("--epochs", type=int, default=10)
    parser.add_argument("--batch_size", type=int, default=32)
    parser.add_argument("--lr", type=float, default=3e-4)
    parser.add_argument("--img_size", type=int, default=224)
    parser.add_argument("--out_dir", type=str, default="weights")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    set_seed(args.seed)
    ensure_dir(args.out_dir)

    device = get_device()
    print(f"Using device: {device}")

    # Use the weights' recommended transforms for dataloaders
    weights = get_weights()
    train_loader, val_loader, class_names = build_dataloaders(
        args.data_dir, img_size=args.img_size, batch_size=args.batch_size, weights=weights
    )

    # Build model with the correct number of classes
    num_classes = len(class_names)
    model, _ = get_model(num_classes=num_classes)
    model.to(device)

    criterion = nn.CrossEntropyLoss()
    optimizer = AdamW(model.parameters(), lr=args.lr)
    total_steps = args.epochs * max(len(train_loader), 1)
    scheduler = OneCycleLR(optimizer, max_lr=args.lr, total_steps=total_steps) if total_steps > 0 else None

    writer = SummaryWriter(log_dir=os.path.join(args.out_dir, "runs"))
    best_val_acc = 0.0
    best_path = os.path.join(args.out_dir, "best.pt")
    class_path = os.path.join(args.out_dir, "classes.json")
    save_class_names(class_names, class_path)

    global_step = 0
    t0 = time()
    for epoch in range(1, args.epochs + 1):
        def step_fn():
            nonlocal global_step
            global_step += 1
            if scheduler is not None:
                scheduler.step()

        train_loss, train_acc = train_one_epoch(model, train_loader, criterion, optimizer, device, step_fn=step_fn)
        val_loss, val_acc = evaluate(model, val_loader, criterion, device)

        writer.add_scalar("loss/train", train_loss, epoch)
        writer.add_scalar("loss/val", val_loss, epoch)
        writer.add_scalar("acc/train", train_acc, epoch)
        writer.add_scalar("acc/val", val_acc, epoch)

        print(f"Epoch {epoch:03d} | train_loss {train_loss:.4f} acc {train_acc:.4f} | val_loss {val_loss:.4f} acc {val_acc:.4f}")

        if val_acc > best_val_acc:
            best_val_acc = val_acc
            torch.save({"model_state": model.state_dict(), "num_classes": num_classes}, best_path)
            print(f"  ↳ Saved new best to {best_path} (val_acc={best_val_acc:.4f})")

    dt = time() - t0
    print(f"Done. Best val_acc={best_val_acc:.4f}. Time: {dt/60:.1f} min. Checkpoints in {args.out_dir}")

if __name__ == "__main__":
    main()
