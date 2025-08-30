from textual.app import App, ComposeResult
from textual.containers import HorizontalGroup, VerticalScroll, Vertical
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Footer, Header, ListView, Button, ListItem


class Sidebar(Widget):
    """
    Our sidebar widget.

    Add desired content to compose()

    """
    def compose(self) -> ComposeResult:
        with Vertical():
            yield Button("New Ticket", id="new", variant="primary")
            yield Button("Edit Ticket", id="edit", variant="primary")
            yield Button("Exit", id="exit", variant="error")
    
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "exit":
            self.app.exit()


class TicketRPGApp(App):
    """A Textual app."""

    BINDINGS = [("s", "toggle_sidebar", "Toggle Sidebar")]

    show_sidebar = reactive(False)

    CSS_PATH = "style/main_menu.tcss"

    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Sidebar()
        yield Header()
        yield Footer()
        
    
    def on_mount(self) -> None:
        """Set Title"""
        self.title = "Ticket RPG"
        self.sub_title = "Earn XP while working!"

        """Set Theme"""
        self.theme = "monokai"
    
    def action_toggle_sidebar(self) -> None:
        """Toggle the sidebar visibility."""
        self.show_sidebar = not self.show_sidebar

    def watch_show_sidebar(self, show_sidebar: bool) -> None:
        """Set or unset visible class when reactive changes."""
        self.query_one(Sidebar).set_class(show_sidebar, "-visible")


if __name__ == "__main__":
    app = TicketRPGApp()
    app.run()