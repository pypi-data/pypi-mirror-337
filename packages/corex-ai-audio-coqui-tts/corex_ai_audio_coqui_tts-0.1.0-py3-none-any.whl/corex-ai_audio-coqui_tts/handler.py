# Handler for coqui_tts implementing ai_audio interface
from corex.core.interfaces.ai_audio import Ai_audioInterface

class Coqui_ttsHandler(Ai_audioInterface):
    def __init__(self):
        pass

    def example_method(self):
        print("Handling ai_audio with coqui_tts")
