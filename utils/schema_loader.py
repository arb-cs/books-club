import json
from pathlib import Path


def load_schema(name: str):
    schema_dir = Path(__file__).parent.parent / "schemas"
    path = schema_dir / name
    with path.open() as f:
        return json.load(f)
