import streamlit as st

def upload_pdf():
    st.title("Upload PDF")

def trigger_airflow():
    st.title("Trigger Airflow")

def query_snowflake():
    st.title("Database Query")

if __name__ == "__main__":
    st.set_page_config(
        page_title="Team 2 - PDF Extraction",
        page_icon=":handshake",
        layout="wide"
    )

    st.sidebar.title("Team 2 - PDF Extraction Airflow Pipeline")
    page = st.sidebar.selectbox(
        "Select a page",
        ["Upload PDF","Trigger Airflow","Database Query"]
    )

    if page == "Upload PDF":
        upload_pdf()
    elif page == "Trigger Airflow":
        trigger_airflow()
    else:
        query_snowflake()
