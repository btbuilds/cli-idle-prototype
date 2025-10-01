from enum import Enum
from textual import on
from textual.app import ComposeResult
from textual.widgets import Button, Label
from textual.containers import Vertical
from textual.screen import ModalScreen

class PopupType(Enum):
    ERROR = "error"
    SUCCESS = "success"

class PopupScreen(ModalScreen):
    def __init__(self, message: str, type: PopupType):
        super().__init__()
        self.message = message
        self.type = type

    def compose(self) -> ComposeResult:
        popup_classes = "popup-error" if self.type == PopupType.ERROR else "popup-success"
        with Vertical(id="popup", classes=popup_classes):
            yield Label(content=self.message)
            yield Button("Close", id="close", variant="success")
    
    @on(Button.Pressed, "#close")
    def close_screen(self):
        if self.type == PopupType.SUCCESS:
            self.app.pop_screen() # Close the modal
            self.app.pop_screen() # Close the screen we were on
        elif self.type == PopupType.ERROR:
            self.app.pop_screen() # Close only the modal