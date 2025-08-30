from textual.app import App, ComposeResult
from textual.reactive import reactive
from textual.widgets import Footer, Header
from panels.sidebar import Sidebar





class TicketRPGApp(App):
    """A Textual app."""
    BINDINGS = [("s", "toggle_sidebar", "Toggle Sidebar")]

    show_sidebar = reactive(False)

    CSS_PATH = "style/style.tcss"

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