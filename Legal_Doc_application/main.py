import os
from io import BytesIO
import streamlit as st
from dotenv import load_dotenv
from pypdf import PdfReader
from utils import get_text_chunks, get_vector_store
from extract_key_clauses import extract_key_clauses
from summarize_document import summarize_document
from prepare_initial_draft import prepare_initial_draft
from genai_config import configure_genai, get_genai_client  # Import from genai_config
from langchain_core.prompts import PromptTemplate

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Configure Gemini API (using the new config file)
configure_genai(GEMINI_API_KEY)

# Class to handle document processing
class LegalDocumentProcessor:
    def __init__(self, api_key):
        self.api_key = api_key
        self.chunk = None
        self.contract_text = ""
    
    def get_pdf_text(self, file):
        """Extract text from the uploaded PDF."""  
        text = ""    
        if isinstance(file, BytesIO):
            reader = PdfReader(file)
        else:
            reader = PdfReader(BytesIO(file.read()))

        for page in reader.pages:
            text += page.extract_text() or ""
        return text
    
    def process_uploaded_file(self, uploaded_file):
        """Process the uploaded PDF file."""
        if uploaded_file:
            self.contract_text = self.get_pdf_text(uploaded_file)
            self.chunk = get_text_chunks(self.contract_text)
        else:
            st.warning("Please upload a PDF file to proceed.")

# Sidebar UI for file upload
def create_sidebar():
    with st.sidebar:
        st.header("Upload Legal Files")
        st.write("Upload PDF files related to employment law to get personalized legal advice.")
        files = st.file_uploader('Upload the Legal Files', type=['pdf'], accept_multiple_files=True)
        if files:
            for file in files:
                st.success(f"File '{file.name}' uploaded successfully!")
        else:
            st.warning("No files were uploaded.")
    return files

# Main UI
def main():
    # Initialize the LegalDocumentProcessor
    processor = LegalDocumentProcessor(GEMINI_API_KEY)
    
    # Create sidebar and handle file upload
    uploaded_file = st.file_uploader("Upload a PDF Contract", type="pdf")
    processor.process_uploaded_file(uploaded_file)

    # Tabs for different actions
    tab1, tab2, tab3 = st.tabs(["Extract Key Clauses", "Summarize Document", "Prepare Initial Draft"])

    with tab1:
        if processor.chunk and st.button("Extract Clauses"):
            extract_key_clauses(processor.chunk)

    with tab2:
        if processor.chunk and st.button("Summarize"):
            summary = summarize_document(processor.chunk)
            st.write("Document Summary:")
            for item in summary:
                st.write(item)

    with tab3:
        user_query = st.text_input("Enter your query for the initial draft")
        if processor.chunk and st.button("Generate Draft") and user_query:
            draft = prepare_initial_draft(user_query, processor.chunk)
            st.write("Initial Draft:")
            for item in draft:
                st.write(item)

# Run the Streamlit app
if __name__ == "__main__":
    st.title("Legal Document Automation App")
    main()
