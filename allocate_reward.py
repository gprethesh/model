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

def allocate_rewards(redis_client, num_miners, num_comparisons):
    miner_pools_scores = {}

    # Iterate over miner pools
    for miner_id in range(num_miners):
        total_score = 0

        # Accumulate scores from comparisons
        for comparison in range(1, num_comparisons + 1):
            score_key = f"score_{comparison}"
            score_str = redis_client.hget(f"miners:{miner_id}", score_key)

            if score_str is not None:
                total_score += float(score_str)

        # Assign total_score to the miner pool
        miner_pools_scores[f"Miner Pool {miner_id}"] = total_score

    # Sort and print scores
    sorted_scores = sorted(miner_pools_scores.items(), key=lambda x: x[1], reverse=True)
    print("Miner Pool Scores:")
    for pool, score in sorted_scores:
        print(f"{pool}: {score}")
    import matplotlib.pyplot as plt

    def plot_miner_pool_scores(miner_pools_scores):
        pools, scores = zip(*miner_pools_scores.items())

        plt.figure(figsize=(10, 6))
        plt.bar(pools, scores, color='blue')
        plt.xlabel('Miner Pools')
        plt.ylabel('Total Score')
        plt.title('Miner Pool Scores')
        plt.show()

    # Call this function after allocating rewards
    plot_miner_pool_scores(miner_pools_scores)

    # Allocate rewards based on scores (you can customize this part)
    # For example, you might allocate a percentage of rewards to the top-performing miner pools

# Simulate allocating rewards to miner pools
r = redis.Redis(
host='redis-13225.c1.asia-northeast1-1.gce.cloud.redislabs.com',
port=13225,
password='081zfCxu7ZI8NHW7cEHr8sPFyGToo7pR')

# Connect to the Redis server
redis_client = redis.StrictRedis(
    host='redis-13225.c1.asia-northeast1-1.gce.cloud.redislabs.com',
    port=13225,
    password='081zfCxu7ZI8NHW7cEHr8sPFyGToo7pR',
    decode_responses=True
)
num_miners = 10
num_comparisons = 3
allocate_rewards(redis_client, num_miners, num_comparisons)