# Handler for llama_index implementing ai_retrieval interface
from corex.core.interfaces.ai_retrieval import Ai_retrievalInterface

class Llama_indexHandler(Ai_retrievalInterface):
    def __init__(self):
        pass

    def example_method(self):
        print("Handling ai_retrieval with llama_index")
