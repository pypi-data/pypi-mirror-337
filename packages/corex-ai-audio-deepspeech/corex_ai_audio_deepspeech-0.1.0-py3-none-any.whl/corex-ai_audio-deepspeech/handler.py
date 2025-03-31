# Handler for deepspeech implementing ai_audio interface
from corex.core.interfaces.ai_audio import Ai_audioInterface

class DeepspeechHandler(Ai_audioInterface):
    def __init__(self):
        pass

    def example_method(self):
        print("Handling ai_audio with deepspeech")
