import os
import pyodbc

# Database Configuration
DB_SERVER = r"localhost\SQLEXPRESS"
DB_NAME = "RetailPriceOptimizer"

# Detect installed SQL Server ODBC drivers
available_drivers = pyodbc.drivers()
DB_DRIVER = None
for driver in ["ODBC Driver 18 for SQL Server", "ODBC Driver 17 for SQL Server", "SQL Server"]:
    if driver in available_drivers:
        DB_DRIVER = driver
        break

if not DB_DRIVER:
    # Fallback to first available if none of our preferred matched
    DB_DRIVER = available_drivers[0] if available_drivers else "SQL Server"

# Build Connection Strings with standard safety parameters to handle server-side forced encryption
extra_params = ";Encrypt=no;TrustServerCertificate=yes"

MASTER_CONN_STR = f"Driver={{{DB_DRIVER}}};Server={DB_SERVER};Database=master;Trusted_Connection=yes{extra_params};"
CONN_STR = f"Driver={{{DB_DRIVER}}};Server={DB_SERVER};Database={DB_NAME};Trusted_Connection=yes{extra_params};"

# Directories Setup
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, "models")
EXPORTS_DIR = os.path.join(BASE_DIR, "exports")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
TEMP_DIR = os.path.join(BASE_DIR, "temp")

for d in [MODELS_DIR, EXPORTS_DIR, ASSETS_DIR, TEMP_DIR]:
    os.makedirs(d, exist_ok=True)
