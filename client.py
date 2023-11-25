import redis

# Connect to Redis
r = redis.StrictRedis(
    host="redis-13225.c1.asia-northeast1-1.gce.cloud.redislabs.com",
    port=13225,
    password="081zfCxu7ZI8NHW7cEHr8sPFyGToo7pR",
    decode_responses=True,
)


def create_job(job_id, file_hashes):
    for file_hash, data in file_hashes.items():
        hash_key = f"{job_id}:{file_hash}"

        # Store wallet, downloaded, extracted, gradient data
        for key, value in data.items():
            r.hset(hash_key, key, value)


def get_job_data(job_id, file_hashes):
    retrieved_data = {}
    for file_hash in file_hashes:
        # Construct the key for the job file hash
        job_file_key = f"job:{job_id}:{file_hash}"

        # Get the hash data
        hash_data = r.hgetall(job_file_key)

        # Decode the data (if needed) and add to the retrieved data
        # Remove the .decode("utf-8") as it's not needed with decode_responses=True
        decoded_data = {k: v for k, v in hash_data.items()}
        retrieved_data[file_hash] = decoded_data

    return retrieved_data


# Sample data
job_data = {
    "file-hash1": {
        "wallet": "wallet1, wallet2, wallet3",
        "downloaded": "wallet1:true:time:1000, wallet2:true:time:1000, wallet3:true:time:1000",
        "extracted": "wallet1:true, wallet2:true, wallet3:false",
        "gradient": "wallet1:4.65, wallet2:4.34, wallet3:4.78",
    },
    "file-hash2": {
        "wallet": "wallet4, wallet5, wallet6",
        "downloaded": "wallet4:true:time:1000, wallet5:true:time:1000, wallet6:true:time:1000",
        "extracted": "wallet4:true, wallet5:true, wallet6:false",
        "gradient": "wallet4:4.65, wallet5:4.34, wallet6:4.78",
    },
    "file-hash3": {
        "wallet": "wallet7, wallet8, wallet9",
        "downloaded": "wallet7:true:time:1000, wallet8:true:time:1000, wallet9:true:time:1000",
        "extracted": "wallet7:true, wallet8:true, wallet9:false",
        "gradient": "wallet7:4.65, wallet8:4.34, wallet9:4.78",
    },
}

# Create job
create_job("job12345", job_data)

# Retrieve and print job data
retrieved_data = get_job_data("job12345", job_data.keys())
print(retrieved_data)
