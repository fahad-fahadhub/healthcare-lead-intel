import asyncio
import requests
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
from database import insert_lead, init_db

async def run_google_maps_scraper(search_query):
    init_db()
    url = f"https://google.com{search_query.replace(' ', '+')}"
    new_leads = 0
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            executable_path="/usr/bin/chromium",
            args=["--no-sandbox", "--disable-setuid-sandbox", "--disable-blink-features=AutomationControlled"]
        )

        context = await browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        page = await context.new_page()
        
        try:
            await page.goto(url, timeout=60000)
            await page.wait_for_load_state("networkidle")
            
            # Continuous view pane scrolling emulation
            for _ in range(3):
                await page.evaluate("window.scrollBy(0, 1000);")
                await asyncio.sleep(2)
                
            html_source = await page.content()
            soup = BeautifulSoup(html_source, 'html.parser')
            places = soup.find_all('a', class_='hfpxzc') or soup.find_all('div', class_='Nv2y3c')
            
            for place in places:
                name = place.get('aria-label') or place.text.strip()
                link = place.get('href') or "https://google.com"
                if name:
                    if insert_lead(name, "Pending verification", "See source mapping link", link, 'Inorganic (Scraped)'):
                        new_leads += 1
        except Exception as e:
            print(f"Scraper runtime interrupt: {e}")
        finally:
            await browser.close()
    return new_leads

def run_us_npi_api_scraper(city, specialty):
    init_db()
    clean_city = city.replace(" ", "+")
    clean_specialty = specialty.replace(" ", "+")
    target_api_url = f"https://hhs.gov{clean_city}&taxonomy_description={clean_specialty}&limit=20"
    
    new_leads = 0
    try:
        response = requests.get(target_api_url, timeout=300)
        if response.status_code == 200:
            data = response.json()
            results = data.get("results", [])
            for item in results:
                basic = item.get("basic", {})
                first_name = basic.get("first_name", "")
                last_name = basic.get("last_name", "")
                organization_name = basic.get("organization_name", "")
                
                name = organization_name if organization_name else f"Dr. {first_name} {last_name}"
                
                addresses = item.get("addresses", [])
                primary_address = "US Registry Address"
                phone = "N/A"
                if addresses:
                    addr_data = addresses if isinstance(addresses, list) and len(addresses) > 0 else {}
                    primary_address = f"{addr_data.get('address_1', '')}, {addr_data.get('city', '')}"
                    phone = addr_data.get("telephone_number", "N/A")
                
                npi_number = item.get("number", "")
                source_link = f"https://hhs.gov{npi_number}"
                
                if name:
                    if insert_lead(name, phone, primary_address, source_link, 'Inorganic (Scraped)'):
                        new_leads += 1
    except Exception as e:
        print(f"NPI API failure: {e}")
    return new_leads
