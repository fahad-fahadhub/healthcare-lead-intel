import streamlit as st
import sqlite3
import pandas as pd
import asyncio
from database import init_db, insert_lead
import scraper
import ai_engine

st.set_page_config(layout="wide", page_title="Healthcare Lead Intelligence Portal")
init_db()

st.title("🩺 Healthcare Lead Intelligence System (HLIS)")

# --- INTEGRATED INBOUND ORGANIC HOOK MODAL ---
with st.expander("🌱 Organic Inbound Simulation Node (Public Website Widget Block)"):
    st.markdown("### Test Inbound Lead Capture Flow")
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        inbound_name = st.text_input("Practitioner / Facility Legal Name:")
    with col_b:
        inbound_phone = st.text_input("Primary Callback Contact Number:")
    with col_c:
        inbound_address = st.text_input("Operating Clinic Postal Address:")
    if st.button("Submit Inbound Optimization Request"):
        if inbound_name:
            success = insert_lead(inbound_name, inbound_phone, inbound_address, "Organic Platform Intake Form", "Organic (Inbound)")
            if success:
                st.success("Lead ingested into the processing workflow queue!")
            else:
                st.warning("Provider entry already mapped within system directory tables.")

# --- COMPUTATION OPERATION CONTROLS ---
st.sidebar.header("🕹️ System Operations")
market_selection = st.sidebar.selectbox("Target Market Pipeline", ["India (Google Maps Scraper)", "United States (NPPES Federal Registry API)"])

if market_selection == "India (Google Maps Scraper)":
    query_target = st.sidebar.text_input("Location Matrix & Specialty Keyword:", "Cardiologists Indiranagar Bangalore")
    if st.sidebar.button("Launch Playwright Extractor Engine"):
        with st.spinner("Automating Chromium Instance..."):
            count = asyncio.run(scraper.run_google_maps_scraper(query_target))
            st.sidebar.success(f"Processing Complete! Discovered {count} unlisted target entries.")
else:
    us_city = st.sidebar.text_input("Target US City:", "Houston")
    us_spec = st.sidebar.text_input("Taxonomy/Specialty:", "Cardiology")
    if st.sidebar.button("Fetch Federal NPI Records"):
        with st.spinner("Polling Federal Databases..."):
            count = scraper.run_us_npi_api_scraper(us_city, us_spec)
            st.sidebar.success(f"Ingested {count} net-new verified practitioner profiles.")

if st.sidebar.button("Run Competitor Footprint Mapping Engine"):
    with st.spinner("Processing deep web index mapping workflows..."):
        ai_engine.run_enrichment_pipeline()
        st.sidebar.success("Competitor analysis metrics successfully written to database!")

# --- MULTI-ROLE CORE DISPLAY ROUTING PORTALS ---
role = st.radio("Access Control Operational Viewport Matrix:", ["Field Executive Validation Panel", "Sales Intelligence Target Feed"], horizontal=True)

def fetch_filtered_records(status):
    conn = sqlite3.connect("leads_intelligence.db")
    query = "SELECT * FROM healthcare_leads WHERE verification_status = ?"
    df = pd.read_sql_query(query, conn, params=(status,))
    conn.close()
    return df

# --- SCREEN 1: FIELD EXECUTIVE QUEUE ---
if role == "Field Executive Validation Panel":
    st.header("📋 Pending Ground Verification Queue")
    df_field = fetch_filtered_records("Pending Field Visit")
    
    if df_field.empty:
        st.info("✨ Ground pipelines clear. No current provider entries require manual field validation cycles.")
    else:
        st.dataframe(df_field[["id", "name", "phone", "address", "lead_type", "source_url"]], use_container_width=True)
        
        st.subheader("🖋️ Submit Ground Field Investigation Report (Root Cause Analysis - RCA)")
        with st.form("ground_verification_form"):
            target_id = st.number_input("Target System ID Reference:", min_value=1, step=1)
            exec_name = st.text_input("Assigned Field Officer Signature:")
            rca_notes = st.text_area("Root Cause Analysis (Why are they unlisted? What are their core operational software challenges?)")
            intel_notes = st.text_area("Inside Intel (Key Decision Maker name, gatekeeper schedule, tech pain points)")
            
            if st.form_submit_button("Verify Report and Unlock for Sales Deployment"):
                if exec_name and rca_notes:
                    conn = sqlite3.connect("leads_intelligence.db")
                    cursor = conn.cursor()
                    cursor.execute('''
                        UPDATE healthcare_leads 
                        SET verification_status = 'Verified', field_executive_name = ?, root_cause_analysis = ?, inside_intelligence = ?
                        WHERE id = ?
                    ''', (exec_name, rca_notes, intel_notes, target_id))
                    conn.commit()
                    conn.close()
                    st.success(f"Account Profile #{target_id} processed and transferred to Sales Dashboard.")
                    st.rerun()

# --- SCREEN 2: THE SALES INTEL HIGH-TRACEABILITY FEED ---
else:
    st.header("🎯 Highly Enriched Qualified Lead Feed Pipeline")
    df_sales = fetch_filtered_records("Verified")
    
    if df_sales.empty:
        st.warning("⏳ System holding state. Awaiting completion of ground validation cycles by field teams.")
    else:
        for idx, row in df_sales.iterrows():
            badge = "🟢 Organic Inbound" if row['lead_type'] == "Organic (Inbound)" else "🔍 Inorganic Outbound"
            
            with st.expander(f"{badge} | {row['name']} | Competitors: {row['competitor_presence']}"):
                
                # --- HIGH TRACEABILITY ORIGIN LOGS BLOCK ---
                st.info(f"📌 **Lead Origin & Traceability Proof Panel**")
                v_col1, v_col2 = st.columns(2)
                with v_col1:
                    st.markdown(f"**📥 Capture Channel:** {row['lead_type']}")
                    st.markdown(f"**🏗️ Extraction Blueprint:** {'Federal JSON Database Sync' if 'npiregistry' in row['source_url'] else 'Playwright Dynamic Browser Memory Scan'}")
                with v_col2:
                    st.link_button("🌐 Open Live Raw Data Source Validation Link", url=row['source_url'], use_container_width=True)
                
                st.markdown("---")
                
                # --- METRIC INSIGHTS DISPLAY BLOCKS ---
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**🤖 AI Processing Summary:** *{row['ai_summary']}*")
                    st.markdown(f"**💡 AI Actionable Pitch Strategy:** {row['ai_rationale']}")
                with col2:
                    st.markdown(f"**🕵️ Authenticated By Field Officer:** {row['field_executive_name']}")
                    st.markdown(f"**🛑 Ground Root Cause Analysis Report:** {row['root_cause_analysis']}")
                    st.markdown(f"**🔑 Internal Account Intelligence Pockets:** {row['inside_intelligence']}")
                
                st.button("Lock Target Account to My Representative Portfolio", key=f"lock_{row['id']}", type="primary")
