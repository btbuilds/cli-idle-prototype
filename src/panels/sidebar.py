from textual import on
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widget import Widget
from textual.widgets import Button

class Sidebar(Widget):
    def compose(self) -> ComposeResult:
        with Vertical(id="sidebar"):
            yield Button("New Ticket", id="new", variant="primary")
            yield Button("Edit Ticket", id="edit", variant="primary")
            yield Button("Account", id="account", variant="success")
            yield Button("Exit", id="exit", variant="error")
    
    @on(Button.Pressed, "#account")
    def push_account(self) -> None:
        from panels.account import AccountScreen # Import here to avoid circular import issue.
        # Comment on next line ignores pylance/vscode error since the code works
        self.screen.show_sidebar = False  # type: ignore[attr-defined]
        self.app.push_screen(AccountScreen())
    
    @on(Button.Pressed, "#exit")
    def quit_button(self) -> None:
        self.app.exit()