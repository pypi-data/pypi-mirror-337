# Handler for weaviate implementing ai_embeddings interface
from corex.core.interfaces.ai_embeddings import Ai_embeddingsInterface

class WeaviateHandler(Ai_embeddingsInterface):
    def __init__(self):
        pass

    def example_method(self):
        print("Handling ai_embeddings with weaviate")
