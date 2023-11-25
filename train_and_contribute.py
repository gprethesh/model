import torch
import torch.nn as nn
import torch.optim as optim
import redis
import json
from load_data import load_data
from train_model import train_model
class SimpleModel(nn.Module):
    def __init__(self):
        super(SimpleModel, self).__init__()
        self.fc = nn.Linear(10, 1)

    def forward(self, x):
        return self.fc(x)
def train_and_contribute(miner_id, global_model, zip_file_path, redis_client):
    # Simulate loading data from the processed zip file
    data_loader = load_data(zip_file_path)

    # Initialize the model
    model = SimpleModel()

    # Train the model
    train_model(model, data_loader)

    # Check if gradients are not None
    if any(param.grad is None for param in model.parameters()):
        print(f"Miner {miner_id} failed to compute gradients.")
        return

    # Get model gradients
    gradients = [param.grad.data.numpy().tolist() for param in model.parameters()]

    # Update the pool's Redis database with the model's gradients
    redis_client.hset(f"miners:{miner_id}", "model_gradients", json.dumps(gradients))
    print(f"Miner {miner_id} contributed model gradients.")