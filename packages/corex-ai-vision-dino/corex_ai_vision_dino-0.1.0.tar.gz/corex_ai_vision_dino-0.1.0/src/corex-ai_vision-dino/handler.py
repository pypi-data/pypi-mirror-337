# Handler for dino implementing ai_vision interface
from corex.core.interfaces.ai_vision import Ai_visionInterface

class DinoHandler(Ai_visionInterface):
    def __init__(self):
        pass

    def example_method(self):
        print("Handling ai_vision with dino")
