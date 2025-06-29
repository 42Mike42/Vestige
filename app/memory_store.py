# memory_store.py
import json
import os
import datetime

DATA_PATH = "../data/memories.jsonl"



def load_memories():
    memories = []
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    mem = json.loads(line.strip())
                    # Recast timestamp if it's a string
                    if "timestamp" in mem and isinstance(mem["timestamp"], str):
                        mem["timestamp"] = datetime.datetime.fromisoformat(mem["timestamp"])
                    memories.append(mem)
                except:
                    continue
    return memories

def serialize_memory(memory):
    mem_copy = memory.copy()
    if isinstance(mem_copy.get("timestamp"), datetime.datetime):
        mem_copy["timestamp"] = mem_copy["timestamp"].isoformat()
    return mem_copy


def save_memory(memory):
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    with open(DATA_PATH, "a", encoding="utf-8") as f:
        json.dump(serialize_memory(memory), f)
        f.write("\n")
