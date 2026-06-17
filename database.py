import os
import pyodbc
import config

def get_master_connection():
    return pyodbc.connect(config.MASTER_CONN_STR, autocommit=True)

def get_connection():
    return pyodbc.connect(config.CONN_STR)

def initialize_database():
    """Checks if the database exists; creates it and initializes tables."""
    # 1. Create database if not exists
    m_conn = get_master_connection()
    cursor = m_conn.cursor()
    cursor.execute("SELECT name FROM sys.databases")
    databases = [row[0] for row in cursor.fetchall()]
    
    if config.DB_NAME not in databases:
        print(f"Database {config.DB_NAME} not found. Creating...")
        cursor.execute(f"CREATE DATABASE {config.DB_NAME}")
        print("Database created successfully.")
    m_conn.close()
    
    # 2. Run setup.sql script
    conn = get_connection()
    cursor = conn.cursor()
    sql_path = os.path.join(config.BASE_DIR, "setup.sql")
    if os.path.exists(sql_path):
        with open(sql_path, "r", encoding="utf-8") as f:
            sql_script = f.read()
        try:
            cursor.execute(sql_script)
            conn.commit()
            print("Database tables initialized successfully.")
        except Exception as e:
            conn.rollback()
            print(f"Error executing setup script: {e}")
            raise
    else:
        print("Warning: setup.sql script not found!")
    conn.close()

def execute_query(query, params=None, commit=True, fetch=False):
    """Safely executes a query with parameters using a new connection."""
    conn = get_connection()
    cursor = conn.cursor()
    result = None
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
            
        if fetch:
            result = cursor.fetchall()
            
        if commit:
            conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Database Query Error: {e}")
        raise
    finally:
        conn.close()
    return result

def clear_existing_data():
    """Purges all records from Products and Predictions tables."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Disable foreign key check or delete in order of references
        cursor.execute("DELETE FROM Predictions")
        cursor.execute("DELETE FROM Products")
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        print(f"Error purging database records: {e}")
        return False
    finally:
        conn.close()
