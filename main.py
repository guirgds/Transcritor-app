import os
import sys
from src.app import TranscriberApp


def setup_environment():
    """
    Adiciona os diretórios 'Library\\bin' e 'Scripts' do ambiente Conda
    ao PATH do sistema. Isto é crucial para que a biblioteca whisper
    encontre o ffmpeg.exe e outras ferramentas.
    """
    if not hasattr(sys, 'executable'):
        print("Não foi possível determinar o caminho do executável do Python.")
        return

    # sys.executable é o caminho para o python.exe do ambiente atual
    env_path = os.path.dirname(sys.executable)

    # Caminhos onde o Conda pode instalar executáveis como o ffmpeg.exe
    paths_to_add = [
        os.path.join(env_path, 'Scripts'),
        os.path.join(env_path, 'Library', 'bin')
    ]

    current_path = os.environ.get("PATH", "")

    for path in paths_to_add:
        if os.path.isdir(path) and path not in current_path:
            print(f"Adicionando ao PATH do sistema: {path}")
            os.environ["PATH"] = path + os.pathsep + os.environ["PATH"]
        else:
            print(f"O caminho '{path}' já está no PATH ou não foi encontrado.")


if __name__ == "__main__":
    # Primeiro, configuramos o ambiente para encontrar as nossas ferramentas
    setup_environment()

    # Depois, iniciamos a aplicação
    app = TranscriberApp()
    app.run()
