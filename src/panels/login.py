from textual.app import ComposeResult
from textual.widgets import Input, Button
from textual.containers import Vertical
from panels.base_screen import BaseScreen

class LoginScreen(BaseScreen):
    BINDINGS = [("escape", "app.pop_screen", "Close screen")]

    def compose(self) -> ComposeResult:
        yield from super().compose() # This gets header/sidebar/footer
        with Vertical(id="login-content"):
            yield Input(placeholder="Username")
            yield Button("Login")