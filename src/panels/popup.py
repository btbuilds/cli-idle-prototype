from textual import on
from textual.app import ComposeResult
from textual.widgets import Button, Label
from textual.containers import Vertical
from textual.screen import ModalScreen

class PopupScreen(ModalScreen):
    def __init__(self, message: str):
        super().__init__()
        self.message = message

    def compose(self) -> ComposeResult:
        with Vertical(id="popup"):
            yield Label(content=self.message)
            yield Button("Close", id="close", variant="success")
    
    @on(Button.Pressed, "#close")
    def close_screen(self):
        self.app.pop_screen()
        self.app.pop_screen()