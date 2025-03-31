from rich.console import Console
from rich.panel import Panel
from rich.text import Text


class TitleScreen:
    """Displays the welcome screen of the application"""
    
    def __init__(self, console: Console, font_manager):
        """Initialize the title screen"""
        self.console = console
        self.font_manager = font_manager
    
    def show(self):
        """Display the title screen"""
        # Clear the console
        self.console.clear()
        
        # Generate random fonts for title elements
        title_font = self.font_manager.get_fancy_font()
        subtitle_font = self.font_manager.get_fancy_font()
        
        # Create ASCII art text
        title_art = self.font_manager.render_text("Fontsy - The ASCII Font Explorer", title_font)
        subtitle_art = self.font_manager.render_text("Find your perfect style!", subtitle_font)
        
        # Create styled rich text objects
        title_text = Text(title_art, style="bold green")
        subtitle_text = Text(subtitle_art, style="cyan")
        
        # Display font info at the bottom
        font_info = f"[dim]v0.1.3 - Title Font: [bold cyan]{title_font}[/bold cyan] | Subtitle Font: [bold magenta]{subtitle_font}[/bold magenta][/dim]"
        
        # Combine all elements
        welcome_content = title_text + Text("\n") + subtitle_text
        
        welcome_panel = Panel(
            welcome_content,
            border_style="bright_blue", 
            title="[yellow]✨ Welcome ✨[/yellow]",
            title_align="center",
        )
        self.console.print(welcome_panel)
        self.console.print(font_info)
        
        # Simple instructions instead of full help
        self.console.print("\n[bold cyan]Enter text to see it in different ASCII art fonts[/bold cyan]")
        self.console.print("[dim]Type [bold]help[/bold] for a list of all commands[/dim]")
        self.console.print("[dim]Type [bold]quit[/bold] to exit[/dim]\n") 