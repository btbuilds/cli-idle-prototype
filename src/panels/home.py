from textual.app import ComposeResult
from textual.widgets import Static
from art import text2art
from panels.base_screen import BaseScreen

class HomeScreen(BaseScreen):
    def compose(self) -> ComposeResult:
        yield from super().compose()  # This gets header/sidebar/footer
        logo = str(text2art("Ticket RPG", font="cybermedium")) # This already returns a string, but pylance complains about it otherwise.
        yield Static(content=logo, id="main-content")