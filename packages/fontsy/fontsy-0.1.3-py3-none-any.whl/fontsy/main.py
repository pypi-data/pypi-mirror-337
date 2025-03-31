from rich.console import Console

from .core.app_state import AppState
from .core.font_manager import FontManager
from .core.favorites_manager import FavoritesManager
from .ui.title_screen import TitleScreen
from .ui.display_manager import DisplayManager
from .ui.command_processor import CommandProcessor
from .utils.help_text import get_help_text


def main() -> None:
    """Main entry point for the ASCII Art Font Explorer application"""
    console = Console()
    
    # Initialize core components
    font_manager = FontManager()
    app_state = AppState(font_manager)
    favorites_manager = FavoritesManager(console)
    
    # Load favorites from disk
    if favorites_manager.load_favorites():
        app_state.favorite_fonts = favorites_manager.favorite_fonts
        console.print(f"[green]Loaded {len(app_state.favorite_fonts)} favorites from disk.[/green]")
    
    # Initialize UI components
    title_screen = TitleScreen(console, font_manager)
    display_manager = DisplayManager(console, app_state, font_manager)
    
    # Generate help text
    help_text = get_help_text(app_state.available_styles)
    
    # Show the title screen
    title_screen.show()
    
    # Initialize command processor
    command_processor = CommandProcessor(
        console=console,
        app_state=app_state,
        font_manager=font_manager,
        favorites_manager=favorites_manager,
        display_manager=display_manager,
        title_screen=title_screen,
        help_text=help_text
    )
    
    # Start the main loop
    command_processor.run_command_loop() 