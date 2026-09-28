import sqlite3
from duckduckgo_search import DDGS

def check_competitor_listings(lead_name):
    competitor_domains = ["practo.com", "zocdoc.com", "medibuddy.in", "lybrate.com"]
    matched = []
    
    with DDGS() as ddgs:
        for domain in competitor_domains:
            try:
                search_query = f"site:{domain} {lead_name}"
                query_generator = ddgs.text(search_query, max_results=1)
                if query_generator and len(list(query_generator)) > 0:
                    matched.append(domain.split('.')[0].capitalize())
            except Exception:
                continue
    return ", ".join(matched) if matched else "None (Exclusive Target)"

def run_enrichment_pipeline():
    conn = sqlite3.connect("leads_intelligence.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, lead_type FROM healthcare_leads WHERE competitor_presence IS NULL")
    rows = cursor.fetchall()
    
    for row in rows:
        lead_id, name, lead_type = row
        print(f"🧠 Running intelligence sequence for: {name}")
        
        competitors = check_competitor_listings(name)
        
        if lead_type == 'Organic (Inbound)':
            summary = "User initiated registration inquiry directly via organic mini-tool portal."
            rationale = "High conversion probability. Target reached out to evaluate platform capabilities."
        else:
            summary = "Inorganic provider profile discovered via open-source registry mining operations."
            if "None" in competitors:
                rationale = "High prioritization value. Complete digital visibility gap across key platforms."
            else:
                rationale = f"Tech-receptive provider listing discovered on competing ecosystem ({competitors}). Focus pitch on platform advantages and payout times."
                
        cursor.execute('''
            UPDATE healthcare_leads 
            SET competitor_presence = ?, ai_summary = ?, ai_rationale = ?
            WHERE id = ?
        ''', (competitors, summary, rationale, lead_id))
        conn.commit()
    conn.close()
