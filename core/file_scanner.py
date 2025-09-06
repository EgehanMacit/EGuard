import os
import hashlib

# Simple example of a malware signature database
KNOWN_HASHES = {
    "44d88612fea8a8f36de82e1278abb02f",  # eicar test
}

def calculate_md5(file_path):
    try:
        with open(file_path, "rb") as f:
            return hashlib.md5(f.read()).hexdigest()
    except Exception as e:
        return None

def scan_file(file_path):
    file_hash = calculate_md5(file_path)
    if file_hash is None:
        return (file_path, "Access Error")

    if file_hash in KNOWN_HASHES:
        return (file_path, "Threat Detected")
    else:
        return (file_path, "Clean")

def scan_directory(directory_path):
    results = []
    for root, dirs, files in os.walk(directory_path):
        for f in files:
            full_path = os.path.join(root, f)
            result = scan_file(full_path)
            results.append(result)
    return results
