from textual import on
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widget import Widget
from textual.widgets import Button
from panels.popup import PopupScreen, PopupType

class Sidebar(Widget):
    def compose(self) -> ComposeResult:
        with Vertical(id="sidebar"):
            yield Button("Tickets", id="tickets", variant="primary")
            yield Button("Customers", id="customers", variant="primary")
            yield Button("Technicians", id="technicians", variant="primary")
            yield Button("Account", id="account", variant="success")
            yield Button("Exit", id="exit", variant="error")
    
    @on(Button.Pressed, "#tickets")
    def push_tickets(self) -> None:
        if not self.app.current_technician: # type: ignore[attr-defined]
            self.app.push_screen(PopupScreen(f"Error: Must be logged in.", PopupType.ERROR))
            return
        from panels.ticket import TicketScreen # Import here to avoid circular import issue.
        # Comment on next line ignores pylance/vscode error since the code works
        self.screen.show_sidebar = False  # type: ignore[attr-defined]
        self.app.push_screen(TicketScreen())
    
    @on(Button.Pressed, "#customers")
    def push_customers(self) -> None:
        if not self.app.current_technician: # type: ignore[attr-defined]
            self.app.push_screen(PopupScreen(f"Error: Must be logged in.", PopupType.ERROR))
            return
        from panels.customer import CustomerScreen # Import here to avoid circular import issue.
        # Comment on next line ignores pylance/vscode error since the code works
        self.screen.show_sidebar = False  # type: ignore[attr-defined]
        self.app.push_screen(CustomerScreen())

    @on(Button.Pressed, "#account")
    def push_account(self) -> None:
        from panels.account import AccountScreen # Import here to avoid circular import issue.
        # Comment on next line ignores pylance/vscode error since the code works
        self.screen.show_sidebar = False  # type: ignore[attr-defined]
        self.app.push_screen(AccountScreen())
    
    @on(Button.Pressed, "#technicians")
    def push_technicians(self) -> None:
        if not self.app.current_technician: # type: ignore[attr-defined]
            self.app.push_screen(PopupScreen(f"Error: Must be logged in.", PopupType.ERROR))
            return
        from panels.technician import TechnicianScreen # Import here to avoid circular import issue.
        # Comment on next line ignores pylance/vscode error since the code works
        self.screen.show_sidebar = False  # type: ignore[attr-defined]
        self.app.push_screen(TechnicianScreen())
    
    @on(Button.Pressed, "#exit")
    def quit_button(self) -> None:
        self.app.exit()