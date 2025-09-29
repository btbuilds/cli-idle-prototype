from __future__ import annotations
from typing import TYPE_CHECKING

from textual.screen import Screen
from textual.app import ComposeResult
from textual.reactive import reactive
from textual.widgets import Header, Footer
from panels.sidebar import Sidebar

if TYPE_CHECKING:
    from main import TicketRPGApp

class BaseScreen(Screen):
    @property
    def app(self) -> "TicketRPGApp":
        """Get the app instance with proper typing"""
        return super().app  # type: ignore
    
    show_sidebar = reactive(False)
    BINDINGS = [("s", "toggle_sidebar", "Toggle Sidebar")]
    
    def compose(self) -> ComposeResult:
        yield Header()
        yield Sidebar()
        yield Footer()
        # Subclasses add their content
    
    def action_toggle_sidebar(self) -> None:
        self.show_sidebar = not self.show_sidebar
    
    def watch_show_sidebar(self, show_sidebar: bool) -> None:
        self.query_one(Sidebar).set_class(show_sidebar, "-visible")