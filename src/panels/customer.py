from textual import on
from textual.app import ComposeResult
from textual.widgets import Input, Button, Label, Rule, ListView, ListItem, Checkbox, Select
from textual.containers import Vertical, Horizontal
from panels.base_screen import BaseScreen
from panels.popup import PopupScreen, PopupType
from core.manager import SearchType

class CustomerScreen(BaseScreen):
    BINDINGS = [("escape", "app.pop_screen", "Close screen")]
    CSS_PATH = "../style/customer.tcss"

    def compose(self) -> ComposeResult:
        yield from super().compose() # This gets header/sidebar/footer
        with Vertical(id="form-content"):
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
        self.app.push_screen(EditCustomerScreen())

class NewCustomerScreen(BaseScreen):
    BINDINGS = [("escape", "app.pop_screen", "Close screen")]
    CSS_PATH = "../style/newcustomer.tcss"

    def compose(self) -> ComposeResult:
        yield from super().compose()
        with Vertical(id="form-content"):
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

class EditCustomerScreen(BaseScreen):
    BINDINGS = [("escape", "app.pop_screen", "Close screen")]
    CSS_PATH = "../style/editcustomer.tcss"

    def compose(self) -> ComposeResult:
        yield from super().compose()
        
        with Vertical(id="edit-customer-content"):
            # Search section
            with Horizontal(id="search-section"):
                yield Select(
                    [("Code", "code"), 
                    ("Name", "name"), 
                    ("Email", "email"), 
                    ("Phone", "phone")],
                    id="search-type",
                    value="code"
                )
                yield Input(placeholder="Search...", id="search-input")
                yield Button("Search", id="search-btn", variant="primary")
            
            # Results section
            with Vertical(id="results-section"):
                yield Label("Search Results")
                yield ListView(id="customer-results")
            
            # Edit form section
            with Vertical(id="edit-form-section"):
                yield Label("Edit Customer")
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
                yield Button("Save", id="save-btn", variant="primary")
    
    def on_mount(self) -> None:
        self.current_customer_id = None
        self.query_one("#edit-form-section", Vertical).disabled = True
    
    def search_customers(self):
        """Search for customers that match query and load matches in to list"""
        results_list = self.query_one("#customer-results", ListView)
        results_list.clear()
        query = self.query_one("#search-input", Input).value
        search_type = self.query_one("#search-type", Select).value
        customers = self.app.manager.customers.search_customers(query, SearchType(search_type))

        for customer in customers:
            item = ListItem(Label(f"{customer.name} ({customer.code})"))
            item.customer_id = customer.id # type: ignore[attr-defined]
            results_list.append(item)
    
    @on(Button.Pressed, "#search-btn")
    @on(Input.Submitted, "#search-input")
    def search(self):
        self.search_customers()
    
    @on(Button.Pressed, "#save-btn")
    def save_customer(self):
        if not self.current_customer_id:
            return  # No customer selected
        code = self.query_one("#code-input", Input).value
        name = self.query_one("#name-input", Input).value
        phone = self.query_one("#phone-input", Input).value
        email = self.query_one("#email-input", Input).value
        address = self.query_one("#address-input", Input).value
        is_business = self.query_one("#is_business", Checkbox).value
        try:
            self.app.manager.customers.update_customer(self.current_customer_id, code, name, phone, email, address, is_business)
            self.app.push_screen(PopupScreen(f"Customer {name} saved!", PopupType.SUCCESS))
        except Exception as e:
            self.app.push_screen(PopupScreen(f"Error: {e}", PopupType.ERROR))
    
    @on(ListView.Selected, "#customer-results")
    def select_customer(self, event: ListView.Selected) -> None:
        self.query_one("#edit-form-section", Vertical).disabled = False
        selected_item = event.item
        customer_id = selected_item.customer_id # type: ignore[attr-defined]

        customer = self.app.manager.customers.find_by_id(customer_id)

        if customer:
            self.current_customer_id = customer.id
            # Update the form fields
            self.query_one("#code-input", Input).value = customer.code
            self.query_one("#name-input", Input).value = customer.name
            self.query_one("#phone-input", Input).value = customer.phone
            self.query_one("#email-input", Input).value = customer.email
            self.query_one("#address-input", Input).value = customer.address
            self.query_one("#is_business", Checkbox).value = customer.is_business
        