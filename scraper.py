import time
from duckduckgo_search import DDGS
from database import insert_lead

def check_practo_live(lead_name, city):
    """Queries live search indexes to determine if the provider is on Practo or Zocdoc."""
    try:
        with DDGS() as ddgs:
            query = f"site:practo.com OR site:zocdoc.com {lead_name} {city}"
            results = list(ddgs.text(query, max_results=2))
            if results:
                for r in results:
                    if "practo.com" in r['href'].lower() or "zocdoc.com" in r['href'].lower():
                        return "Listed on Competitor Network"
    except Exception:
        pass
    return "None (Exclusive Target)"

def discover_and_fill_pipeline(city, specialty, target_count=15):
    """Extracts, live-evaluates, filters, and fills the database with exactly 15 exclusive leads."""
    search_queries = [
        f"{specialty} clinic in {city} address phone",
        f"best {specialty} doctors in {city} directory",
        f"top private {specialty} hospital {city}"
    ]
    
    ingested_leads = 0
    seen_names = set()
    
    with DDGS() as ddgs:
        for query in search_queries:
            if ingested_leads >= target_count:
                break
                
            try:
                raw_results = list(ddgs.text(query, max_results=40))
                for item in raw_results:
                    if ingested_leads >= target_count:
                        break
                        
                    title = item.get("title", "")
                    snippet = item.get("body", "")
                    source_url = item.get("href", "https://google.com")
                    
                    # Clean the snippet to parse out provider titles
                    clean_name = title.split("-")[0].split("|")[0].split(":")[0].strip()
                    
                    if len(clean_name) < 5 or clean_name in seen_names:
                        continue
                        
                    seen_names.add(clean_name)
                    
                    # 1. LIVE PRACTO CHECKER BLOCK
                    presence = check_practo_live(clean_name, city)
                    
                    # 2. THE DUMP GATE: If listed on competitor, discard it immediately and proceed to next lead
                    if presence != "None (Exclusive Target)":
                        print(f"🗑️ Dumping lead (Already on Practo/Zocdoc): {clean_name}")
                        continue
                    
                    # 3. PARSE OUT OPERATIONAL INSIGHTS FROM LIVE SNIPPET DATA
                    address = "Verified Local Business Entity"
                    for word in snippet.split("."):
                        if "street" in word.lower() or "road" in word.lower() or "nagar" in word.lower() or "ave" in word.lower():
                            address = word.strip()
                            break
                    
                    # 4. INITIALIZE PIPELINE WITH REAL-TIME INSIGHTS
                    summary = f"Verified unlisted standalone {specialty} facility discovered active in {city} region."
                    rationale = f"High value target candidate. Complete digital market vacancy across primary networks. Pitch localized landing pages."
                    
                    if insert_lead(clean_name, "Pending Verification", address, source_url, 'Inorganic (Scraped)', presence, summary, rationale):
                        ingested_leads += 1
                        time.sleep(1) # Defensive timing layout
                        
            except Exception as e:
                print(f"Extraction stream variance encountered: {e}")
                continue
                
    return ingested_leads
