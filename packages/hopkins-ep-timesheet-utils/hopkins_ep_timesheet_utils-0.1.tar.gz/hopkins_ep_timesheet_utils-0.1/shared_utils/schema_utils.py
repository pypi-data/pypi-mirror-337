import json
import os

def load_schema():
    schema_path = os.path.join(os.path.dirname(__file__), "..", "schema.json")
    with open(schema_path) as file:
        schema = json.load(file)
    return schema
