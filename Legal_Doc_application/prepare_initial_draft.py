from genai_config import configure_genai, get_genai_client
from langchain_core.prompts import PromptTemplate

class InitialDraftGenerator:
    def __init__(self, api_key):
        self.api_key = api_key
        self.llm = None
        self.prompt_template = """
            Prepare an initial draft based on the following user query:
            Initial Draft for the given {chunk}
            User Query:
            {user_query}

            Please create an initial draft that addresses the query.
        """
        self.configure_api()

    def configure_api(self):
        """Configure the Gemini API client."""
        configure_genai(self.api_key)
        self.llm = get_genai_client()

    def generate_draft(self, user_query, chunk):
        """Generate the initial draft based on the user query and chunk."""
        # Create the prompt using the template
        prompt = PromptTemplate(input_variables=["user_query", "chunk"], template=self.prompt_template)

        # Generate content using the configured language model
        response = self.llm.generate_content(contents=prompt.format(user_query=user_query, chunk=chunk))

        # Return the response text as a list of lines
        return response.text.split("\n")
