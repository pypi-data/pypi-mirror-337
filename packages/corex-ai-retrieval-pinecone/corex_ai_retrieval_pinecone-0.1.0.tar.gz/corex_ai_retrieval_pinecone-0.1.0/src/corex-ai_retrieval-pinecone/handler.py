# Handler for pinecone implementing ai_retrieval interface
from corex.core.interfaces.ai_retrieval import Ai_retrievalInterface

class PineconeHandler(Ai_retrievalInterface):
    def __init__(self):
        pass

    def example_method(self):
        print("Handling ai_retrieval with pinecone")
