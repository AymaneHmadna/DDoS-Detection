import streamlit as st
import pandas as pd
from cassandra.cluster import Cluster
import time
import datetime
st.set_page_config(page_title="Network Attack Detection", layout="wide")
COLOR_BG = "#1E1E24"
COLOR_CARD = "#555663"
COLOR_TEXT = "#FCFDFD"
COLOR_ACCENT = "#2F7EDA"
COLOR_SECONDARY = "#9FA0B5"
COLOR_DANGER = "#FF4B4B"
COLOR_SUCCESS = "#4CAF50"
st.markdown(f"""
    <style>
    .stApp {{ background-color: {COLOR_BG}; }}
    h1, h2, h3 {{ color: {COLOR_TEXT} !important; font-family: 'Segoe UI', sans-serif; text-align: center; margin-bottom: 0px; }}
    .block-container {{ padding-top: 2rem; }}
    div[data-testid="stMetric"] {{ background-color: {COLOR_CARD}; border-left: 6px solid {COLOR_ACCENT}; padding: 15px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }}
    div[data-testid="stMetricLabel"] p {{ color: {COLOR_SECONDARY} !important; font-size: 14px; font-weight: 600; }}
    div[data-testid="stMetricValue"] div {{ color: {COLOR_TEXT} !important; font-size: 24px; }}
    </style>
""", unsafe_allow_html=True)
@st.cache_resource
def get_session():
    cluster = Cluster(['cassandra_interne'])
    session = cluster.connect()
    return session
try:
    session = get_session()
except Exception as e:
    st.error(f"Cassandra connection error : {e}")
    st.stop()
def load_data():
    try:
        query = "SELECT ip, count, last_seen, prediction FROM projet_logs.resultats_ips LIMIT 2000;"
        rows = session.execute(query)
        df = pd.DataFrame(list(rows))
        if df.empty:
            return pd.DataFrame(columns=['ip', 'count', 'last_seen', 'prediction'])
        temps_obj = pd.to_datetime(df['last_seen']) + pd.Timedelta(hours=1)
        df['last_seen'] = temps_obj.dt.strftime('%H:%M:%S')
        df = df.sort_values(by='last_seen', ascending=False)
        return df
    except Exception as e:
        return pd.DataFrame()
st.title("Network Attack Detection")
st.markdown("<br>", unsafe_allow_html=True)
df = load_data()
if df.empty:
    st.info("SCANNER WAITING FOR DATA...")
else:
    active_sources = df['ip'].nunique()
    vraies_menaces = ['DDoS Attack (Massive)', 'ATTACK DETECTED']
    threats_count = df[df['prediction'].isin(vraies_menaces)].shape[0]
    if threats_count > 0:
        etat_systeme = "CRITICAL"
    else:
        etat_systeme = "ACTIVE"
    col1, col2, col3 = st.columns(3)
    with col1: st.metric(label="SYSTEM STATUS", value=etat_systeme)
    with col2: st.metric(label="ACTIVE IP SOURCES", value=active_sources)
    with col3: st.metric(label="DETECTED THREATS", value=threats_count)
    st.markdown("---")
    def color_threats(val):
        color = COLOR_TEXT
        if 'DDoS' in val or 'ATTACK' in val:
            color = COLOR_DANGER 
        elif 'Safe' in val:
            color = COLOR_SUCCESS
        return f'color: {color}; font-weight: bold;'
    display_df = df.head(50)[['last_seen', 'ip', 'prediction', 'count']].copy()
    display_df.columns = ['TIMESTAMP', 'SOURCE IP', 'VERDICT', 'TARGET PORT']
    st.dataframe(
        display_df.style.map(color_threats, subset=['VERDICT']),
        use_container_width=True,
        height=600,
        hide_index=True
    )
time.sleep(2)
st.rerun()