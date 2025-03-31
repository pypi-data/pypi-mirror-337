from typing import List, Optional
import random
import re

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.columns import Columns
from rich.table import Table
from rich.progress import Progress
from rich import box


class DisplayManager:
    """Manages the display of fonts in different modes (list, grid, showcase)"""
    
    def __init__(self, console: Console, app_state, font_manager):
        """Initialize the display manager"""
        self.console = console
        self.app_state = app_state
        self.font_manager = font_manager
    
    def display_fonts(self, text: str, fonts: List[str]):
        """Display the fonts based on the current display mode"""
        if not fonts:
            self.console.print("[yellow]No fonts to display.[/yellow]")
            return
        
        category = self.app_state.current_category
        used_fonts_count = len(self.app_state.used_fonts)
        
        # Determine category count for progress display
        if category == "favorites":
            category_count = len(self.app_state.favorite_fonts)
        else:
            category_count = self.font_manager.get_font_count(category)
        
        # Create title
        title = f"[bold]'{text}'[/bold] in {len(fonts)} {category.upper()} fonts ({used_fonts_count}/{category_count} shown)"
        self.console.print(Panel(title, border_style="blue"))
        
        # Store current fonts for favorite/unfavorite operations
        self.app_state.update_current_fonts(fonts)
        
        # Display based on mode
        if self.app_state.display_mode == 'grid':
            self._display_grid(text, fonts)
        else:
            self._display_list(text, fonts)
        
        # Show status line
        favorite_status = f" | Favorites: {len(self.app_state.favorite_fonts)}" if self.app_state.favorite_fonts else ""
        self.console.print("\n[dim]Press Enter to see more fonts, or type new text, or 'quit' to exit.[/dim]")
        self.console.print("[dim]Type 'export html', 'export text', or 'export md' to save this view.[/dim]")
        self.console.print(f"[dim]Mode: {self.app_state.display_mode.upper()} | Category: {category.upper()}{favorite_status}[/dim]")
    
    def _display_grid(self, text: str, fonts: List[str]):
        """Display fonts in a grid layout"""
        grid_items = []
        
        for i, font in enumerate(fonts):
            try:
                art = self.font_manager.render_text(text, font)
                # Select a random color
                color = self.font_manager.get_random_color()
                # Check if the font is a favorite
                is_favorite = "★ " if font in self.app_state.favorite_fonts else ""
                
                panel = Panel(
                    Text(art, style=color),
                    title=f"[bold white]{i+1}. {is_favorite}{font}[/bold white]",
                    subtitle="Type number to favorite/unfavorite",
                    border_style=color,
                    expand=False
                )
                grid_items.append(panel)
            except Exception as e:
                grid_items.append(Panel(f"Error: {e}", title=f"{i+1}. {font}", border_style="red"))
        
        # Display in columns
        columns = Columns(grid_items, equal=True, expand=True)
        self.console.print(columns)
    
    def _display_list(self, text: str, fonts: List[str]):
        """Display fonts in a list layout"""
        for i, font in enumerate(fonts):
            try:
                art = self.font_manager.render_text(text, font)
                # Select a random color
                color = self.font_manager.get_random_color()
                banner_text = Text(art, style=f"bold {color}")
                
                # Check if the font is a favorite
                is_favorite = "★ " if font in self.app_state.favorite_fonts else ""
                fav_status = "unfavorite" if font in self.app_state.favorite_fonts else "favorite"
                
                # Create panel with the font name and art
                panel = Panel(
                    banner_text,
                    title=f"[bold white]{i+1}. {is_favorite}{font}[/bold white]",
                    subtitle=f"Type {i+1} to {fav_status}",
                    border_style=color
                )
                self.console.print(panel)
            except Exception as e:
                self.console.print(Panel(f"Error: {e}", title=f"{i+1}. Font: {font}", border_style="red"))
    
    def display_showcase(self, command: List[str], text: str):
        """Display a showcase of fonts"""
        if not text:
            self.console.print("[yellow]Please enter some text first.[/yellow]")
            return
        
        # Default is to show all fonts
        fonts_to_show = sorted(self.font_manager.get_fonts_in_category("standard"))
        title_prefix = "ALL"
        
        # Check for category option (e.g., "showcase small")
        if len(command) > 1 and command[1] in self.app_state.available_styles:
            category = command[1]
            if category == "favorites":
                if not self.app_state.favorite_fonts:
                    self.console.print("[yellow]You don't have any favorite fonts yet.[/yellow]")
                    return
                fonts_to_show = sorted(self.app_state.favorite_fonts)
                title_prefix = "FAVORITE"
            else:
                fonts_to_show = sorted(self.font_manager.get_fonts_in_category(category))
                title_prefix = category.upper()
        
        # Check for random sample option (e.g., "showcase 20")
        elif len(command) > 1 and command[1].isdigit():
            total_fonts = len(self.font_manager.get_fonts_in_category("standard"))
            sample_size = min(int(command[1]), total_fonts)
            fonts_to_show = random.sample(self.font_manager.get_fonts_in_category("standard"), sample_size)
            title_prefix = f"{sample_size} RANDOM"
        
        # Check for range option (e.g., "showcase 10-30")
        elif len(command) > 1 and re.match(r'^\d+-\d+$', command[1]):
            try:
                start, end = map(int, command[1].split('-'))
                total_fonts = len(self.font_manager.get_fonts_in_category("standard"))
                
                if start < 1:
                    start = 1
                if end > total_fonts:
                    end = total_fonts
                if start > end:
                    start, end = end, start
                
                # Get fonts in the specified range (from sorted list)
                all_fonts_sorted = sorted(self.font_manager.get_fonts_in_category("standard"))
                fonts_to_show = all_fonts_sorted[start-1:end]
                title_prefix = f"RANGE {start}-{end}"
            except ValueError:
                self.console.print("[yellow]Invalid range format. Use 'showcase 10-30' format.[/yellow]")
                return
        
        self.console.print(f"[bold green]Generating showcase of {title_prefix} fonts for '[bold white]{text}[/bold white]'...[/bold green]")
        self.console.print("[yellow]This might take a moment. Press Ctrl+C to cancel.[/yellow]")
        
        # Store the showcase fonts for favoriting by number
        self.app_state.update_showcase_fonts(fonts_to_show)
        
        # Create a colorful table with the selected fonts
        table = Table(
            title=f"[bold]{title_prefix} Font Showcase[/bold] for '{text}'", 
            box=box.ROUNDED, 
            header_style="bold magenta",
            title_style="bold cyan",
            border_style="bright_blue"
        )
        table.add_column("#", style="dim", width=4)
        table.add_column("Font Name", style="cyan")
        table.add_column("Preview")
        
        # Add progress bar for large operations
        with Progress() as progress:
            task = progress.add_task(f"[cyan]Rendering {len(fonts_to_show)} fonts...", total=len(fonts_to_show))
            
            for i, font in enumerate(fonts_to_show):
                try:
                    art = self.font_manager.render_text(text, font)
                    is_favorite = "★ " if font in self.app_state.favorite_fonts else ""
                    
                    # Assign a random color for the font preview
                    color = self.font_manager.get_random_color()
                    colored_art = f"[{color}]{art}[/{color}]"
                    
                    table.add_row(str(i+1), f"{is_favorite}{font}", colored_art)
                except Exception:
                    table.add_row(str(i+1), font, "[red](Font rendering failed)[/red]")
                progress.update(task, advance=1)
        
        self.console.print(table)
        self.console.print("[dim]Type a number to favorite/unfavorite a font from this showcase.[/dim]")
        self.console.print("[dim]Type 'export html', 'export text', or 'export md' to save this view.[/dim]") 