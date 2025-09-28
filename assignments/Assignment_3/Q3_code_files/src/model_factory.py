import torch
import torch.nn as nn
from torchvision import models
import json

class ModelFactory:
    def __init__(self, config_path="./config/data_config.json"):
        with open(config_path, "r") as f:
            self.config = json.load(f)
    
    def get_model(self, model_name=None, num_classes=10):
        if model_name is None:
            model_name = self.config["model_architecture"]["selected_model"]
        
        if model_name == "resnet34":
            model = models.resnet34(weights=models.ResNet34_Weights.IMAGENET1K_V1)
        elif model_name == "resnet50":
            model = models.resnet50(weights=models.ResNet50_Weights.IMAGENET1K_V2)
        elif model_name == "resnet101":
            model = models.resnet101(weights=models.ResNet101_Weights.IMAGENET1K_V2)
        elif model_name == "resnet152":
            model = models.resnet152(weights=models.ResNet152_Weights.IMAGENET1K_V2)
        
        num_features = model.fc.in_features
        model.fc = nn.Linear(num_features, num_classes)
        
        return model