import requests
from database import insert_lead, init_db

def run_india_maps_scraper(city, specialty):
    init_db()
    clean_query = f"{specialty}+{city}".replace(" ", "+")
    # Upgraded to use a direct spatial metadata index API that bypasses broken HTML selectors
    target_url = f"https://openstreetmap.org{clean_query}&format=json&addressdetails=1&limit=20"
    headers = {"User-Agent": "HealthcareLeadIntelApp/1.0 (fahadgomez1998@gmail.com)"}
    
    new_leads = 0
    try:
        response = requests.get(target_url, headers=headers, timeout=15)
        if response.status_code == 200:
            records = response.json()
            for item in records:
                display_name = item.get("display_name", "")
                name = display_name.split(",")[0]
                address = ", ".join(display_name.split(",")[1:4]).strip()
                lat = item.get("lat", "")
                lon = item.get("lon", "")
                source_link = f"https://google.com{lat},{lon}"
                
                if name:
                    if insert_lead(name, "Pending Ground Verification", address, source_link, 'Inorganic (Scraped)'):
                        new_leads += 1
    except Exception as e:
        print(f"Global Maps Index Engine Fault: {e}")
    return new_leads

def run_us_npi_api_scraper(city, specialty):
    init_db()
    clean_city = city.replace(" ", "+")
    clean_specialty = specialty.replace(" ", "+") + "*"
    target_api_url = f"https://hhs.gov{clean_city}&taxonomy_description={clean_specialty}&limit=20"
    
    new_leads = 0
    try:
        response = requests.get(target_api_url, timeout=15)
        if response.status_code == 200:
            data = response.json()
            results = data.get("results", [])
            for item in results:
                basic = item.get("basic", {})
                first_name = basic.get("first_name", "")
                last_name = basic.get("last_name", "")
                org_name = basic.get("organization_name", "")
                name = org_name if org_name else f"Dr. {first_name} {last_name}"
                
                addresses = item.get("addresses", [])
                primary_address = f"{city}, USA"
                phone = "Not Listed"
                if addresses and isinstance(addresses, list):
                    addr_data = addresses[0]
                    primary_address = f"{addr_data.get('address_1', '')}, {addr_data.get('city', '')}"
                    phone = addr_data.get("telephone_number", "Not Listed")
                
                npi_number = item.get("number", "")
                source_link = f"https://hhs.gov{npi_number}"
                
                if name:
                    if insert_lead(name, phone, primary_address, source_link, 'Inorganic (Scraped)'):
                        new_leads += 1
    except Exception as e:
        print(f"NPI Cloud Failure: {e}")
    return new_leads

