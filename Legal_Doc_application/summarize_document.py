# summarize_document.py

from genai_config import configure_genai
from langchain_core.prompts import PromptTemplate

class DocumentSummarizer:
    def __init__(self):
        """Initialize the DocumentSummarizer with the provided API key."""
        self.llm = None
        self.prompt_template = """
            Summarize the following legal document:

            Document Text:
            {contract_text}

            Please provide a concise summary of the main points and clauses.
        """
        self.configure_api()

    def configure_api(self):
        """Configure the Gemini API client."""
        genai=configure_genai()
        self.llm = genai.GenerativeModel(model_name="gemini-1.5-flash")

    def summarize(self, contract_text):
        """Generate a summary for the provided contract text."""
        if not self.llm:
            raise Exception("Gemini API is not properly configured.")
        
        # Create the prompt using the template
        prompt = PromptTemplate(input_variables=["contract_text"], template=self.prompt_template)

        try:
            # Generate content using the LLM
            response = self.llm.generate_content(contents=prompt.format(contract_text=contract_text))

            # Return the summary text, splitting into lines for easy readability
            return response.text.split("\n")
        except Exception as e:
            raise Exception(f"Error generating summary: {e}")


def summarize_document(contract_text):
    """Function to summarize the provided contract text."""
    # Initialize the DocumentSummarizer with the Gemini API key
    summarizer = DocumentSummarizer()

    try:
        # Get the document summary
        summary = summarizer.summarize(contract_text)
        
        # Return the summary
        return summary
    except Exception as e:
        return f"Error: {e}"
