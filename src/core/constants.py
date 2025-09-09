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