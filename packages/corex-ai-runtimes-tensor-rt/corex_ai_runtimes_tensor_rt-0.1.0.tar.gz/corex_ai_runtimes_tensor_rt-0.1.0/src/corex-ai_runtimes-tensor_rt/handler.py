# Handler for tensor_rt implementing ai_runtimes interface
from corex.core.interfaces.ai_runtimes import Ai_runtimesInterface

class Tensor_rtHandler(Ai_runtimesInterface):
    def __init__(self):
        pass

    def example_method(self):
        print("Handling ai_runtimes with tensor_rt")
