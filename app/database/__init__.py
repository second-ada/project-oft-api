from lever import Database
from pathlib import Path


DB_DIR = Path(__file__).parent.resolve() / 'database.db'
db = Database(DB_DIR)
