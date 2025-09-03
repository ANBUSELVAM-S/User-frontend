from typing import Tuple
import os
from torchvision import datasets, transforms

def build_dataloaders(
    data_dir: str,
    img_size: int = 224,
    batch_size: int = 32,
    weights=None,
    num_workers: int = 2
) -> Tuple[object, object, list]:
    train_dir = os.path.join(data_dir, "train")
    val_dir = os.path.join(data_dir, "val")

    if weights is not None:
        preprocess = weights.transforms()
        train_tfms = preprocess
        val_tfms = preprocess
    else:
        train_tfms = transforms.Compose([
            transforms.Resize((img_size, img_size)),
            transforms.RandomHorizontalFlip(),
            transforms.ToTensor()
        ])
        val_tfms = transforms.Compose([
            transforms.Resize((img_size, img_size)),
            transforms.ToTensor()
        ])

    train_ds = datasets.ImageFolder(train_dir, transform=train_tfms)
    val_ds = datasets.ImageFolder(val_dir, transform=val_tfms)
    class_names = train_ds.classes

    from torch.utils.data import DataLoader
    train_loader = DataLoader(train_ds, batch_size=batch_size, shuffle=True, num_workers=num_workers, pin_memory=True)
    val_loader = DataLoader(val_ds, batch_size=batch_size, shuffle=False, num_workers=num_workers, pin_memory=True)

    return train_loader, val_loader, class_names
