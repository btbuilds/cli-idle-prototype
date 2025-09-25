from textual.app import App
from textual.reactive import reactive
from panels.login import LoginScreen
from panels.home import HomeScreen

class TicketRPGApp(App):
    SCREENS = {"loginscreen": LoginScreen,
               "homescreen": HomeScreen}
    BINDINGS = [("l", "push_screen('loginscreen')", "Login")]
    CSS_PATH = "style/style.tcss"
   
    def on_mount(self) -> None:
        self.title = "Ticket RPG"
        self.sub_title = "Earn XP while working!"
        self.theme = "monokai"
        self.push_screen("homescreen")

if __name__ == "__main__":
    app = TicketRPGApp()
    app.run()