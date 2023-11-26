import redis
import json

# Connect to Redis
r = redis.StrictRedis(
    host="redis-13225.c1.asia-northeast1-1.gce.cloud.redislabs.com",
    port=13225,
    password="081zfCxu7ZI8NHW7cEHr8sPFyGToo7pR",
    decode_responses=True,
)


def update_job_data(job_id, file_hash, sub_key, sub_value):
    # Retrieve the JSON string for the specified file_hash
    json_data = r.hget(job_id, file_hash)
    if json_data:
        # Deserialize the JSON string into a Python dictionary
        data = json.loads(json_data)

        # Modify the specified sub_key value
        if sub_key in data:
            # Assuming the value is a comma-separated string, split it into a list
            values = data[sub_key].split(", ")
            # Modify the specific value
            values = [v if "wallet9" not in v else "wallet9:true" for v in values]
            # Join the list back into a string
            data[sub_key] = ", ".join(values)

            # Serialize the dictionary back to a JSON string
            updated_json_data = json.dumps(data)
            # Store the updated JSON string in Redis
            r.hset(job_id, file_hash, updated_json_data)
            return True
    return False


# Example usage: Update file-hash3 -> extracted -> wallet9 to true
update_success = update_job_data("job12345", "file-hash3", "extracted", "wallet9:true")
print(f"Update successful: {update_success}")
