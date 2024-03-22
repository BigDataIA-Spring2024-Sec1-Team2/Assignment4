import streamlit as st
from menu import menu

st.set_option("client.showSidebarNavigation", False)

st.set_page_config(
        page_title="Team 2: PDF Extracton",
        page_icon=":handshake",
        layout="wide"
    )

menu()

st.title("Team 2: PDF Extraction Airflow Pipeline")

st.write("Start by uploading your pdf to AWS S3 bucket")
if st.button("Upload PDF"):
    st.switch_page("pages/page_1.py")
    


    
