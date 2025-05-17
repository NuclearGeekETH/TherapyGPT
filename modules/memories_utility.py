import os
import json

DATA_FOLDER = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(DATA_FOLDER, "memories.json")

BLANK_DATA = {
    "memory": []
}

def load_memory():
    if not os.path.exists(DATA_PATH):
        with open(DATA_PATH, "w", encoding="utf-8") as f:
            json.dump(BLANK_DATA, f, indent=2, ensure_ascii=False)
        return BLANK_DATA
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)
    
def save_memory(data):
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    return "Patient memory saved!"

def get_patient_memory_text():
    data = load_memory()
    return json.dumps(data, indent=2, ensure_ascii=False)

def flatten_text_list(lst):
    return "\n".join(lst if lst else [])

def unflatten_text_list(val):
    return [line.strip() for line in val.splitlines() if line.strip()]

def flatten_table(lst, fields):
    return [[d.get(f, "") for f in fields] for d in lst]

def unflatten_table(rows, fields):
    import pandas as pd
    out = []
    # If rows is a pandas DataFrame, convert to a list of lists:
    if isinstance(rows, pd.DataFrame):
        rows = rows.values.tolist()
    for row in rows:
        if isinstance(row, (list, tuple)) and len(row) == len(fields) and any(str(x).strip() for x in row):
            out.append({f: row[i] for i, f in enumerate(fields)})
    return out

def flatten_memory(data):
    mem = data["memory"]
    return [
        mem.get("timestamp", ""),
        mem.get("summary", ""),
        mem.get("time_of_event", ""),
        mem.get("therapy_notes", ""),
    ]

def unflatten_memory(values, data):
    mem = data["memory"]
    mem["timestamp"] = values[0]
    mem["summary"] = values[1]
    mem["time_of_event"] = values[2]
    mem["therapy_notes"] = values[3]
    return data

def memory_load():
    data = load_memory()
    out = []
    out.append(flatten_table(data["memory"], ["timestamp","summary","time_of_event", "therapy_notes"]))
    out.append(data)
    return out

def memory_save(*args):
    idx = 0
    data = args[-1]  # Last arg is full dict
    data["memory"] = unflatten_table(args[idx], ["timestamp","summary","time_of_event", "therapy_notes"])
    save_memory(data)
    return "Memory saved!"

