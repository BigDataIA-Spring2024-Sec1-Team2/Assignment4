import streamlit as st
from menu import menu
from service import upload_file_api

menu()

def upload_pdf():
    st.title("Upload PDF")
    # File upload widget
    uploaded_file = st.file_uploader("Upload PDF file", type="pdf")

    if uploaded_file is not None:
        st.write("File uploaded successfully!")
        # st.write("Filename:", uploaded_file.name)

        # Button to trigger API upload
        if st.button("Upload to S3"):
            response = upload_file_api(uploaded_file)
            st.write("Below is the S3 File path to your file:")
            st.code(response)

upload_pdf()
