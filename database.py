omatically routes leads cleanly without breaking imports
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute('            INSERT INTO healthcare_leads (name, phone, address, source_url, lead_type)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, phone, address, source_url, lead_type))
        conn.commit()
        inserted = True
    except sqlite3.IntegrityError:
        inserted = False  
    conn.close()
    return inserted


