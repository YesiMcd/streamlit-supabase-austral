import streamlit as st
from supabase import create_client

def get_supabase_client():
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_DB_PASSWORD"]
    return create_client(url, key)