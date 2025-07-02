import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

class LLMHandler:
    """
    Handles all interactions with the Large Language Model (LLM).
    This class is responsible for taking a user query and retrieved context,
    formatting them into a prompt, sending it to the LLM, and returning the response.
    """
    def __init__(self):
        """
        Initializes the handler by setting up the LLM, prompt template, and the RAG chain.
        It expects the GOOGLE_API_KEY to be available as an environment variable,
        loaded from a .env file by the main application's config.
        """
        # --- 1. Verify API Key and Initialize the LLM ---
        # This check ensures the application fails fast if the API key is missing.
        if not os.getenv("GOOGLE_API_KEY"):
            raise ValueError(
                "GOOGLE_API_KEY not found. "
                "Please ensure it is set in a .env file in the project's root directory."
            )

        # Initialize the Google Gemini Pro model.
        # It automatically uses the GOOGLE_API_KEY from the environment.
        self.model = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",  # Using the stable version
            temperature=0.3  # A lower temperature promotes more factual, less creative answers
        )

        # --- 2. Define the Prompt Template ---
        # This template is the instruction set for the LLM. It strictly tells the model
        # to answer ONLY based on the provided context. This is the core of RAG's reliability.
        self.prompt_template = PromptTemplate.from_template(
            """
            You are an expert AI assistant for the MOSDAC (Meteorological and Oceanographic Satellite Data Archival Centre) portal.
            Your primary task is to answer the user's question accurately and concisely based ONLY on the context provided below.

            - Do not use any outside knowledge or information you were trained on.
            - If the context does not contain the answer to the question, you must state: "I could not find an answer in the provided documents."
            - After providing the answer, list all the source URLs or document titles you used under a "Sources:" heading.

            CONTEXT:
            {context}

            QUESTION:
            {question}

            ANSWER:
            """
        )

        # --- 3. Create the RAG Chain using LangChain Expression Language (LCEL) ---
        # This chain defines the step-by-step data flow for processing a query.
        self.chain = (
            # The input to the chain is a dictionary with 'question' and 'context_docs'.
            # The 'context' key is populated by calling the _format_context method.
            # The 'question' key is passed through directly.
            {"context": self._format_context, "question": RunnablePassthrough()}
            | self.prompt_template
            | self.model
            | StrOutputParser() # Parses the LLM's chat message output into a simple string.
        )

    def _format_context(self, context_data: dict) -> str:
        """
        A helper method to format the list of retrieved documents into a single,
        readable string to be injected into the prompt's context.
        """
        # The input is the dictionary passed from the chain, containing all input variables.
        docs_with_scores = context_data.get('context_docs', [])
        if not docs_with_scores:
            return "No context provided."
            
        context_parts = []
        for doc, score in docs_with_scores:
            source = doc.metadata.get('source', 'N/A')
            title = doc.metadata.get('title', 'No Title')
            content = doc.page_content
            # Each document is clearly marked with its source and title.
            context_parts.append(f"Source: {source} (Title: {title})\nContent: {content}")
        
        # Documents are separated by a clear line for the LLM to distinguish them.
        return "\n\n---\n\n".join(context_parts)

    def get_response(self, query: str, context_docs: list) -> str:
        """
        The main method called by the API to generate a response.
        It invokes the RAG chain with the user's query and the retrieved documents.

        Args:
            query (str): The user's original question.
            context_docs (list): A list of (Document, score) tuples from the vector store.

        Returns:
            str: The final, LLM-generated answer as a string.
        """
        if not context_docs:
            return "I could not find any relevant information in the knowledge base to answer your question."
        
        try:
            # The chain is invoked with a dictionary matching the inputs defined in its construction.
            # The _format_context method expects 'context_docs', and the prompt expects 'question'.
            # We pass the question through the `RunnablePassthrough` by providing it again at the top level.
            return self.chain.invoke({
                "question": query,
                "context_docs": context_docs
            })
        except Exception as e:
            # Catch potential API errors (e.g., rate limits, network issues) from Google AI.
            print(f"ERROR: An error occurred while calling the Google Gemini API: {e}")
            return "Sorry, I encountered an error while communicating with the AI service. Please try your question again later."