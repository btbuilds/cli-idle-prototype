from textual.app import App
from textual.reactive import reactive
from panels.home import HomeScreen
from core.manager import TicketSystemManager

class TicketRPGApp(App):
    CSS_PATH = "style/style.tcss"
    current_technician = reactive(None)
    manager = TicketSystemManager()
   
    def on_mount(self) -> None:
        self.title = "Ticket RPG"
        self.sub_title = "Earn XP while working!"
        self.theme = "monokai"
        self.push_screen(HomeScreen())
    
    def login_user(self, technician):
        self.current_technician = technician
        self.sub_title = f"Earn XP while working! Current User: {technician.username}"
    
    def logout_user(self):
        self.current_technician = None
        self.sub_title = "Earn XP while working!"

if __name__ == "__main__":
    app = TicketRPGApp()
    app.run()