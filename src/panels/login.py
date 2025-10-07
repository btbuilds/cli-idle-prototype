from textual import on
from textual.app import ComposeResult
from textual.widgets import Input, Button, Label
from textual.containers import Vertical
from panels.base_screen import BaseScreen
from panels.popup import PopupScreen, PopupType

class LoginScreen(BaseScreen):
    BINDINGS = [("escape", "app.pop_screen", "Close screen")]

    def compose(self) -> ComposeResult:
        yield from super().compose() # This gets header/sidebar/footer
        with Vertical(id="form-content"):
            yield Label("Login")
            yield Input(placeholder="Username", id="username-input")
            yield Button("Login", id="login", variant="primary")
    
    @on(Button.Pressed, "#login")
    @on(Input.Submitted, "#username-input")
    def handle_login(self):
        username = self.query_one("#username-input", Input).value
        tech = self.app.manager.technicians.login(username)
        
        if tech and tech.is_active:
            self.app.login_user(tech)  # Pass the Technician object
            self.app.push_screen(PopupScreen("Login successful!", PopupType.SUCCESS))
        elif tech and not tech.is_active: 
            self.app.push_screen(PopupScreen("Error: Username is not active!", PopupType.ERROR))
        else:
            self.app.push_screen(PopupScreen("Error: Username does not exist!", PopupType.ERROR))