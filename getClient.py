import redis
import json

# Connect to Redis
r = redis.StrictRedis(
    host="redis-13225.c1.asia-northeast1-1.gce.cloud.redislabs.com",
    port=13225,
    password="081zfCxu7ZI8NHW7cEHr8sPFyGToo7pR",
    decode_responses=True,
)


def update_job_data(job_id, file_hash, field, new_value):
    # Get the JSON string stored in Redis for the specific file_hash
    json_data = r.hget(job_id, file_hash)
    if json_data:
        # Deserialize the JSON string to a Python dictionary
        data = json.loads(json_data)
        # Update the specified field with the new value
        data[field] = new_value
        # Serialize the updated data back to a JSON string
        updated_json_data = json.dumps(data)
        # Store the updated JSON string in Redis
        r.hset(job_id, file_hash, updated_json_data)
    else:
        print(f"No data found for file hash: {file_hash}")


# Update the 'extracted' field of 'file-hash3' in 'job12345' to True
update_success = update_job_data("job12345", "file-hash3", "extracted", True)

print(f"Update successful: {update_success}")
