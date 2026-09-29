import sqlite3
from duckduckgo_search import DDGS

def check_competitor_listings(lead_name):
    competitor_domains = ["practo.com", "zocdoc.com", "medibuddy.in"]
    matched = []
    try:
        with DDGS() as ddgs:
            for domain in competitor_domains:
                try:
                    search_query = f"site:{domain} {lead_name}"
                    results = list(ddgs.text(search_query, max_results=1))
                    if results:
                        matched.append(domain.split('.')[0].capitalize())
                except Exception:
                    continue
    except Exception:
        pass
    return ", ".join(matched) if matched else "None (Exclusive Target)"

def run_enrichment_pipeline():
    conn = sqlite3.connect("leads_intelligence.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, lead_type FROM healthcare_leads WHERE competitor_presence IS NULL")
    rows = cursor.fetchall()
    
    for row in rows:
        lead_id, name, lead_type = row
        competitors = check_competitor_listings(name)
        
        if lead_type == 'Organic (Inbound)':
            summary = "User initiated registration inquiry directly via organic portal."
            rationale = "High conversion probability. Target reached out to evaluate system capabilities."
        else:
            summary = f"Inorganic discovery. Checked cross-listings across digital networks."
            if "None" in competitors:
                rationale = "High priority asset. Complete visibility vacancy across key vertical applications."
            else:
                rationale = f"Provider profile actively listed on competing ecosystem ({competitors}). Highlight transaction time differences."
                
        cursor.execute('''
            UPDATE healthcare_leads 
            SET competitor_presence = ?, ai_summary = ?, ai_rationale = ?
            WHERE id = ?
        ''', (competitors, summary, rationale, lead_id))
        conn.commit()
    conn.close()
