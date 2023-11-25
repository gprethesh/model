
import zipfile
import hashlib
import csv
import os
import zipfile
import hashlib
import csv
import os
import redis
import json
import shutil
import time
import torch
import torch.nn as nn
import torch.optim as optim
import shutil
from train_and_contribute import train_and_contribute

from validate_and_allocate_rewards import validate_and_allocate_rewards
def compare_gradients(previous_gradients, current_gradients):
    # Your comparison logic here
    # For example, calculate the absolute difference for each element
    abs_differences = [abs(prev - curr) for prev, curr in zip(previous_gradients[1], current_gradients[1])]

    # Sum the absolute differences
    return sum(abs_differences)


def create_miner_pool(redis_client, global_model, num_miners, num_comparisons=3):
    for miner_id in range(num_miners):
        # Assume each miner requests a 10MB zip file (replace this logic with your actual logic)
        zip_file_path = f'/Uploaded_Zips{miner_id}.zip'

        # Simulate miner training and contributing gradients
        train_and_contribute(miner_id, global_model, zip_file_path, redis_client)

        # Compare gradients with previous miners and set a score
        if miner_id > 0:
            for comparison in range(min(num_comparisons, miner_id)):
                previous_miner_id = miner_id - (comparison + 1)
                previous_gradients_str = redis_client.hget(f"miners:{previous_miner_id}", "model_gradients")
                current_gradients_str = redis_client.hget(f"miners:{miner_id}", "model_gradients")

                # Check if gradients are not None
                if previous_gradients_str is not None and current_gradients_str is not None:
                    previous_gradients = json.loads(previous_gradients_str)
                    current_gradients = json.loads(current_gradients_str)
                    score = compare_gradients(previous_gradients, current_gradients)
                    redis_client.hset(f"miners:{miner_id}", f"score_{comparison + 1}", score)
                    print(f"Miner {miner_id} scored {score} in comparison {comparison + 1}")
                else:
                    print(f"Miner {miner_id} or its previous miner failed to compute gradients.")
    # After training, send the global model to validators for validation
    validator_id = 1  # Replace with the actual validator ID
    test_data = load_test_data()  # Replace with actual test data
    validate_and_allocate_rewards(validator_id, global_model, test_data)

# Load test data for model validation
def load_test_data():
    # Simulate loading test data for model validation
    # Replace with actual test data loading logic
    return torch.randn(100, 10), torch.randint(0, 2, (100, 1))