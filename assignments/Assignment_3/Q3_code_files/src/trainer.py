import torch
import torch.nn as nn

class Trainer:
    def __init__(self, model, device="cpu"):
        self.model = model
        self.device = torch.device(device)
        self.model.to(self.device)
    
    def train(self, train_loader, optimizer, criterion, epochs=2):
        self.model.train()
        
        for epoch in range(epochs):
            for batch_idx, (data, target) in enumerate(train_loader):
                data, target = data.to(self.device), target.to(self.device)
                
                optimizer.zero_grad()
                output = self.model(data)
                loss = criterion(output, target)
                loss.backward()
                optimizer.step()
    
    def evaluate(self, test_loader, criterion):
        self.model.eval()
        correct = 0
        total = 0
        
        with torch.no_grad():
            for data, target in test_loader:
                data, target = data.to(self.device), target.to(self.device)
                output = self.model(data)
                
                _, predicted = output.max(1)
                total += target.size(0)
                correct += predicted.eq(target).sum().item()
        
        accuracy = 100. * correct / total
        return accuracy