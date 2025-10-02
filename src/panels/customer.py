from textual import on
from textual.app import ComposeResult
from textual.widgets import Input, Button, Label, Rule, ListView, ListItem, Checkbox
from textual.containers import Vertical, Horizontal
from panels.base_screen import BaseScreen
from panels.popup import PopupScreen, PopupType

class CustomerScreen(BaseScreen):
    BINDINGS = [("escape", "app.pop_screen", "Close screen")]

    def compose(self) -> ComposeResult:
        yield from super().compose() # This gets header/sidebar/footer
        with Vertical(id="login-content"):
            yield Label("Customers")
            yield Button("New Customer", id="new", variant="primary")
            yield Button("Edit Customer", id="edit", variant="primary")
    
    @on(Button.Pressed, "#new")
    def new_technician(self):
        self.app.pop_screen()
        self.app.push_screen(NewCustomerScreen())

    @on(Button.Pressed, "#edit")
    def edit_technician(self):
        self.app.pop_screen()
        self.app.push_screen(NewCustomerScreen()) # Change to EditCustomerScreen when implemented

class NewCustomerScreen(BaseScreen):
    BINDINGS = [("escape", "app.pop_screen", "Close screen")]

    def compose(self) -> ComposeResult:
        yield from super().compose()
        with Vertical(id="login-content"):
            yield Label("Create Customer")
            yield Rule(line_style="heavy")
            yield Label("Customer Code")
            yield Input(placeholder="Customer Code", id="code-input")
            yield Label("Name")
            yield Input(placeholder="Name", id="name-input")
            yield Label("Phone Number")
            yield Input(placeholder="Phone Number", id="phone-input")
            yield Label("Email")
            yield Input(placeholder="Email", id="email-input")
            yield Label("Address")
            yield Input(placeholder="Address", id="address-input")
            yield Checkbox("Business", id="is_business")
            yield Button("Create", id="create", variant="primary", disabled=True)
            yield Button("Cancel", id="cancel", variant="error")
    
    @on(Input.Changed)
    def check_valid(self) -> None:
        # Email and Address are not required
        if (self.query_one("#code-input", Input).value and 
            self.query_one("#name-input", Input).value and 
            self.query_one("#phone-input", Input).value):
            self.query_one("#create", Button).disabled = False
        else:
            self.query_one("#create", Button).disabled = True
    
    @on(Button.Pressed, "#create")
    def create_technician(self):
        code = self.query_one("#code-input", Input).value
        name = self.query_one("#name-input", Input).value
        phone = self.query_one("#phone-input", Input).value
        email = self.query_one("#email-input", Input).value
        address = self.query_one("#address-input", Input).value
        is_business = self.query_one("#is_business", Checkbox).value
        try:
            self.app.manager.customers.create_customer(code, name, phone, email, address, is_business)
            self.app.push_screen(PopupScreen(f"Customer {name} created!", PopupType.SUCCESS))
        except Exception as e:
            self.app.push_screen(PopupScreen(f"Error: {e}", PopupType.ERROR))
        

    @on(Button.Pressed, "#cancel")
    def close_screen(self):
        self.app.pop_screen()