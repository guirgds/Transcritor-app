import sounddevice as sd
import numpy as np


class AudioRecorder:
    """Responsável por gravar áudio do microfone diretamente para a memória."""

    def __init__(self, sample_rate=16000, chunk_duration=5):
        self.sample_rate = sample_rate
        self.chunk_duration = chunk_duration
        self._list_audio_devices()  # Diagnóstico ao iniciar

    def _list_audio_devices(self):
        """Lista os dispositivos de áudio disponíveis para diagnóstico."""
        print("\n--- Dispositivos de Áudio Disponíveis ---")
        try:
            print(sd.query_devices())
            print("------------------------------------------\n")
        except Exception as e:
            print(f"Não foi possível listar os dispositivos de áudio: {e}")

    def record_chunk(self):
        """Grava um trecho de áudio e o retorna como um array numpy."""
        num_samples = int(self.chunk_duration * self.sample_rate)

        try:
            print("--- Gravando trecho para a memória... ---")
            recording = sd.rec(num_samples, samplerate=self.sample_rate, channels=1, dtype='float32')
            sd.wait()

            # Verifica se a gravação contém algo além de silêncio
            if np.max(np.abs(recording)) < 0.01: # Usamos um limiar pequeno em vez de zero
                print("!!!!!! AVISO: O microfone não captou som (gravação está em silêncio). !!!!!!")
                return None # Retorna None se não houver som

            return recording.flatten() # Retorna o array de áudio diretamente

        except Exception as e:
            print(f"!!!!!! ERRO AO GRAVAR O ÁUDIO: {e} !!!!!!")
            return None

    def cleanup(self):
        """Não faz nada, pois não há ficheiros para limpar."""
        pass

