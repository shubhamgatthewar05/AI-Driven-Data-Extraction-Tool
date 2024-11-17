
import streamlit as st
import pandas as pd
from google.oauth2 import service_account
from googleapiclient.discovery import build
from serpapi import GoogleSearch
import requests
import time
import re
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.llms import HuggingFaceHub

# API Keys.............................................................................................................................................................................
serpapi_key = "ADD YOUR SERPAPI API HERE"
hf_api_token = "ADD YOUR Hugging FACE APII TOKEN"
hf_model_url = "https://api-inference.huggingface.co/models/openai-community/gpt2"




# LangChain Configuration................................................................................................................................................................
hf_llm = HuggingFaceHub(repo_id="gpt2", huggingfacehub_api_token=hf_api_token)





# Page Configuration....................................................................................................................................................................
st.set_page_config(
    page_title="Enhanced AI Data Extraction Tool",
    page_icon="✨",
    layout="wide"
)



#fetch Google Sheets....................................................................................................................................................................
def fetch_google_sheet(spreadsheet_id, range_name):
    try:
        credentials = service_account.Credentials.from_service_account_file("path_to_service_account.json")
        service = build("sheets", "v4", credentials=credentials)
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
        values = result.get('values', [])
        return pd.DataFrame(values[1:], columns=values[0]) if values else None
    except Exception as e:
        st.error(f"Error fetching Google Sheet: {e}")
        return None



#export results to Google Sheets....................................................................................................................................................................
def export_to_google_sheet(spreadsheet_id, range_name, data):
    try:
        credentials = service_account.Credentials.from_service_account_file("path_to_service_account.json")
        service = build("sheets", "v4", credentials=credentials)
        body = {"values": [data.columns.tolist()] + data.values.tolist()}
        service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption="RAW",
            body=body
        ).execute()
        st.success("Results exported to Google Sheets successfully!")
    except Exception as e:
        st.error(f"Error exporting to Google Sheets: {e}")



#fetch search results....................................................................................................................................................................
def fetch_search_results(entity, query_template):
    query = query_template.replace("{entity}", entity)
    params = {
        "engine": "google",
        "q": query,
        "api_key": serpapi_key
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    return results.get("organic_results", [])



#extract email from text....................................................................................................................................................................
def extract_email(text):
    match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
    return match.group(0) if match else "Not Found"



# LangChain-based information extraction....................................................................................................................................................................
def extract_with_langchain(entity, search_results, prompts):
    search_text = "\n".join([f"{result.get('title', 'No Title')}: {result.get('snippet', 'No Snippet')}" for result in search_results])
    extracted_info = {}
    for prompt in prompts:
        prompt_template = PromptTemplate(
            input_variables=["entity", "search_text"],
            template=prompt
        )
        chain = LLMChain(llm=hf_llm, prompt=prompt_template)
        response = chain.run({"entity": entity, "search_text": search_text})
        column_name = re.sub(r"[^a-zA-Z0-9_ ]", "", prompt.split(" ")[1]).strip()  # Generateing  column name dynamically...........
        extracted_info[column_name] = response.strip() if response else "No result"
    return extracted_info



# Title and introduction....................................................................................................................................................................
st.title("✨ Enhanced AI-Driven Data Extraction Tool")
st.markdown(
    """
    Welcome to the **Enhanced AI-Driven Data Extraction Tool**!  
    This tool leverages **LangChain**, **Hugging Face**, and **Google Search APIs** to extract, analyze, and visualize data based on your input.
    """
)



# Sidebar instructions....................................................................................................................................................................
with st.sidebar:
    st.header("📋 Instructions")
    st.write(
        """
        1. **Upload a CSV file** or **Enter Google Sheet ID** to load data.  
        2. **Select a column** containing entities for extraction.  
        3. Use multiple prompts to extract detailed data.  
        4. Click **Run Extraction** to process and export results.
        """
    )
    st.markdown("---")
    st.info("Make sure your API keys are configured correctly!")



# File upload or Google Sheets connection....................................................................................................................................................................
st.subheader("📂 Upload Data")
uploaded_file = st.file_uploader("Upload a CSV file", type="csv")
google_sheet_url = st.text_input("Or, enter Google Sheet ID:")



# Loading the  data....................................................................................................................................................................
data = None
if uploaded_file:
    data = pd.read_csv(uploaded_file)
    st.success("CSV file uploaded successfully!")
elif google_sheet_url:
    try:
        sheet_id = google_sheet_url.split("/")[5]
        data = fetch_google_sheet(sheet_id, "Sheet1!A1:A100")
        st.success("Google Sheet data loaded successfully!")
    except Exception as e:
        st.error(f"Error loading Google Sheet: {e}")



# Display data preview....................................................................................................................................................................
if data is not None:
    st.subheader("👀 Data Preview")
    st.write(data.head())
    column = st.selectbox("Select Column for Entity Names:", data.columns)



    # Row selection,.....................................................................
    st.subheader("🔍 Select Rows for Extraction")
    selected_rows = []
    for i, entity in enumerate(data[column]):
        if st.checkbox(f"Select row {i + 1} ({entity})", key=i):
            selected_rows.append(entity)




    # Multiple prompts,.....................................................................
    st.subheader("✏️ Customize Prompts")
    num_prompts = st.number_input("Number of prompts:", min_value=1, value=1, step=1)
    prompts = [st.text_area(f"Enter prompt {i+1}:", "Extract the email address of {entity} from the following results:\n{search_text}") for i in range(num_prompts)]



    # Query template,......
    # 
    # ...............................................................



    query_template = st.text_input("Enter search query template (use {entity} as a placeholder):", "Get me the email address of {entity}")

    # Export option,.....................................................................
    export_option = st.checkbox("Export results to Google Sheets?")
    export_sheet_id = None
    if export_option:
        export_sheet_id = st.text_input("Enter Google Sheet ID for export:")




    # Run extraction,.....................................................................
    if st.button("🚀 Run Extraction"):
        if selected_rows:
            st.info(f"Processing {len(selected_rows)} selected entities...")
            results = []
            for entity in selected_rows:
                st.write(f"🔄 Processing: {entity}")
                search_results = fetch_search_results(entity, query_template)
                extracted_info = extract_with_langchain(entity, search_results, prompts)
                extracted_info["Entity"] = entity
                extracted_info["Email"] = extract_email(" ".join(extracted_info.values()))
                results.append(extracted_info)
                time.sleep(1)

            
            results_df = pd.DataFrame(results)

            
            st.subheader("📊 Extraction Results")
            st.write(results_df)

          
            if export_option and export_sheet_id:
                export_to_google_sheet(export_sheet_id, "Sheet1!A1", results_df)

            # Download button
            st.download_button(
                "⬇️ Download Results as CSV",
                results_df.to_csv(index=False),
                file_name="extracted_data.csv"
            )
        else:
            st.warning("Please select at least one row to proceed.")
