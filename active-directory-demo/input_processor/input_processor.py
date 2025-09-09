# input_processor.py
# Node 1 - validate / preprocess the input and pass forward.
from time import sleep
import os

PROCESSING_TIME = int(os.getenv("PROCESSING_TIME", 10))

def _normalize_input(item):
    keys = ['user', 'email', 'case', 'activity_description']
    normalized = {}
    for k in keys:
        if k not in item:
            print(f"missing required key: {k}")
            return None
        v = item[k]
        if isinstance(v, str):
            v = v.strip()
        normalized[k] = v
    print(f"Sanitizing input for user {normalized['user']}...")
    sleep(PROCESSING_TIME)
    print(f"Finished normalize for user: {normalized['user']}")
    return normalized

def start(args, hkube_api):
    items = []
    users = args["input"]

    for it in users:
        normalized = _normalize_input(it)
        if normalized is not None:
            # Mock processing placeholder
            items.append(normalized)

    print(f"Processed Data: {items}")
    return items


def stop():
    return None
