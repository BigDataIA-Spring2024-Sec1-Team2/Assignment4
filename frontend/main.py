import streamlit as st
from menu import menu
from service import check_airflow_health
import time
import streamlit_authenticator as stauth

import yaml
from yaml.loader import SafeLoader
with open('./config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Streamlit app to display Airflow health check
def streamlit_airflow_health_monitor(airflow_url):
    # Streamlit widget to start/stop monitoring
    start_button = st.button('check Health ')

    monitoring = False
    # Placeholder for displaying the health check status
    status_placeholder = st.empty()
    run_placeholder = st.text(f"Monitoring... : {monitoring}")
    # Initialize the monitoring status

    # run_placeholder = status_placeholder.text(f"Monitoring... : {monitoring}")

    if start_button:
        monitoring = True

        run_placeholder = run_placeholder.text(f"Monitoring... : {monitoring}")
        
        

    if monitoring:

        run_placeholder = run_placeholder.text(f"Monitoring... : {monitoring}")
        # Perform the health check
        health_status = check_airflow_health(airflow_url)
        # Display the health status
        
        status_placeholder.text(f"Airflow Health Status: {health_status}")
        # Wait for 1 second before the next check
        time.sleep(1)


st.set_option("client.showSidebarNavigation", False)

st.set_page_config(
        page_title="Team 2: PDF Extracton",
        page_icon=":handshake",
        layout="wide"
    )


authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['pre-authorized']
)

authenticator.login()
if st.session_state["authentication_status"]:
    authenticator.logout()
    st.title('Some content')
    menu()
    st.title("Airflow Health Monitoring Dashboard")
    # Input for the Airflow URL
    airflow_url = st.text_input("Enter Airflow URL", "http://localhost:8080")
    # Run the monitoring function
    streamlit_airflow_health_monitor(airflow_url)



    st.title("Team 2: PDF Extraction Airflow Pipeline")

    st.write("Start by uploading your pdf to AWS S3 bucket")
    if st.button("Upload PDF"):
        st.switch_page("pages/page_1.py")
elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')


