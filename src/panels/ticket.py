from textual import on
from textual.app import ComposeResult
from textual.widgets import Input, Button, Label, Rule, ListView, ListItem, Checkbox, Select, TextArea
from textual.containers import Vertical, Horizontal
from panels.base_screen import BaseScreen
from panels.popup import PopupScreen, PopupType
from core.manager import SearchType

class TicketScreen(BaseScreen):
    BINDINGS = [("escape", "app.pop_screen", "Close screen")]
    CSS_PATH = "../style/tickets.tcss"

    def compose(self) -> ComposeResult:
        yield from super().compose() # This gets header/sidebar/footer
        with Vertical(id="form-content"):
            yield Label("Tickets")
            yield Button("New Ticket", id="new", variant="primary")
            yield Button("Edit Ticket", id="edit", variant="primary")
            yield Button("Search Tickets", id="search", variant="primary")
    
    @on(Button.Pressed, "#new")
    def new_ticket(self):
        self.app.pop_screen()
        self.app.push_screen(NewTicketScreen())

    @on(Button.Pressed, "#edit")
    def edit_ticket(self):
        self.app.pop_screen()
        self.app.push_screen(EditTicketScreen())

    @on(Button.Pressed, "#search")
    def search_tickets(self):
        self.app.pop_screen()
        self.app.push_screen(SearchTicketScreen())

class NewTicketScreen(BaseScreen):
    BINDINGS = [("escape", "app.pop_screen", "Close screen")]
    CSS_PATH = "../style/newticket.tcss"

    def compose(self) -> ComposeResult:
        yield from super().compose()
        with Vertical(id="new-ticket-content"):
            yield Label("New Ticket")
            yield Rule(line_style="heavy")
            with Horizontal(classes="two-column"):
                with Vertical():
                    yield Label("Customer Code")
                    with Horizontal():
                        yield Input(placeholder="Customer Code", id="code-input")
                        yield Button("Lookup", id="lookup", variant="primary")
                with Vertical():
                    yield Label("Priority")
                    yield Select(
                    [("1 - High", "1"), 
                    ("2", "2"), 
                    ("3", "3"), 
                    ("4", "4"),
                    ("5 - Low", "5")],
                    id="priority-select",
                    prompt="Priority"
                )
            with Horizontal(classes="two-column"):
                with Vertical():
                    yield Label("Contact Name") # Maybe automatically populate this when a valid customer code is put in
                    yield Input(placeholder="Contact Name", id="name-input")
                with Vertical():
                    yield Label("Phone Number")
                    yield Input(placeholder="Phone Number", id="phone-input")
            yield Label("Problem Description")
            yield TextArea(placeholder="Problem Description...", id="problem-input")
            yield Label("Equipment")
            with Horizontal(id="equipment-row"):
                yield Select(
                    [("Desktop", "desktop"),
                    ("Laptop", "laptop"),
                    ("Printer", "printer"),
                    ("Other", "other")],
                    id=f"eq-type",
                    prompt="Type"
                )
                yield Input(placeholder="Model", id="eq-model")
                yield Input(placeholder="Serial", id="eq-serial")
                yield Input(placeholder="Notes", id="eq-notes")
            yield Button("+ Add Equipment", id="add-equipment", variant="success")
            yield Label("Equipment List")
            yield ListView(id="equipment-container")
            yield Button("Create", id="create", variant="primary", disabled=True)
            yield Button("Cancel", id="cancel", variant="error")
    
    def on_mount(self) -> None:
        self.query_one("#lookup", Button).can_focus = False

    def add_equipment_row(self) -> None:
        pass

    @on(Button.Pressed, "#add-equipment")
    def handle_add_equipment(self) -> None:
        self.add_equipment_row()
    
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
    def create_customer(self):
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