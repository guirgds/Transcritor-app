from PIL import Image, ImageDraw
import pystray
from pystray import MenuItem


class TrayIcon:
    """Gere o ícone e o menu na bandeja do sistema."""

    def __init__(self, toggle_callback, exit_callback):
        self._toggle_callback = toggle_callback
        self._exit_callback = exit_callback
        self._icon = self._setup_icon()

    @staticmethod
    def _create_icon_image(color):
        """Cria uma imagem de ícone simples com uma cor."""
        width = 64
        height = 64
        image = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        draw.ellipse((0, 0, width - 1, height - 1), fill=color, outline='black')
        return image

    def _on_toggle(self, _icon, _menu_item):
        """Função chamada pelo menu para iniciar/parar a gravação."""
        self._toggle_callback()

    def _on_exit(self, _icon, _menu_item):
        """Função chamada pelo menu para sair da aplicação."""
        self._exit_callback()

    def _setup_icon(self):
        """Cria e configura o objeto do ícone."""
        menu = (
            MenuItem('Iniciar/Parar Gravação', self._on_toggle, default=True),
            MenuItem('Sair', self._on_exit)
        )
        image = self._create_icon_image('green')
        icon = pystray.Icon("Transcritor", image, "Transcritor (Inativo)", menu)
        return icon

    def update_icon(self, is_recording):
        """Atualiza a cor e o título do ícone com base no estado."""
        if is_recording:
            self._icon.icon = self._create_icon_image('red')
            self._icon.title = "Transcritor (Gravando)"
        else:
            self._icon.icon = self._create_icon_image('green')
            self._icon.title = "Transcritor (Inativo)"

    def set_title(self, title):
        """Define o texto que aparece ao passar o rato por cima do ícone."""
        if self._icon:
            self._icon.title = title

    def run(self):
        """Mostra o ícone e inicia o loop da aplicação."""
        print("App iniciado. Procure o ícone na bandeja do sistema.")
        self._icon.run()

    def stop(self):
        """Para o ícone."""
        self._icon.stop()

