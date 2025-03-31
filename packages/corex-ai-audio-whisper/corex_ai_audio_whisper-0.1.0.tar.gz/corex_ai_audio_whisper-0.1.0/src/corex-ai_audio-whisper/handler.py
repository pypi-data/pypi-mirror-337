# Handler for whisper implementing ai_audio interface
from corex.core.interfaces.ai_audio import Ai_audioInterface

class WhisperHandler(Ai_audioInterface):
    def __init__(self):
        pass

    def example_method(self):
        print("Handling ai_audio with whisper")
