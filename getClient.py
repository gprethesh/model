import redis

r = redis.StrictRedis(
    host="redis-13225.c1.asia-northeast1-1.gce.cloud.redislabs.com",
    port=13225,
    password="081zfCxu7ZI8NHW7cEHr8sPFyGToo7pR",
    decode_responses=True,
)


def update_wallet_extraction_status(job_id, file_hash, wallet, new_status):
    # Construct the hash key
    hash_key = f"{job_id}:{file_hash}"

    # Get the current extracted data
    current_extracted = r.hget(hash_key, "extracted")

    # Modify the extracted data for the specific wallet
    # Assuming the format is "wallet1:true, wallet2:true, wallet3:false" etc.
    wallets = current_extracted.split(", ")
    updated_extracted = []
    for w in wallets:
        w_info = w.split(":")
        if w_info[0] == wallet:
            updated_extracted.append(f"{wallet}:{new_status}")
        else:
            updated_extracted.append(w)

    # Update the extracted data in Redis
    r.hset(hash_key, "extracted", ", ".join(updated_extracted))


# Example usage
update_wallet_extraction_status("job12345", "file-hash3", "wallet9", "true")
