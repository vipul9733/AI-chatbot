from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import TextLoader
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
import os

class RAGSystem:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings()
        self.vector_store = None
        self.qa_chain = None
        self.load_knowledge_base()

    def load_knowledge_base(self):
        try:
            # Load training data
            loader = TextLoader("data/training_data.txt")
            documents = loader.load()
            
            # Split texts
            text_splitter = CharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200
            )
            texts = text_splitter.split_documents(documents)
            
            # Create vector store
            self.vector_store = Chroma.from_documents(
                texts,
                self.embeddings
            )
            
            # Create QA chain
            self.qa_chain = RetrievalQA.from_chain_type(
                llm=OpenAI(),
                chain_type="stuff",
                retriever=self.vector_store.as_retriever()
            )
        except Exception as e:
            print(f"Error loading knowledge base: {e}")

    def get_response(self, query):
        try:
            if self.qa_chain is None:
                return "I'm sorry, but I'm having trouble accessing my knowledge base."
            
            response = self.qa_chain.run(query)
            return response
        except Exception as e:
            print(f"Error getting response: {e}")
            return "I apologize, but I'm having trouble generating a response."