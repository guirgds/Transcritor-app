import threading
from .recorder import AudioRecorder
from .transcriber import WhisperTranscriber
from .tray_icon import TrayIcon


class TranscriberApp:
    """Orquestra a aplicação inteira."""

    def __init__(self):
        self.is_recording = False
        self.recorder = AudioRecorder()
        self.transcriber = WhisperTranscriber()
        self.tray_icon = TrayIcon(self.toggle_recording, self.exit_app)
        self.recording_thread = None

    def toggle_recording(self):
        """Inicia ou para a gravação."""
        self.is_recording = not self.is_recording
        self.tray_icon.update_icon(self.is_recording)

        if self.is_recording:
            # Inicia a gravação e transcrição em uma nova thread
            self.recording_thread = threading.Thread(target=self.recording_loop, daemon=True)
            self.recording_thread.start()

    def recording_loop(self):
        """Loop principal de gravação e transcrição."""
        # Carrega o modelo apenas quando a gravação começa
        self.tray_icon.set_title("Carregando modelo...")
        self.transcriber.load_model()
        self.tray_icon.set_title("Transcritor (Gravando)")

        while self.is_recording:
            audio_data = self.recorder.record_chunk()

            if not self.is_recording:
                break

            # Passa os dados de áudio diretamente, sem usar um ficheiro
            if audio_data is not None:
                print("Transcrevendo trecho...")
                self.transcriber.transcribe_audio(audio_data)

        print("Loop de gravação finalizado.")

    def exit_app(self):
        """Encerra a aplicação de forma limpa."""
        print("Fechando a aplicação...")
        self.is_recording = False
        # A função cleanup não é mais necessária, mas mantemo-la por uma questão de estrutura
        self.recorder.cleanup()
        self.tray_icon.stop()

    def run(self):
        """Inicia a aplicação."""
        self.tray_icon.run()

