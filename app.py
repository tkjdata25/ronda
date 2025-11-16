import streamlit as st
import requests
import base64
import json
from datetime import date

# ==============================
# KONFIGURASI GITHUB
# ==============================

GITHUB_TOKEN = st.secrets["github"]["token"]
GITHUB_USERNAME = st.secrets["github"]["username"]
GITHUB_REPO = st.secrets["github"]["repo"]
GITHUB_PATH = st.secrets["github"]["path"]

API_URL = f"https://api.github.com/repos/{GITHUB_USERNAME}/{GITHUB_REPO}/contents/{GITHUB_PATH}"

headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

# ==============================
# FUNGSI LOAD DATA DARI GITHUB
# ==============================

def load_data():
    response = requests.get(API_URL, headers=headers)
    if response.status_code == 200:
        content = response.json()
        file_data = base64.b64decode(content["content"]).decode("utf-8")
        return json.loads(file_data), content["sha"]
    else:
        st.error("Gagal mengambil data dari GitHub.")
        return [], None

# ==============================
# FUNGSI SIMPAN DATA KE GITHUB
# ==============================

def save_data(data, sha):
    new_content = json.dumps(data, indent=4)
    encoded = base64.b64encode(new_content.encode()).decode()

    payload = {
        "message": "Update jadwal ronda",
        "content": encoded,
        "sha": sha
    }

    put_response = requests.put(API_URL, headers=headers, json=payload)

    if put_response.status_code == 200 or put_response.status_code == 201:
        st.success("✔ Jadwal berhasil disimpan ke GitHub!")
    else:
        st.error("❌ Gagal menyimpan data ke GitHub.")


# ==============================
# STREAMLIT UI
# ==============================

st.title("📅 Aplikasi Jadwal Ronda (GitHub + Streamlit)")

menu = st.sidebar.selectbox("Menu", ["Lihat Jadwal", "Tambah Jadwal", "Cari Jadwal"])

data, sha = load_data()

# ==============================
# MENU 1 — LIHAT JADWAL
# ==============================

if menu == "Lihat Jadwal":
    st.header("📋 Daftar Jadwal Ronda")
    if data:
        st.table(data)
    else:
        st.info("Belum ada jadwal.")

# ==============================
# MENU 2 — TAMBAH JADWAL
# ==============================

elif menu == "Tambah Jadwal":
    st.header("➕ Tambah Jadwal")

    nama = st.text_input("Nama Warga")
    tanggal = st.date_input("Tanggal Ronda", date.today())

    if st.button("Simpan Jadwal"):
        if nama:
            data.append({"nama": nama, "tanggal": str(tanggal)})
            save_data(data, sha)
        else:
            st.warning("Nama tidak boleh kosong.")

# ==============================
# MENU 3 — CARI JADWAL
# ==============================

elif menu == "Cari Jadwal":
    st.header("🔍 Cari Jadwal Ronda")
    keyword = st.text_input("Cari berdasarkan nama:")

    if keyword:
        hasil = [d for d in data if keyword.lower() in d["nama"].lower()]
        if hasil:
            st.table(hasil)
        else:
            st.warning("Tidak ditemukan data.")
