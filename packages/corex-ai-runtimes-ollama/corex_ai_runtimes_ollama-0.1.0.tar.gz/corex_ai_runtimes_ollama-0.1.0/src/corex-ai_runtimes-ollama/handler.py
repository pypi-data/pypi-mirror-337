# Handler for ollama implementing ai_runtimes interface
from corex.core.interfaces.ai_runtimes import Ai_runtimesInterface

class OllamaHandler(Ai_runtimesInterface):
    def __init__(self):
        pass

    def example_method(self):
        print("Handling ai_runtimes with ollama")
