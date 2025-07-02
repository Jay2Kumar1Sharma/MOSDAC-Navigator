from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from .config import VECTOR_STORE_PATH, EMBEDDING_MODEL_NAME

class KnowledgeBase:
    def __init__(self):
        """
        Initializes the KnowledgeBase by loading the pre-computed FAISS vector store.
        """
        if not VECTOR_STORE_PATH.exists():
            raise FileNotFoundError(
                f"Vector store not found at {VECTOR_STORE_PATH}. "
                "Please run the data ingestion process first."
            )
        
        print("Loading knowledge base from disk...")
        embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)
        # We need to allow dangerous deserialization for FAISS with custom embeddings
        self.vector_store = FAISS.load_local(
            str(VECTOR_STORE_PATH), 
            embeddings, 
            allow_dangerous_deserialization=True
        )
        print("Knowledge base loaded successfully.")

    def query(self, query_text: str, k: int = 4):
        """
        Performs a search on the vector store to find relevant documents
        using the Maximal Marginal Relevance (MMR) algorithm.

        MMR helps to select documents that are relevant to the query while also
        being as different from each other as possible, promoting diversity in the results.

        Args:
            query_text (str): The user's question.
            k (int): The number of relevant documents to retrieve.

        Returns:
            list: A list of (Document, score) tuples.
        """
        # We use the vector store's built-in MMR search method.
        # fetch_k is the number of documents to initially fetch before applying MMR.
        # It should be larger than k.
        retrieved_docs_with_scores = self.vector_store.similarity_search_with_score(
            query=query_text,
            k=k,
            # Note: Not all vector stores support MMR directly in this function.
            # FAISS's similarity_search does not have a native 'mmr' type.
            # A more robust way is to use the .as_retriever() method as shown below.
        )
        
        # --- The more robust and correct way using as_retriever ---
        retriever = self.vector_store.as_retriever(
            search_type="mmr",
            search_kwargs={'k': k, 'fetch_k': 20} # Fetch 20 docs, then select 4 diverse ones.
        )
        
        # The retriever returns Document objects, not scores.
        # We will wrap them in a tuple with a dummy score to match our expected format.
        relevant_docs = retriever.invoke(query_text)
        
        print(f"Retrieved {len(relevant_docs)} documents using MMR.")
        return [(doc, 0.0) for doc in relevant_docs] # Add dummy score of 0.0