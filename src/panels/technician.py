from textual import on
from textual.app import ComposeResult
from textual.widgets import Input, Button, Label, Rule
from textual.containers import Vertical
from panels.base_screen import BaseScreen
from panels.popup import PopupScreen

class TechnicianScreen(BaseScreen):
    BINDINGS = [("escape", "app.pop_screen", "Close screen")]

    def compose(self) -> ComposeResult:
        yield from super().compose() # This gets header/sidebar/footer
        with Vertical(id="login-content"):
            yield Label("Technicians")
            yield Button("New Technician", id="new", variant="primary")
            yield Button("Edit Technician", id="edit", variant="primary")
    
    @on(Button.Pressed, "#new")
    def new_technician(self):
        self.app.pop_screen()
        self.app.push_screen(NewTechnicianScreen())

    @on(Button.Pressed, "#edit")
    def edit_technician(self):
        self.app.pop_screen()
        self.app.push_screen(NewTechnicianScreen())

class NewTechnicianScreen(BaseScreen):
    BINDINGS = [("escape", "app.pop_screen", "Close screen")]

    def compose(self) -> ComposeResult:
        yield from super().compose()
        with Vertical(id="login-content"):
            yield Label("Create Technician")
            yield Rule(line_style="heavy")
            yield Label("Name")
            yield Input(placeholder="Name", id="name-input")
            yield Label("Username")
            yield Input(placeholder="Username", id="username-input")
            yield Label("Email")
            yield Input(placeholder="Email", id="email-input")
            yield Button("Create", id="create", variant="primary", disabled=True)
            yield Button("Cancel", id="cancel", variant="error")
    
    @on(Input.Changed)
    def check_valid(self) -> None:
        if (self.query_one("#name-input", Input).value and 
            self.query_one("#username-input", Input).value and 
            self.query_one("#email-input", Input).value):
            self.query_one("#create", Button).disabled = False
        else:
            self.query_one("#create", Button).disabled = True
    
    @on(Button.Pressed, "#create")
    def create_technician(self):
        name = self.query_one("#name-input", Input).value
        username = self.query_one("#username-input", Input).value
        email = self.query_one("#email-input", Input).value
        self.app.manager.technicians.create_technician(name, username, email)
        self.app.push_screen(PopupScreen(f"Technician {name} created!"))
        

    @on(Button.Pressed, "#cancel")
    def close_screen(self):
        self.app.pop_screen()