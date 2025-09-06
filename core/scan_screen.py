from utils.virustotal_api import check_hash_with_virustotal
import json

def check_virus_total(self, file_hash):
    with open("config.json") as f:
        config = json.load(f)

    api_key = config.get("vt_api_key")
    if not api_key:
        print("API key not found. Please enter it in the settings.")
        return

    result = check_hash_with_virustotal(api_key, file_hash)
    if "error" in result:
        print("Error:", result["error"])
    else:
        print("VT Result:", result)
