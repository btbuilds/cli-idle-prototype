from textual.app import ComposeResult
from textual.widgets import Static
from panels.base_screen import BaseScreen

class HomeScreen(BaseScreen):
    def compose(self) -> ComposeResult:
        yield from super().compose()  # This gets header/sidebar/footer
        yield Static("Home Content", id="main-content")