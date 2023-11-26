import redis
import json

# Connect to Redis
r = redis.StrictRedis(
    host="redis-13225.c1.asia-northeast1-1.gce.cloud.redislabs.com",
    port=13225,
    password="081zfCxu7ZI8NHW7cEHr8sPFyGToo7pR",
    decode_responses=True,
)


def create_job(job_id, file_hashes):
    for file_hash, data in file_hashes.items():
        # Serialize the data to a JSON string
        json_data = json.dumps(data)
        # Store the JSON string under the job_id hash with the file_hash as the field
        r.hset(job_id, file_hash, json_data)


def get_job_data(job_id, file_hashes):
    retrieved_data = {}
    for file_hash in file_hashes:
        # Get the JSON string stored in Redis
        json_data = r.hget(job_id, file_hash)
        # Deserialize the JSON string back to a Python dictionary
        if json_data:
            data = json.loads(json_data)
            retrieved_data[file_hash] = data
    return retrieved_data


# Sample data
job_data = {
    "file-hash1": {
        "wallet": "wallet1",
        "downloaded": True,
        "extracted": True,
        "gradient": 3.4,
        "location": "../gradients/job12345/",
    },
    "file-hash2": {
        "wallet": "wallet2",
        "downloaded": True,
        "extracted": False,
        "gradient": 7.4,
        "location": "../gradients/job12345/",
    },
    "file-hash3": {
        "wallet": "wallet3",
        "downloaded": False,
        "extracted": False,
        "gradient": None,
        "location": "",
    },
}

# Create job
create_job("job12345", job_data)

# Retrieve and print job data
retrieved_data = get_job_data("job12345", job_data.keys())
print(retrieved_data)
