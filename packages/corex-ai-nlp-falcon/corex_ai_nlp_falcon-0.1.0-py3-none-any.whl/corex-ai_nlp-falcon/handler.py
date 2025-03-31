# Handler for falcon implementing ai_nlp interface
from corex.core.interfaces.ai_nlp import Ai_nlpInterface

class FalconHandler(Ai_nlpInterface):
    def __init__(self):
        pass

    def example_method(self):
        print("Handling ai_nlp with falcon")
