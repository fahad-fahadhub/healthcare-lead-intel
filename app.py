import streamlit as st
import sqlite3
import pandas as pd
from database import init_db, insert_lead
import scraper
import ai_engine

st.set_page_config(layout="wide", page_title="Healthcare Lead Intelligence Portal")
init_db()

st.title("🩺 Healthcare Lead Intelligence System (HLIS)")

# --- INTEGRATED INBOUND ORGANIC HOOK NODE ---
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
            success = insert_lead(inbound_name, inbound_phone, inbound_address, "Organic Platform Intake Form", "Organic (Inbound)", "None", "Organic Inbound", "Immediate Outreach Recommended")
            if success:
                st.success("Lead ingested into the processing workflow queue!")
            else:
                st.warning("Provider entry already mapped within system directory tables.")

# --- SIDEBAR CONTROL CENTER PANEL ---
st.sidebar.header("🕹️ System Operations")
# Input authorization key needed to authenticate calls directly into Google's developer framework
api_token = st.sidebar.text_input("Google Gemini API Token Secret Key:", type="password")
target_city = st.sidebar.text_input("Target City Matrix Location:", "Bangalore")
target_spec = st.sidebar.text_input("Specialty Matrix Focus Group:", "Cardiologist")

if st.sidebar.button("🚀 ONE-CLICK EXTRACT & AUTOMATED FILTER (15 LEADS)"):
    if not api_token:
        st.sidebar.error("⚠️ Authentication Key Missing! Please input your Gemini API Token.")
    else:
        with st.spinner("Invoking Gemini session matrices, cross-checking competitor listings, and compiling 15 exclusive targets..."):
            count = scraper.run_gemini_session_miner(target_city, target_spec, api_token, target_count=15)
            st.sidebar.success(f"Pipeline Filled! Ingested {count} unique, unlisted healthcare accounts.")

# --- DISPLAY ROUTING PORTALS ---
role = st.radio("Access Control Operational Viewport Matrix:", ["Field Executive Validation Panel", "Sales Intelligence Target Feed"], horizontal=True)

def fetch_filtered_records(status):
    conn = sqlite3.connect("leads_intelligence.db")
    query = "SELECT * FROM healthcare_leads WHERE verification_status = ?"
    df = pd.read_sql_query(query, conn, params=(status,))
    conn.close()
    return df

if role == "Field Executive Validation Panel":
    st.header("📋 Pending Ground Verification Queue")
    df_field = fetch_filtered_records("Pending Field Visit")
    
    if df_field.empty:
        st.info("✨ Ground pipelines clear. No provider profiles require verification cycles.")
    else:
        st.dataframe(df_field[["id", "name", "phone", "address", "lead_type", "source_url"]], use_container_width=True)
        st.subheader("🖋️ Submit Ground Field Investigation Report (RCA)")
        with st.form("ground_verification_form"):
            target_id = st.number_input("Target System ID Reference:", min_value=1, step=1)
            exec_name = st.text_input("Assigned Field Officer Signature:")
            rca_notes = st.text_area("Root Cause Analysis (Tech challenges, missing listings):")
            intel_notes = st.text_area("Inside Intel (Key Decision Maker, best schedule to call):")
            
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
else:
    st.header("🎯 Highly Enriched Qualified Lead Feed Pipeline")
    df_sales = fetch_filtered_records("Verified")
    
    if df_sales.empty:
        st.warning("⏳ System holding state. Awaiting completion of ground validation cycles.")
    else:
        for idx, row in df_sales.iterrows():
            badge = "🟢 Organic Inbound" if row['lead_type'] == "Organic (Inbound)" else "🔍 Inorganic Outbound"
            with st.expander(f"{badge} | {row['name']} | Competitors: {row['competitor_presence']}"):
                st.info(f"📌 **Lead Origin & Traceability Proof Panel**")
                v_col1, v_col2 = st.columns(2)
                with v_col1:
                    st.markdown(f"**📥 Capture Channel:** {row['lead_type']}")
                    st.markdown(f"**🏗️ Extraction Source:** Google Gemini Session Context Layer")
                with v_col2:
                    st.link_button("🌐 Open Live Raw Data Source Validation Link", url=row['source_url'], use_container_width=True)
                
                st.markdown("---")
                
                if st.button(f"🔍 Execute Deep Live Google OSINT Market Research", key=f"osint_{row['id']}"):
                    if not api_token:
                        st.error("⚠️ Input your Gemini API Token Key in the sidebar control to execute live deep web research.")
                    else:
                        with st.spinner("Invoking Gemini web-indexing matrices across live directories..."):
                            deep_sum, deep_rat = ai_engine.research_lead_deep_gemini(row['name'], target_city, api_token)
                            conn = sqlite3.connect("leads_intelligence.db")
                            cursor = conn.cursor()
                            cursor.execute("UPDATE healthcare_leads SET ai_summary = ?, ai_rationale = ? WHERE id = ?", (deep_sum, deep_rat, row['id']))
                            conn.commit()
                            conn.close()
                            st.success("Deep research complete! AI insights updated.")
                            st.rerun()
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**🤖 AI Processing Summary:** *{row['ai_summary']}*")
                    st.markdown(f"**💡 AI Actionable Pitch Strategy:** {row['ai_rationale']}")
                with col2:
                    st.markdown(f"**🕵️ Authenticated By Field Officer:** {row['field_executive_name']}")
                    st.markdown(f"**🛑 Ground Root Cause Analysis Report:** {row['root_cause_analysis']}")
                    st.markdown(f"**🔑 Internal Account Intelligence Pockets:** {row['inside_intelligence']}")
                st.button("Lock Target Account to My Representative Portfolio", key=f"lock_{row['id']}", type="primary")
