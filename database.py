import sqlite3

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

def insert_lead(name, phone, address, source_url, lead_type='Inorganic (Scraped)'):
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
