import whisper
from pynput.keyboard import Controller

class WhisperTranscriber:
    """Responsável por carregar o modelo Whisper e transcrever áudio."""
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
                # Propaga o erro para a classe principal lidar com ele
                raise e

    def transcribe_audio(self, audio_path):
        """Transcreve o ficheiro de áudio e digita o texto."""
        # Adicionada verificação para o caso de a gravação falhar
        if not audio_path:
            print("Caminho do áudio inválido, pulando transcrição.")
            return

        if self.model is None:
            print("Erro: Modelo não carregado. Chame load_model() primeiro.")
            return

        try:
            result = self.model.transcribe(audio_path, fp16=False)
            transcribed_text = result.get('text', '').strip()
            if transcribed_text:
                self._type_text(transcribed_text)
        except Exception as e:
            print(f"Ocorreu um erro durante a transcrição: {e}")

    def _type_text(self, text):
        """Digita o texto no local do cursor."""
        print(f"Digitando: {text}")
        self.keyboard.type(" " + text)

