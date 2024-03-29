import streamlit as st
from menu import menu
from dotenv import dotenv_values
import requests

menu()

st.title('Snowflake Query Executor')

# FastAPI endpoint URL
config = dotenv_values(".env")
fastapi_url = config["API_URL"] + '/execute_query/'
# Text area for inputting the SQL query
query = st.text_area("Enter your SQL query here:")

if st.button('Execute'):
    if query:
        # Send the query to the FastAPI endpoint
        response = requests.post(fastapi_url, json={"query": query})

        if response.status_code == 200:
            # Display the results
            results = response.json()['result']
            st.write(results)
        else:
            st.error(f"Error executing query: {response.text}")
    else:
        st.error("Please enter a SQL query.")

