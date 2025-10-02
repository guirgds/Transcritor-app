import tkinter as tk
import threading
import whisper
import sounddevice as sd
from pynput.keyboard import Controller
import numpy as np
import tempfile
import os
from scipy.io.wavfile import write as write_wav

# --- Configurações ---
MODELO_WHISPER = "base"
TAXA_AMOSTRAGEM = 16000
TEMPO_GRAVACAO_CHUNK = 5
ARQUIVO_TEMP = tempfile.mkstemp(suffix=".wav")[1]

# --- Variáveis Globais de Controle ---
is_recording = False
stop_event = threading.Event()
keyboard = Controller()
model = None

# --- Funções Principais ---
def type_text(text):
    print(f"Digitando: {text}")
    keyboard.type(text)

def record_and_transcribe():
    global model
    if model is None:
        print(f"Carregando o modelo Whisper '{MODELO_WHISPER}'...")
        status_label.config(text=f"Carregando modelo '{MODELO_WHISPER}'...")
        try:
            model = whisper.load_model(MODELO_WHISPER)
            print("Modelo carregado com sucesso.")
            status_label.config(text="Modelo carregado. Pronto para gravar.")
        except Exception as e:
            print(f"Erro ao carregar o modelo: {e}")
            status_label.config(text=f"Erro ao carregar modelo.")
            toggle_recording()
            return

    while is_recording:
        status_label.config(text="Gravando...")
        print("Iniciando gravação de um trecho...")
        recording = sd.rec(int(TEMPO_GRAVACAO_CHUNK * TAXA_AMOSTRAGEM), samplerate=TAXA_AMOSTRAGEM, channels=1, dtype='int16')
        sd.wait()

        if not is_recording:
            break

        print("Gravação do trecho finalizada. Transcrevendo...")
        status_label.config(text="Processando...")
        write_wav(ARQUIVO_TEMP, TAXA_AMOSTRAGEM, recording)

        try:
            result = model.transcribe(ARQUIVO_TEMP, fp16=False)
            transcribed_text = result['text']
            if transcribed_text:
                type_text(" " + transcribed_text.strip())
        except Exception as e:
            print(f"Ocorreu um erro durante a transcrição: {e}")

    print("Thread de gravação finalizada.")
    status_label.config(text="Clique para iniciar.")

def toggle_recording():
    global is_recording
    if is_recording:
        is_recording = False
        stop_event.set()
        record_button.config(text="Iniciar Gravação", bg="green")
        status_label.config(text="Clique para iniciar.")
        print("Parando gravação.")
    else:
        is_recording = True
        stop_event.clear()
        record_button.config(text="Parar Gravação", bg="red")
        thread = threading.Thread(target=record_and_transcribe)
        thread.daemon = True
        thread.start()

# --- Configuração da Interface Gráfica (GUI) ---
root = tk.Tk()
root.title("Transcritor Local")
root.geometry("250x120")
root.attributes('-topmost', True)

frame = tk.Frame(root, padx=10, pady=10)
frame.pack(expand=True, fill=tk.BOTH)

status_label = tk.Label(frame, text="Clique para iniciar.", wraplength=230)
status_label.pack(pady=(0, 10))

record_button = tk.Button(frame, text="Iniciar Gravação", command=toggle_recording, bg="green", fg="white", font=("Helvetica", 10, "bold"))
record_button.pack(pady=5, fill=tk.X)

try:
    root.mainloop()
finally:
    if os.path.exists(ARQUIVO_TEMP):
        os.remove(ARQUIVO_TEMP)
    print("Aplicativo fechado e arquivo temporário removido.")