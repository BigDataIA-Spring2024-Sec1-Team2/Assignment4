import streamlit as st
from menu import menu

menu()

def upload_pdf():
    st.title("Upload PDF")
    # File upload widget
    uploaded_file = st.file_uploader("Upload PDF file", type="pdf")

    if uploaded_file is not None:
        st.write("File uploaded successfully!")
        st.write("Filename:", uploaded_file.name)

        # Button to trigger API upload
        if st.button("Upload to API"):
            # response = upload_file_to_api(uploaded_file)
            s3_file_path = "s3://bucket_name/path/to/file"
            st.write("S3 File path:", s3_file_path)

upload_pdf()
