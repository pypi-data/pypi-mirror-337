from typing import List, Set, Dict, Optional


class AppState:
    """Manages the application state and user session data"""
    
    def __init__(self, font_manager):
        """Initialize the application state"""
        self.last_input: str = ""
        self.used_fonts: Set[str] = set()
        self.current_category: str = "standard"
        self.display_mode: str = "list"  # Default display mode
        self.current_fonts: List[str] = []  # Keep track of currently displayed fonts
        self.showcase_fonts: List[str] = []  # Keep track of fonts displayed in showcase mode
        self.favorite_fonts: Set[str] = set()
        
        # Get available styles from font manager
        self.available_styles = font_manager.get_available_styles()
        
    def reset_showcase_mode(self):
        """Reset the showcase mode"""
        self.showcase_fonts = []
        
    def reset_used_fonts(self):
        """Reset the used fonts set"""
        self.used_fonts = set()
        
    def update_current_fonts(self, fonts: List[str]):
        """Update the current fonts list"""
        self.current_fonts = fonts.copy()
        
    def update_showcase_fonts(self, fonts: List[str]):
        """Update the showcase fonts list"""
        self.showcase_fonts = fonts.copy()
        
    def add_to_used_fonts(self, fonts: List[str]):
        """Add fonts to the used fonts set"""
        self.used_fonts.update(fonts)
        
    def set_display_mode(self, mode: str):
        """Set the display mode"""
        if mode in ["list", "grid"]:
            self.display_mode = mode
            return True
        return False
        
    def set_current_category(self, category: str):
        """Set the current font category"""
        if category in self.available_styles:
            self.current_category = category
            return True
        return False 