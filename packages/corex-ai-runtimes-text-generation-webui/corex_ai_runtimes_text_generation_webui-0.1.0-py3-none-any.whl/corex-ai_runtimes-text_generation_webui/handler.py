# Handler for text_generation_webui implementing ai_runtimes interface
from corex.core.interfaces.ai_runtimes import Ai_runtimesInterface

class Text_generation_webuiHandler(Ai_runtimesInterface):
    def __init__(self):
        pass

    def example_method(self):
        print("Handling ai_runtimes with text_generation_webui")
