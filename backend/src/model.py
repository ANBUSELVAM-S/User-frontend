from typing import Tuple
import torch
from torch import nn
from torchvision import models

def get_weights():
    # Central place to get the pretrained weights & their recommended transforms
    return models.ResNet18_Weights.DEFAULT

def get_model(num_classes: int) -> Tuple[torch.nn.Module, object]:
    """
    Return a ResNet-18 CNN with the final layer sized to `num_classes`,
    plus the corresponding torchvision weights object (for transforms()).
    """
    weights = get_weights()
    model = models.resnet18(weights=weights)
    in_features = model.fc.in_features
    model.fc = nn.Linear(in_features, num_classes)
    return model, weights
