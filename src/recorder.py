import os
import tempfile
import sounddevice as sd
import soundfile as sf  # Usaremos esta biblioteca mais robusta


class AudioRecorder:
    """Responsável por gravar áudio do microfone."""

    def __init__(self, sample_rate=16000, chunk_duration=5):
        self.sample_rate = sample_rate
        self.chunk_duration = chunk_duration
        self.temp_file_path = tempfile.mkstemp(suffix=".wav")[1]

    def record_chunk(self):
        """Grava um trecho de áudio e salva em um ficheiro temporário."""
        num_samples = int(self.chunk_duration * self.sample_rate)

        # Grava o áudio. dtype='float32' é um formato padrão e bem suportado.
        recording = sd.rec(num_samples, samplerate=self.sample_rate, channels=1, dtype='float32')
        sd.wait()

        # Salva o áudio gravado usando soundfile, que é mais confiável
        try:
            sf.write(self.temp_file_path, recording, self.sample_rate)
            return self.temp_file_path
        except Exception as e:
            print(f"Erro ao salvar o arquivo de áudio: {e}")
            return None

    def cleanup(self):
        """Remove o ficheiro de áudio temporário."""
        if os.path.exists(self.temp_file_path):
            try:
                os.remove(self.temp_file_path)
                print("Arquivo temporário de áudio removido.")
            except Exception as e:
                print(f"Erro ao remover arquivo temporário: {e}")

