# **Enhanced AI-Driven Data Extraction Tool** ✨

This project is a versatile tool designed to simplify and automate the extraction of meaningful data from web searches. By leveraging the **Hugging Face API**, **Google Search API**, and **LangChain**, users can define prompts to retrieve specific information such as email addresses, founder names, or any other custom data.

[![Demo Video](https://img.shields.io/badge/YouTube-Demo-red?style=for-the-badge&logo=youtube)](https://youtu.be/IJHSkFvh8eU?si=GnYJxBlN6oS9nWAu)

---

## **🚀 Features**

### **1. Multiple Data Input Options**
- **CSV Upload**: Upload a CSV file directly from your local system.
- **Google Sheets Integration**: Load data from a Google Sheet by entering its ID.

### **2. Customizable Prompts for AI Extraction**
- Define multiple prompts to guide the AI in extracting specific details from web search results.
- Examples: *"Find the email address of {entity}"*, *"Extract the founder's name for {entity}"*.

### **3. AI-Powered Data Processing**
- Uses Google Search API to retrieve relevant results for the selected entities.
- Processes the results using **LangChain** and **Hugging Face's GPT-2** model to extract the required information.

### **4. Email Address Detection**
- Employs regular expressions to dynamically identify and extract email addresses from the AI's output.
- Stores the extracted emails in a separate column in the results dataset.

### **5. Export and Download Options**
- **CSV Export**: Download the extracted data in CSV format.
- **Google Sheets Export**: Directly export the results to a specified Google Sheet.

---

## **📋 Installation**

1. **Clone the repository**  
   ```bash
   git clone https://github.com/your-username/enhanced-ai-data-extraction.git
   cd enhanced-ai-data-extraction
   ```

2. **Install dependencies**  
   Use the provided `requirements.txt` file to install all necessary packages.  
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up API Keys**  
   - Replace placeholders in the code with your **SerpAPI** and **Hugging Face** API keys.  
   - Add your **Google Cloud Service Account JSON file** path for Google Sheets integration.

4. **Run the Streamlit app**  
   ```bash
   streamlit run app.py
   ```

---

## **🛠️ Usage**

1. **Load Data**  
   - Upload a CSV file or provide a Google Sheet ID to load your dataset.

2. **Select Column and Rows**  
   - Choose the column containing the entities for extraction and select specific rows for processing.

3. **Customize Prompts**  
   - Define one or more prompts to guide the AI in extracting relevant information.

4. **Run Extraction**  
   - Click the **Run Extraction** button to start the process.

5. **View Results**  
   - Results are displayed in real-time and can be downloaded or exported to Google Sheets.

---

## **🖥️ Demo**

[![Watch the Demo](https://img.shields.io/badge/YouTube-Watch_Demo-red?style=for-the-badge&logo=youtube)](https://youtu.be/IJHSkFvh8eU?si=GnYJxBlN6oS9nWAu)

Watch a 2-minute walkthrough showcasing the tool's features, dashboard workflow, and key functionalities.

---

## **📂 File Structure**

```plaintext
enhanced-ai-data-extraction/
├── app.py                 # Main Streamlit application code
├── requirements.txt       # Required Python libraries
├── README.md              # Project documentation
├── utils/                 # Utility functions (e.g., API handlers, data processing)
├── assets/                # Images and assets for the project
└── path_to_service_account.json # Your Google Cloud Service Account JSON file
```

---

## **📖 How It Works**

1. **Search Results Retrieval**:  
   - Fetches web search results for each entity using the SerpAPI.

2. **AI-Based Extraction**:  
   - Processes search results with Hugging Face's GPT-2 and LangChain for data extraction based on user-defined prompts.

3. **Email Extraction**:  
   - Dynamically identifies email addresses from the AI-generated text using regular expressions.

4. **Results Compilation**:  
   - Stores all extracted information, including emails, in a structured table.

5. **Export Options**:  
   - Allows downloading the results as a CSV file or exporting them to Google Sheets.

---

## **🔑 API Configuration**

### **1. SerpAPI**  
Sign up for a free or paid account on [SerpAPI](https://serpapi.com/) and obtain your API key.

### **2. Hugging Face**  
Generate a personal access token from [Hugging Face](https://huggingface.co/settings/tokens) for API usage.

### **3. Google Cloud Service Account**  
Set up a service account in Google Cloud, enable Sheets API, and download the JSON key file.

---

## **🎯 Future Enhancements**

- Add support for additional AI models (e.g., GPT-3 or similar advanced models).
- Include more visualization options for the extracted data.
- Implement rate-limiting and caching mechanisms for API efficiency.
- Add support for multilingual data extraction.

---

## **🤝 Contributing**

Contributions are welcome! Feel free to fork the repository and submit a pull request with your improvements.

---

## **📜 License**

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Let me know if you need any further updates or improvements!
