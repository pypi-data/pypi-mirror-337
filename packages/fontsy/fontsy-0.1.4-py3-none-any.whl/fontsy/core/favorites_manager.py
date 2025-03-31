import os
import json
from typing import Set, Optional
from rich.console import Console


class FavoritesManager:
    """Manages user's favorite fonts"""
    
    def __init__(self, console: Console):
        """Initialize the favorites manager"""
        self.console = console
        self.favorite_fonts: Set[str] = set()
        
        # File to save favorites
        self.favorites_file = os.path.join(os.path.expanduser("~"), ".ascii_art_favorites.json")
    
    def load_favorites(self) -> bool:
        """Load favorites from disk"""
        if os.path.exists(self.favorites_file):
            try:
                with open(self.favorites_file, 'r') as f:
                    self.favorite_fonts = set(json.load(f))
                return True
            except Exception as e:
                self.console.print(f"[yellow]Error loading favorites: {e}[/yellow]")
                return False
        return False
    
    def save_favorites(self) -> bool:
        """Save favorites to disk"""
        try:
            with open(self.favorites_file, 'w') as f:
                json.dump(list(self.favorite_fonts), f)
            return True
        except Exception as e:
            self.console.print(f"[yellow]Error saving favorites: {e}[/yellow]")
            return False
    
    def toggle_favorite(self, font_name: str) -> bool:
        """Toggle favorite status for a font"""
        if font_name in self.favorite_fonts:
            self.favorite_fonts.remove(font_name)
            self.console.print(f"[yellow]Removed [bold]{font_name}[/bold] from favorites[/yellow]")
        else:
            self.favorite_fonts.add(font_name)
            self.console.print(f"[green]Added [bold]{font_name}[/bold] to favorites![/green]")
        return self.save_favorites()
    
    def clear_favorites(self) -> bool:
        """Clear all favorites"""
        self.favorite_fonts.clear()
        return self.save_favorites()
    
    def is_favorite(self, font_name: str) -> bool:
        """Check if a font is a favorite"""
        return font_name in self.favorite_fonts 