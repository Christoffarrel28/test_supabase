import streamlit as st
from supabase import Client, create_client
from dotenv import load_dotenv
import os
import pandas as pd

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

        x= st.form_submit_button()
        if x:
            if nama and alamat and nomor_telepon:
                supabase.table("Pelanggan").insert({
                    "nama": nama,
                    "alamat": alamat,
                    "nomor_telepon": nomor_telepon
                }).execute()    
                st.balloons()
                st.session_state.sesi = 2
                st.rerun()
            else:
                st.error("Masukin datanya dong")

if st.session_state.sesi == 2:
    st.header("Data Pelanggan")
    df = supabase.table("Pelanggan").select("*").execute()
    st.dataframe(pd.DataFrame(df.data))

    w = st.button("Hapus data")
    if w:
        supabase.table("Pelanggan").delete().neq("id",0).execute()
        st.rerun()

    z = st.button("Tambah data")
    if z:
        st.session_state.sesi = 1
        st.rerun()
    

    



