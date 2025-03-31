# Handler for vllm implementing ai_runtimes interface
from corex.core.interfaces.ai_runtimes import Ai_runtimesInterface

class VllmHandler(Ai_runtimesInterface):
    def __init__(self):
        pass

    def example_method(self):
        print("Handling ai_runtimes with vllm")
