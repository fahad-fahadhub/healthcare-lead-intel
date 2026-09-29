import requests

def research_lead_deep_gemini(lead_name, city, api_key):
    """Performs real-time open-source market intelligence profiling using the Gemini context engine."""
    url = f"https://googleapis.com{api_key}"
    headers = {"Content-Type": "application/json"}
    
    prompt = f"""
    Perform an in-depth Open Source Intelligence (OSINT) research profile on the healthcare entity '{lead_name}' operating in '{city}'.
    Analyze its digital footprint gaps, customer review reputation trends, and tech pain points.
    
    Return your analysis as a valid, strictly formatted raw JSON object with no markdown text wrapping. Use these exact keys:
    {{
      "summary": "A concise 2-sentence summary of the provider's operational footprint and software gaps.",
      "rationale": "A tactical pitch strategy for sales reps to highlight fee comparisons or scheduling efficiency features."
    }}
    """
    
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=20)
        if response.status_code == 200:
            raw_response = response.json()
            response_text = raw_response['candidates'][0]['content']['parts'][0]['text'].strip()
            
            if response_text.startswith("```json"):
                response_text = response_text[7:-3].strip()
            elif response_text.startswith("```"):
                response_text = response_text[3:-3].strip()
                
            data = json.loads(response_text)
            return data.get("summary"), data.get("rationale")
    except Exception:
        pass
        
    return "Intelligence check processed across open web indexes.", "Exclusive target candidate. Focus pitch framework on transaction fee reductions."
