from typing import List, Optional, Dict, Callable
import random
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

try:
    import pyperclip
    CLIPBOARD_AVAILABLE = True
except ImportError:
    CLIPBOARD_AVAILABLE = False


class CommandProcessor:
    """Processes user commands and manages the input loop"""
    
    def __init__(self, console, app_state, font_manager, favorites_manager, 
                 display_manager, title_screen, help_text):
        """Initialize the command processor"""
        self.console = console
        self.app_state = app_state
        self.font_manager = font_manager
        self.favorites_manager = favorites_manager
        self.display_manager = display_manager
        self.title_screen = title_screen
        self.help_text = help_text
        
        # Set up command handlers with a dictionary of command -> handler function
        self.command_handlers = {
            'quit': self._handle_quit,
            'help': self._handle_help,
            'title': self._handle_title,
            'grid': self._handle_grid,
            'list': self._handle_list,
            'favorites': self._handle_favorites,
            'clear': self._handle_clear,
            'export': self._handle_export,
            'showcase': self._handle_showcase,
            'favorite': self._handle_favorite_by_name,
            'clipboard': self._handle_clipboard,
        }
        
        # If clipboard functionality isn't available, show installation instructions
        if not CLIPBOARD_AVAILABLE:
            self.console.print("[yellow]Clipboard functionality requires 'pyperclip' package.[/yellow]")
            self.console.print("[yellow]Install it with: pip install pyperclip[/yellow]")
            self.console.print("[yellow]Then restart the application to enable clipboard features.[/yellow]")
    
    def run_command_loop(self):
        """Run the main command loop"""
        while True:
            user_input = Prompt.ask("\n[bold cyan]Enter text or command[/bold cyan]")
            self.process_input(user_input)
    
    def process_input(self, user_input: str) -> bool:
        """Process user input - returns True if should continue, False if should exit"""
        # Convert to lowercase for command processing
        input_lower = user_input.lower()
        
        # Handle empty input
        if not user_input.strip():
            return self._handle_empty_input()
        
        # Check if input is a command
        command_parts = input_lower.split()
        if command_parts[0] in self.command_handlers:
            return self.command_handlers[command_parts[0]](command_parts)
        
        # Check if input is a number (for favoriting fonts)
        if input_lower.isdigit():
            return self._handle_favorite_by_number(int(input_lower))
        
        # Check if input is a font category
        if input_lower in self.app_state.available_styles:
            return self._handle_category_change(input_lower)
        
        # If not a command, treat as text to convert
        return self._handle_text_input(user_input)
    
    def _handle_quit(self, command_parts: List[str]) -> bool:
        """Handle the quit command"""
        # Save favorites before exiting
        if self.favorites_manager.save_favorites():
            self.console.print(f"[green]Saved {len(self.favorites_manager.favorite_fonts)} favorites to disk.[/green]")
        self.console.print("[bold green]Thanks for using ASCII Art Font Explorer! Come back soon![/bold green]")
        return False  # Signal to exit the main loop
    
    def _handle_help(self, command_parts: List[str]) -> bool:
        """Handle the help command"""
        self.console.print(Panel(self.help_text, title="[bold]Commands & Tips[/bold]", border_style="green"))
        
        # Information about increasing terminal buffer
        terminal_help = "\n".join([
            "[bold white]Tip: Increase your terminal scrollback buffer[/bold white]",
            "[dim]If you want to see more output history, you can increase your terminal's scrollback buffer:[/dim]",
            "",
            "[bold yellow]Windows Terminal:[/bold yellow]",
            "  Settings > Profile > Scrollback > Increase 'Buffer Size' (e.g., 10000 lines)",
            "",
            "[bold yellow]macOS Terminal:[/bold yellow]",
            "  Terminal > Preferences > Profiles > (Select profile) > Terminal > Increase 'Scrollback' limit",
            "",
            "[bold yellow]Linux Terminal:[/bold yellow]",
            "  Edit > Preferences > Profile > Scrolling > Increase 'Scrollback lines'",
            "",
            "[dim]This allows you to scroll back and see more fonts when using showcase mode.[/dim]"
        ])
        self.console.print(Panel(terminal_help, title="[bold]Terminal Scrollback Help[/bold]", border_style="blue"))
        return True
    
    def _handle_title(self, command_parts: List[str]) -> bool:
        """Handle the title command"""
        self.title_screen.show()
        return True
    
    def _handle_grid(self, command_parts: List[str]) -> bool:
        """Handle the grid command"""
        self.app_state.set_display_mode('grid')
        self.console.print("[yellow]Switched to grid display mode[/yellow]")
        return True
    
    def _handle_list(self, command_parts: List[str]) -> bool:
        """Handle the list command"""
        self.app_state.set_display_mode('list')
        self.console.print("[yellow]Switched to list display mode[/yellow]")
        return True
    
    def _handle_favorites(self, command_parts: List[str]) -> bool:
        """Handle the favorites command"""
        if not self.favorites_manager.favorite_fonts:
            self.console.print("[yellow]You haven't marked any fonts as favorites yet.[/yellow]")
            return True
            
        self.app_state.set_current_category("favorites")
        self.app_state.reset_used_fonts()
        self.console.print(f"[bold yellow]Showing your favorite fonts[/bold yellow]")
        
        if self.app_state.last_input:
            self.console.print(f"[dim]Using previous text: '{self.app_state.last_input}'[/dim]")
            return self._handle_text_input(self.app_state.last_input)
        else:
            self.console.print("[dim]Please enter some text to convert.[/dim]")
            return True
    
    def _handle_clear(self, command_parts: List[str]) -> bool:
        """Handle the clear command"""
        self.favorites_manager.clear_favorites()
        self.console.print("[yellow]All favorites cleared and saved to disk.[/yellow]")
        return True
    
    def _handle_export(self, command_parts: List[str]) -> bool:
        """Handle the export command"""
        from ..exporters.export_manager import ExportManager
        
        if len(command_parts) < 2:
            self.console.print("[yellow]Please specify an export format: html, text, or md[/yellow]")
            return True
            
        if not self.app_state.last_input:
            self.console.print("[yellow]Please display some fonts first before exporting.[/yellow]")
            return True
            
        export_format = command_parts[1]
        
        # Determine which fonts to export
        if self.app_state.showcase_fonts:
            fonts_to_export = self.app_state.showcase_fonts
        elif self.app_state.current_fonts:
            fonts_to_export = self.app_state.current_fonts
        else:
            self.console.print("[yellow]No fonts to export. Please display some fonts first.[/yellow]")
            return True
            
        exporter = ExportManager(self.console, self.app_state)
        
        if export_format in ['html', 'text', 'md', 'markdown']:
            if export_format == 'markdown':
                export_format = 'md'
            exporter.export(export_format, fonts_to_export, self.app_state.last_input)
        else:
            self.console.print(f"[yellow]Unknown export format: {export_format}. Please use html, text, or md.[/yellow]")
        
        return True
    
    def _handle_showcase(self, command_parts: List[str]) -> bool:
        """Handle the showcase command"""
        self.display_manager.display_showcase(command_parts, self.app_state.last_input)
        return True
    
    def _handle_favorite_by_name(self, command_parts: List[str]) -> bool:
        """Handle the 'favorite <font_name>' command"""
        if len(command_parts) < 2:
            self.console.print("[yellow]Please specify a font name to favorite.[/yellow]")
            return True
            
        font_name = ' '.join(command_parts[1:])
        
        if font_name in self.font_manager.get_fonts_in_category("standard"):
            self.favorites_manager.toggle_favorite(font_name)
        else:
            self.console.print(f"[yellow]Font [bold]{font_name}[/bold] not found. Please check the name.[/yellow]")
        
        return True
    
    def _handle_clipboard(self, command_parts: List[str]) -> bool:
        """Handle the clipboard command"""
        if not CLIPBOARD_AVAILABLE:
            self.console.print("[yellow]Clipboard functionality requires 'pyperclip' package.[/yellow]")
            self.console.print("[yellow]Install it with: pip install pyperclip[/yellow]")
            return True
            
        if len(command_parts) < 2 or not command_parts[1].isdigit():
            self.console.print("[yellow]Please specify a valid font number: 'clipboard 5'[/yellow]")
            return True
            
        font_number = int(command_parts[1])
        
        # Determine which fonts list to use
        if self.app_state.showcase_fonts:
            fonts_list = self.app_state.showcase_fonts
        elif self.app_state.current_fonts:
            fonts_list = self.app_state.current_fonts
        else:
            self.console.print("[yellow]No fonts to copy. Please display some fonts first.[/yellow]")
            return True
            
        self._copy_font_to_clipboard(font_number, fonts_list)
        return True
    
    def _handle_favorite_by_number(self, font_number: int) -> bool:
        """Handle favoriting a font by number"""
        # Check if we're in showcase mode and use showcase_fonts
        if self.app_state.showcase_fonts and 1 <= font_number <= len(self.app_state.showcase_fonts):
            font_name = self.app_state.showcase_fonts[font_number - 1]
            self.favorites_manager.toggle_favorite(font_name)
        # Otherwise use the current view fonts
        elif self.app_state.current_fonts and 1 <= font_number <= len(self.app_state.current_fonts):
            font_name = self.app_state.current_fonts[font_number - 1]
            self.favorites_manager.toggle_favorite(font_name)
        else:
            self.console.print(f"[yellow]No font with number {font_number} in current view.[/yellow]")
        
        return True
    
    def _handle_category_change(self, category: str) -> bool:
        """Handle changing to a different font category"""
        self.app_state.set_current_category(category)
        self.app_state.reset_used_fonts()
        self.console.print(f"[bold yellow]Switched to {category.upper()} fonts[/bold yellow]")
        
        # Reset showcase mode
        self.app_state.reset_showcase_mode()
        
        if self.app_state.last_input:
            self.console.print(f"[dim]Using previous text: '{self.app_state.last_input}'[/dim]")
            return self._handle_text_input(self.app_state.last_input)
        else:
            self.console.print("[dim]Please enter some text to convert.[/dim]")
            return True
    
    def _handle_empty_input(self) -> bool:
        """Handle empty input (display new fonts for same text)"""
        if not self.app_state.last_input:
            self.console.print("[yellow]Please enter some text to convert.[/yellow]")
            return True
            
        self.console.print(f"[dim]Using previous text: '{self.app_state.last_input}'[/dim]")
        
        # Reset showcase mode when showing new fonts
        self.app_state.reset_showcase_mode()
        
        return self._display_fonts_for_text(self.app_state.last_input)
    
    def _handle_text_input(self, text: str) -> bool:
        """Handle text input (display fonts for the text)"""
        # Save the new input
        self.app_state.last_input = text
        
        # Reset showcase mode when entering new text
        self.app_state.reset_showcase_mode()
        
        if self.app_state.current_category != "standard":
            # Keep the current category when entering new text
            pass
        else:
            self.app_state.reset_used_fonts()
        
        return self._display_fonts_for_text(text)
    
    def _display_fonts_for_text(self, text: str) -> bool:
        """Display fonts for the specified text"""
        # Determine which fonts to use based on current category
        if self.app_state.current_category == "favorites":
            available_fonts = [f for f in self.favorites_manager.favorite_fonts if f not in self.app_state.used_fonts]
        else:
            available_fonts = [
                f for f in self.font_manager.get_fonts_in_category(self.app_state.current_category)
                if f not in self.app_state.used_fonts
            ]
        
        # If we've shown all fonts or not enough left, reset the used fonts
        if len(available_fonts) < 10:
            if self.app_state.current_category == "favorites":
                self.console.print(f"[yellow]You've seen all your favorite fonts. Starting over.[/yellow]")
                self.app_state.reset_used_fonts()
                available_fonts = list(self.favorites_manager.favorite_fonts)
            else:
                self.console.print(f"[yellow]You've seen most of the available {self.app_state.current_category.upper()} fonts. Starting over.[/yellow]")
                self.app_state.reset_used_fonts()
                available_fonts = self.font_manager.get_fonts_in_category(self.app_state.current_category)
        
        # Select 10 random fonts or less if not enough available
        num_fonts = min(10, len(available_fonts))
        if num_fonts == 0:
            self.console.print("[yellow]No fonts available in this category.[/yellow]")
            return True
            
        selected_fonts = random.sample(available_fonts, num_fonts)
        
        # Add selected fonts to used fonts
        self.app_state.add_to_used_fonts(selected_fonts)
        
        # Display the selected fonts
        self.display_manager.display_fonts(text, selected_fonts)
        
        return True
    
    def _copy_font_to_clipboard(self, font_number: int, fonts_list: List[str]) -> bool:
        """Copy a font to clipboard"""
        if not CLIPBOARD_AVAILABLE:
            self.console.print("[yellow]Clipboard functionality requires 'pyperclip' package.[/yellow]")
            self.console.print("[yellow]Install it with: pip install pyperclip[/yellow]")
            return False
            
        if 1 <= font_number <= len(fonts_list):
            font_name = fonts_list[font_number - 1]
            try:
                art = self.font_manager.render_text(self.app_state.last_input, font_name)
                pyperclip.copy(art)
                self.console.print(f"[green]Copied font [bold]{font_name}[/bold] to clipboard![/green]")
                return True
            except Exception as e:
                self.console.print(f"[yellow]Error copying font: {e}[/yellow]")
                return False
        else:
            self.console.print(f"[yellow]No font with number {font_number} in current view.[/yellow]")
            return False 