from textual import on
from textual.app import ComposeResult
from textual.widgets import Input, Button, Label, Rule, ListView, ListItem, RadioButton, RadioSet
from textual.containers import Vertical, Horizontal
from panels.base_screen import BaseScreen
from panels.popup import PopupScreen, PopupType

class TechnicianScreen(BaseScreen):
    BINDINGS = [("escape", "app.pop_screen", "Close screen")]
    CSS_PATH = "../style/technician.tcss"

    def compose(self) -> ComposeResult:
        yield from super().compose() # This gets header/sidebar/footer
        with Vertical(id="form-content"):
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
        self.app.push_screen(EditTechnicianScreen())

class NewTechnicianScreen(BaseScreen):
    BINDINGS = [("escape", "app.pop_screen", "Close screen")]
    CSS_PATH = "../style/newtech.tcss"

    def compose(self) -> ComposeResult:
        yield from super().compose()
        with Vertical(id="form-content"):
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
        try:
            self.app.manager.technicians.create_technician(name, username, email)
            self.app.push_screen(PopupScreen(f"Technician {name} created!", PopupType.SUCCESS))
        except Exception as e:
            self.app.push_screen(PopupScreen(f"Error: {e}", PopupType.ERROR))
        

    @on(Button.Pressed, "#cancel")
    def close_screen(self):
        self.app.pop_screen()

class EditTechnicianScreen(BaseScreen):
    BINDINGS = [("escape", "app.pop_screen", "Close screen")]
    CSS_PATH = "../style/edittech.tcss"

    def compose(self) -> ComposeResult:
        yield from super().compose()
        
        with Horizontal(id="edit-tech-content"):
            # Left side - list of technicians
            with Vertical(id="tech-list-container"):
                yield Label("Select Technician")
                yield ListView(id="tech-list")
            
            # Right side - edit form
            with Vertical(id="tech-edit-form"):
                yield Label("Name:")
                yield Input(id="tech-name", placeholder="Name")
                yield Label("Username:")
                yield Input(id="tech-username", placeholder="Username")
                yield Label("Email:")
                yield Input(id="tech-email", placeholder="Email")
                with RadioSet(id="is-active"):
                    yield RadioButton("Active", id="active")
                    yield RadioButton("Inactive", id="inactive")
                yield Button("Save", id="save-tech", variant="success")
    
    def on_mount(self) -> None:
        self.load_technicians()
        self.current_tech_id = None
    
    def load_technicians(self):
        """Load all technicians into the list"""
        tech_list = self.query_one("#tech-list", ListView)
        techs = self.app.manager.technicians.list_technicians()

        for tech in techs:
            item = ListItem(Label(f"{tech.name} ({tech.username})"))
            item.tech_id = tech.id # type: ignore[attr-defined]
            tech_list.append(item)
    
    @on(ListView.Selected, "#tech-list")
    def select_tech(self, event: ListView.Selected) -> None:
        selected_item = event.item
        tech_id = selected_item.tech_id # type: ignore[attr-defined]

        tech = self.app.manager.technicians.find_by_id(tech_id)

        if tech:
            self.current_tech_id = tech.id
            # Update the form fields
            self.query_one("#tech-name", Input).value = tech.name
            self.query_one("#tech-username", Input).value = tech.username
            self.query_one("#tech-email", Input).value = tech.email
            if tech.is_active:
                self.query_one("RadioSet #active", RadioButton).value = True
            else:
                self.query_one("RadioSet #inactive", RadioButton).value = True
    
    @on(Button.Pressed, "#save-tech")
    def save_technician(self):
        """Save the edited technician"""
        if not self.current_tech_id:
            return  # No tech selected
        
        name = self.query_one("#tech-name", Input).value
        username = self.query_one("#tech-username", Input).value
        email = self.query_one("#tech-email", Input).value
        is_active = self.query_one("RadioSet #active", RadioButton).value

        try:
            self.app.manager.technicians.update_technician(self.current_tech_id, name, username, email, is_active)
            self.app.push_screen(PopupScreen(f"Technician {name} updated!", PopupType.SUCCESS))
        except Exception as e:
            self.app.push_screen(PopupScreen(f"Error: {e}", PopupType.ERROR))