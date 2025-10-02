import whisper
from pynput.keyboard import Controller
import numpy as np


class WhisperTranscriber:
    """Responsável por carregar o modelo e transcrever dados de áudio da memória."""

    def __init__(self, model_name="base"):
        self.model_name = model_name
        self.model = None
        self.keyboard = Controller()

    def load_model(self):
        """Carrega o modelo Whisper. Executado apenas uma vez."""
        if self.model is None:
            print(f"Carregando modelo Whisper '{self.model_name}'...")
            try:
                self.model = whisper.load_model(self.model_name)
                print("Modelo carregado com sucesso.")
            except Exception as e:
                print(f"Falha ao carregar o modelo: {e}")
                raise e

    def transcribe_audio(self, audio_data: np.ndarray):
        """Transcreve um array de áudio numpy e digita o texto."""
        if audio_data is None:
            print("Nenhum dado de áudio para transcrever.")
            return

        if self.model is None:
            print("Erro: Modelo não carregado. Chame load_model() primeiro.")
            return

        try:
            # O Whisper pode transcrever o array numpy diretamente
            result = self.model.transcribe(audio_data, fp16=False)
            transcribed_text = result.get('text', '').strip()

            if transcribed_text:
                self._type_text(transcribed_text)
            else:
                print("Nenhum texto detectado na transcrição.")

        except Exception as e:
            print(f"Ocorreu um erro durante a transcrição: {e}")

    def _type_text(self, text):
        """Digita o texto no local do cursor."""
        print(f"Digitando: {text}")
        self.keyboard.type(" " + text)

