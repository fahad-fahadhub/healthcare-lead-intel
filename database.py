import sqlite3
import os
import pandas as pd

DB_NAME = "leads_intelligence.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS healthcare_leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            phone TEXT,
            address TEXT,
            source_url TEXT,
            lead_type TEXT DEFAULT 'Inorganic (Scraped)',
            competitor_presence TEXT,
            ai_summary TEXT,
            ai_rationale TEXT,
            verification_status TEXT DEFAULT 'Pending Field Visit',
            field_executive_name TEXT,
            root_cause_analysis TEXT,
            inside_intelligence TEXT
        )
    ''')
    conn.commit()
    conn.close()
    
    # Generate mock CRM lookup data file if it is missing
    if not os.path.exists("mock_crm.csv"):
        df = pd.DataFrame(columns=["Entity Name", "Phone/Contact"])
        df.to_csv("mock_crm.csv", index=False)

def is_already_in_crm(entity_name):
    try:
        crm_df = pd.read_csv("mock_crm.csv")
        return entity_name.lower().strip() in crm_df['Entity Name'].str.lower().str.strip().values
    except Exception:
        return False

def insert_lead(name, phone, address, source_url, lead_type='Inorganic (Scraped)'):
    # This core logic automatically routes leads cleanly without breaking imports
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO healthcare_leads (name, phone, address, source_url, lead_type)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, phone, address, source_url, lead_type))
        conn.commit()
        inserted = True
    except sqlite3.IntegrityError:
        inserted = False  
    conn.close()
    return inserted

