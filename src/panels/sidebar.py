from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widget import Widget
from textual.widgets import Button

class Sidebar(Widget):
    def compose(self) -> ComposeResult:
        with Vertical(id="sidebar"):
            yield Button("New Ticket", id="new", variant="primary")
            yield Button("Edit Ticket", id="edit", variant="primary")
            yield Button("Login", id="login", variant="success")
            yield Button("Exit", id="exit", variant="error")
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "exit":
            self.app.exit()
        elif event.button.id == "login":
            from panels.login import LoginScreen # Import here to avoid circular import issue.
            # don't push LoginScreen if we're already on it
            if isinstance(self.screen, LoginScreen):
                return
            # Comment on next line ignores pylance/vscode error since the code works
            self.screen.show_sidebar = False  # type: ignore[attr-defined]
            self.app.push_screen(LoginScreen())