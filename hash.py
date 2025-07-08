import hashlib
import json

data = {
    "Ico": "46456554",
    "apiKey": "FE7E536DECF447F3BA8EAAD7D3342838"
}

# Převeďte slovník na JSON řetězec
json_data = json.dumps(data, sort_keys=True)

# Vypočítejte SHA-256 hash
hash_object = hashlib.sha256(json_data.encode())
hash_hex = hash_object.hexdigest()

print(hash_hex)