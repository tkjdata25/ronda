import streamlit as st
import requests
import json

st.title("📅 Jadwal Ronda (Streamlit + GitHub)")

# ========================================
# RAW URL GitHub (ubah sesuai repo kamu)
# ========================================
RAW_URL = "https://raw.githubusercontent.com/USERNAME/REPO/main/jadwal.json"

# ========================================
# Fungsi ambil data dari GitHub
# ========================================
def load_data():
    try:
        response = requests.get(RAW_URL)
        if response.status_code == 200:
            return response.json()
        else:
            st.error("Gagal mengambil data dari GitHub.")
            return []
    except:
        st.error("Terjadi kesalahan saat mengambil data.")
        return []

# ========================================
# TAMPILKAN DATA
# ========================================
data = load_data()

st.header("📋 Daftar Jadwal Ronda")

if data:
    st.table(data)
else:
    st.warning("Tidak ada data untuk ditampilkan.")
