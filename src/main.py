from textual.app import App
from panels.home import HomeScreen

class TicketRPGApp(App):
    CSS_PATH = "style/style.tcss"
   
    def on_mount(self) -> None:
        self.title = "Ticket RPG"
        self.sub_title = "Earn XP while working!"
        self.theme = "monokai"
        self.push_screen(HomeScreen())

if __name__ == "__main__":
    app = TicketRPGApp()
    app.run()