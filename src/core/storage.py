import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

CUSTOMERS_FILE = DATA_DIR / "customers.json"
TICKETS_FILE = DATA_DIR / "tickets.json"
TECHS_FILE = DATA_DIR / "technicians.json"

# File map for the json data
FILE_MAP = {
    'customers': CUSTOMERS_FILE,
    'tickets': TICKETS_FILE,
    'technicians': TECHS_FILE
}

COUNTER_FILE = DATA_DIR / "maxticket.txt"

def initialize_files():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    for data_type in FILE_MAP:
        if not FILE_MAP[data_type].exists():
            save_json(FILE_MAP[data_type], [])
    if not COUNTER_FILE.exists():
        with COUNTER_FILE.open("w", encoding="utf-8") as f:
            f.write("0")


def load_json(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)

def save_json(path: Path, data: list[dict]) -> None:
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def load_data(data_type: str) -> list[dict]:
    return load_json(FILE_MAP[data_type])

def save_data(data_type: str, data: list[dict]) -> None:
    save_json(FILE_MAP[data_type], data)

def get_next_ticket_number():
    with open(COUNTER_FILE, 'r') as f:
        current_max = int(f.read().strip())
        
    next_number = current_max + 1
    
    with open(COUNTER_FILE, 'w') as f:
        f.write(str(next_number))
    
    return next_number