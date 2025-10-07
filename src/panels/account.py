from textual import on
from textual.app import ComposeResult
from textual.widgets import Input, Button, Label
from textual.containers import Vertical
from panels.base_screen import BaseScreen

class AccountScreen(BaseScreen):
    BINDINGS = [("escape", "app.pop_screen", "Close screen")]

    def compose(self) -> ComposeResult:
        yield from super().compose() # This gets header/sidebar/footer
        with Vertical(id="form-content"):
            yield Button("Login", id="login", variant="primary")
            yield Button("Logout", id="logout", variant="primary", disabled=True)
        

    def on_mount(self) -> None:
        self.check_button_state()
    
    @on(Button.Pressed, "#login")
    def push_login(self):
        from panels.login import LoginScreen # Import here to avoid circular import issue.
        # Comment on next line ignores pylance/vscode error since the code works
        self.screen.show_sidebar = False  # type: ignore[attr-defined]
        self.app.pop_screen()
        self.app.push_screen(LoginScreen())
    
    @on(Button.Pressed, "#logout")
    def logout(self):
        self.app.logout_user()
        self.check_button_state()

    def check_button_state(self):
        if self.app.current_technician:
            self.query_one("#login", Button).disabled = True
            self.query_one("#logout", Button).disabled = False
        else:
            self.query_one("#login", Button).disabled = False
            self.query_one("#logout", Button).disabled = True