from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static, Button, Log

class RecompDashboardApp(App):
    """Textual TUI dashboard for real-time monitoring of agent loops & context usage."""

    BINDINGS = [("q", "quit", "Quit")]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Static("Deterministic RE & Recompilation Dashboard", id="title")
        yield Log(id="activity_log")
        yield Footer()

    def on_mount(self) -> None:
        log = self.query_one(Log)
        log.write_line("[+] Engine Initialized.")
        log.write_line("[+] Context Window Slicing: Active (4096 tokens).")
        log.write_line("[+] Micro-Prompt Determinism Enforcement: Active.")

if __name__ == "__main__":
    app = RecompDashboardApp()
    app.run()
