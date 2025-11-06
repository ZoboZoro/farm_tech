import os
from pathlib import Path

from dotenv import load_dotenv

# define project parent directory
BASE_DIR = Path(__file__).parent.parent.parent

# define working environment
ENV = os.getenv('ENV', default='dev')
env_path = f"{BASE_DIR}/{ENV}/.env"

load_dotenv(
    dotenv_path=env_path,
    verbose=True,
)

SQL_DIR = BASE_DIR / "src" / "sql"
SQL = SQL_DIR.mkdir(exist_ok=True)
SQL_FILE = BASE_DIR / "src" / "sql" / "query.sql"
LOG_DIR = BASE_DIR / "logs"

LOG = LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR/"ingestion.log"

HOST = os.getenv('DB_HOST', "db")
DBNAME = os.getenv('DB_NAME')
PORT = int(os.getenv('PORT', 5432))

with open('/run/secrets/postgres_pass', 'r') as password:
    PASS = password.read()

with open('/run/secrets/postgres_user', 'r') as user:
    USER = user.read()

with open('/run/secrets/api_secret', 'r') as api_key:
    KEY = api_key.read()
