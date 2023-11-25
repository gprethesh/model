# Main function to run the entire system

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
from load_data import load_data
from inode import vote_for_inode
from miner_connect import cleanup_after_training
from miner_connect import did_miner_extract
from miner_connect import remove_inactive_miner
from miner_connect import hash_and_update_database
from miner_connect import simulate_file_request
from miner_connect import miner_connect
from miner_connect import request_10mb_zip
from miner_connect import is_miner_eligible
from stakes import stake_tokens_and_nominate_validator
from validate_and_allocate_rewards import validate_and_allocate_rewards
from validate_and_allocate_rewards import is_model_approved_by_validators
from validate_and_allocate_rewards import allocate_rewards_to_miner_pools
from validate_and_allocate_rewards import validate_model
from train_and_contribute import train_and_contribute
from create_minor_pool import create_miner_pool
from train_model import train_model
from data import convert_to_10mb_zip


def run_system(main_folder, output_folder, csv_file_path):
    # Connect to the Redis server
    redis_client = redis.StrictRedis(
        host="redis-13225.c1.asia-northeast1-1.gce.cloud.redislabs.com",
        port=13225,
        password="081zfCxu7ZI8NHW7cEHr8sPFyGToo7pR",
        decode_responses=True,
    )

    with open(csv_file_path, "w", newline="") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["File Name", "Hash"])

        for folder_name in os.listdir(main_folder)[
            :10
        ]:  # Limit to a maximum of 10 folders
            folder_path = os.path.join(main_folder, folder_name)
            if os.path.isdir(folder_path):
                # Convert the folder into a 10MB zip file
                zip_file_path = convert_to_10mb_zip(folder_path, output_folder)

    class SimpleModel(nn.Module):
        def __init__(self):
            super(SimpleModel, self).__init__()
            self.fc = nn.Linear(10, 1)

        def forward(self, x):
            return self.fc(x)

    # Create a global model
    global_model = SimpleModel()

    # Specify the number of miners and comparisons
    num_miners = 10
    num_comparisons = 3

    # Create the miner pool and validate gradients
    create_miner_pool(redis_client, global_model, num_miners, num_comparisons)

    # Simulate validators voting for inodes
    validator_id = 1  # Replace with the actual validator ID
    inode_id = 1  # Replace with the actual inode ID
    voting_scale = 8  # Replace with the actual voting scale
    vote_for_inode(validator_id, inode_id, voting_scale)

    # Simulate delegates staking tokens to nominate a validator
    delegate_id = 1  # Replace with the actual delegate ID
    staked_tokens = 1000  # Replace with the actual number of staked tokens
    nominated_validator_id = 1  # Replace with the actual nominated validator ID
    stake_tokens_and_nominate_validator(
        delegate_id, nominated_validator_id, staked_tokens
    )


drive_folder = "Archive"
output_folder = "Upload_Zips"
csv_file_path = "hashed_files.csv"


# Run the entire system
run_system(drive_folder, output_folder, csv_file_path)
