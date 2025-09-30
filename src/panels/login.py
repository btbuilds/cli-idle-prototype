from textual import on
from textual.app import ComposeResult
from textual.widgets import Input, Button, Label
from textual.containers import Vertical, Grid
from textual.screen import ModalScreen
from panels.base_screen import BaseScreen

class LoginScreen(BaseScreen):
    BINDINGS = [("escape", "app.pop_screen", "Close screen")]

    def compose(self) -> ComposeResult:
        yield from super().compose() # This gets header/sidebar/footer
        with Vertical(id="login-content"):
            yield Label("Login")
            yield Label(id="status-label")
            yield Input(placeholder="Username", id="username-input")
            yield Button("Login", id="login", variant="primary")
    
    @on(Button.Pressed, "#login")
    @on(Input.Submitted, "#username-input")
    def handle_login(self):
        username = self.query_one("#username-input", Input).value
        tech = self.app.manager.technicians.login(username)
        
        if tech and tech.is_active:
            self.app.login_user(tech)  # Pass the Technician object
            self.app.push_screen(SuccessPopup())
        elif tech and not tech.is_active:
            self.query_one("#status-label", Label).update(
                "[bold red]Username is not active!"
            )
        else:
            self.query_one("#status-label", Label).update(
                "[bold red]Username does not exist!"
            )

class SuccessPopup(ModalScreen):
    def compose(self) -> ComposeResult:
        # yield Grid(
        #     Label("Are you sure you want to quit?", id="question"),
        #     Button("Quit", variant="error", id="quit"),
        #     Button("Cancel", variant="primary", id="cancel"),
        #     id="dialog",
        # )
        with Vertical(id="successpopup"):
            yield Label("Login successful!")
            yield Button("Close", id="close", variant="success")
    
    @on(Button.Pressed, "#close")
    def close_screen(self):
        self.app.pop_screen()
        self.app.pop_screen()