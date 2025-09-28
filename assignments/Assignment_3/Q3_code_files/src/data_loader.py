import torch
from torchvision import datasets, transforms
from torch.utils.data import DataLoader, Subset
import json

class MNISTDataLoader:
    def __init__(self, config_path="./config/data_config.json"):
        with open(config_path, "r") as f:
            self.config = json.load(f)
        
        self.transform = transforms.Compose([
            transforms.Resize(self.config["data_source"]["image_size"]),
            transforms.Grayscale(3),
            transforms.ToTensor(),
            transforms.Normalize((0.1307, 0.1307, 0.1307), (0.3081, 0.3081, 0.3081))
        ])
    
    def get_dataloaders(self):
        train_dataset = datasets.MNIST(
            root=self.config["data_source"]["path"],
            train=True,
            download=True,
            transform=self.transform
        )
        
        test_dataset = datasets.MNIST(
            root=self.config["data_source"]["path"],
            train=False,
            download=True,
            transform=self.transform
        )
        
        # Use subset for faster training
        train_size = self.config["data_source"]["train_subset"]
        test_size = self.config["data_source"]["test_subset"]
        
        train_indices = torch.randperm(len(train_dataset))[:train_size]
        test_indices = torch.randperm(len(test_dataset))[:test_size]
        
        train_subset = Subset(train_dataset, train_indices)
        test_subset = Subset(test_dataset, test_indices)
        
        train_loader = DataLoader(
            train_subset,
            batch_size=self.config["data_source"]["batch_size"],
            shuffle=True
        )
        
        test_loader = DataLoader(
            test_subset,
            batch_size=self.config["data_source"]["batch_size"],
            shuffle=False
        )
        
        return train_loader, test_loader