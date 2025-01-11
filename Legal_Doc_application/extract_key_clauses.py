# extract_key_clauses.py

from genai_config import configure_genai
from langchain_core.prompts import PromptTemplate
import streamlit as st

class KeyClauseExtractor:
    def __init__(self):
        """Initialize the KeyClauseExtractor with the provided API key."""
        self.llm = None
        self.prompt_template = """
            Extract the following key clauses from the provided contract text:

            1. Effective Date
            2. Service Provider
            3. Client
            4. Scope of Services
            5. Compensation
            6. Term and Termination
            7. Confidentiality
            8. Intellectual Property Rights
            9. Limitation of Liability
            10. Dispute Resolution
            11. Governing Law

            Contract Text:
            {contract_text}

            Please respond in the following format:
            Effective Date: [Effective Date]
            Service Provider: [Service Provider]
            Client: [Client]
            Scope of Services: [Scope of Services]
            Compensation: [Compensation]
            Term and Termination: [Term and Termination]
            Confidentiality: [Confidentiality]
            Intellectual Property Rights: [Intellectual Property Rights]
            Limitation of Liability: [Limitation of Liability]
            Dispute Resolution: [Dispute Resolution]
            Governing Law: [Governing Law]
        """
        self.configure_api()

    def configure_api(self):
        """Configure the Gemini API client."""
        genai=configure_genai()
        self.llm = genai.GenerativeModel(model_name="gemini-1.5-flash")

    def extract_clauses(self, contract_text):
        """Extract key clauses from the provided contract text."""
        # Create the prompt using the template
        prompt = PromptTemplate(input_variables=["contract_text"], template=self.prompt_template)

        try:
            # Generate content using the LLM
            response = self.llm.generate_content(contents=prompt.format(contract_text=contract_text))

            # Return the extracted clauses
            return response.text
        except Exception as e:
            st.error(f"Error generating content: {e}")
            return None


def extract_key_clauses(contract_text):
    """Function to extract key clauses from the contract text."""
    # Initialize the KeyClauseExtractor with the Gemini API key
    clause_extractor = KeyClauseExtractor()
    
    # Extract the clauses and return the result
    clauses = clause_extractor.extract_clauses(contract_text)
    if clauses:
        st.write(clauses)
    else:
        st.warning("Failed to extract clauses.")
