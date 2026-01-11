import streamlit as st
from supabase import Client, create_client
from dotenv import load_dotenv
import os
import pandas as pd
import plotly.express as px

load_dotenv()
    
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

if "sesi" not in st.session_state:
    st.session_state.sesi = 1

supabase: Client = create_client(url,key)


if st.session_state.sesi == 1:
    st.header("Ini coba pake Supabase")
    with st.form(key="test", clear_on_submit= True):
        nama = st.text_input("Masukkan nama")
        alamat = st.text_input("Masukkan alamat")
        nomor_telepon = st.number_input("Masukkan nomor telepon", step=1)
        tanggal = str(st.date_input("Masukkan tanggal", format="DD/MM/YYYY", value= None))
        produk = st.selectbox("Pilih produk", ["HP", "Laptop", "Tablet", "Drone"], placeholder="Pilih produk")
        
        x= st.form_submit_button()
        if x:
            if nama and alamat and nomor_telepon and tanggal and produk:
                supabase.table("Pelanggan").insert({
                    "nama": nama,
                    "alamat": alamat,
                    "nomor_telepon": nomor_telepon,
                    "tanggal": tanggal,
                    "produk": produk
                }).execute()    

                st.balloons()
                st.session_state.sesi = 2
                st.rerun()
            else:
                st.error("Masukin datanya dong")
        
    bt_tampil = st.button("Lihat Data")

    if bt_tampil:
        st.session_state.sesi = 2
        st.rerun()

if st.session_state.sesi == 2:
    st.header("Data Pelanggan")
    df = supabase.table("Pelanggan").select("*").execute()
    data =pd.DataFrame(df.data)

    st.dataframe(data)
    jumlah_produk = data["produk"].value_counts().reset_index()
    jumlah_produk.columns = ["produk", "jumlah"]

    col1, col2 = st.columns([4,1], gap= "medium")

    with col1:
        w = st.button("Hapus data")
        if w:
            supabase.table("Pelanggan").delete().neq("id",0).execute()
            st.rerun()

    with col2:
        z = st.button("Tambah Data")
        if z:
            st.session_state.sesi = 1
            st.rerun()
    
    st.divider()

    fig = px.pie(
        jumlah_produk,
        names="produk",
        values="jumlah",
        title="Proporsi Jumlah Produk"
    )
    st.plotly_chart(fig)
