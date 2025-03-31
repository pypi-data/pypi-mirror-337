import random
from typing import List, Dict, Set
from art import text2art, ART_NAMES, FONT_NAMES, ASCII_FONTS
from art.params import SMALL_WIZARD_FONT, MEDIUM_WIZARD_FONT, LARGE_WIZARD_FONT, XLARGE_WIZARD_FONT


class FontManager:
    """Manages font categories, selections, and operations"""
    
    def __init__(self):
        """Initialize the font manager with font categories"""
        # Using the art library's built-in font categories
        self.font_categories = {
            "standard": FONT_NAMES,  # All fonts
            "small": SMALL_WIZARD_FONT,
            "medium": MEDIUM_WIZARD_FONT,
            "large": LARGE_WIZARD_FONT,
            "xlarge": XLARGE_WIZARD_FONT,
            "ascii_only": ASCII_FONTS,  # Only fonts with ASCII characters
            "3d": [f for f in FONT_NAMES if "3d" in f.lower() or "3-d" in f.lower()],
            "block": [f for f in FONT_NAMES if "block" in f.lower()],
            "banner": [f for f in FONT_NAMES if "banner" in f.lower()],
            "bubble": [f for f in FONT_NAMES if "bubble" in f.lower()],
            "digital": [f for f in FONT_NAMES if "digital" in f.lower()],
            "script": [f for f in FONT_NAMES if "script" in f.lower()],
            "slant": [f for f in FONT_NAMES if "slant" in f.lower()],
            "shadow": [f for f in FONT_NAMES if "shadow" in f.lower()],
            "fancy": [f for f in FONT_NAMES if "fancy" in f.lower()],
            "graffiti": [f for f in FONT_NAMES if "graffiti" in f.lower()],
        }
        
        # Available font styles
        self.available_styles = list(self.font_categories.keys())
        
        # Colors for the fonts - using a wider range of colors
        self.colors = [
            "bright_red", "bright_green", "bright_blue", "bright_magenta", 
            "bright_cyan", "bright_yellow", "orange3", "purple", "gold1", 
            "turquoise2", "deep_pink3", "spring_green1", "dodger_blue1", 
            "light_sea_green", "dark_orange3", "yellow3", "magenta", "cyan"
        ]
    
    def get_available_styles(self) -> List[str]:
        """Get the list of available font styles"""
        return self.available_styles
    
    def get_fonts_in_category(self, category: str) -> List[str]:
        """Get fonts in the specified category"""
        return self.font_categories.get(category, [])
    
    def get_random_color(self) -> str:
        """Get a random color for font rendering"""
        return random.choice(self.colors)
    
    def get_random_fonts(self, category: str, used_fonts: Set[str], count: int = 10) -> List[str]:
        """Get random fonts from the specified category that haven't been used yet"""
        if category == "favorites":
            # This case will be handled separately by the caller
            return []
            
        available_fonts = [f for f in self.font_categories[category] if f not in used_fonts]
        
        # If we've shown all fonts or not enough left, return what we have
        if len(available_fonts) < count:
            return available_fonts
            
        return random.sample(available_fonts, count)
    
    def render_text(self, text: str, font: str) -> str:
        """Render text using the specified font"""
        try:
            return text2art(text, font=font)
        except Exception as e:
            return f"Error rendering font: {e}"
    
    def get_fancy_font(self) -> str:
        """Get a random fancy or script font"""
        return random.choice([f for f in FONT_NAMES if "fancy" in f.lower()])
    
    def get_font_count(self, category: str) -> int:
        """Get the number of fonts in the specified category"""
        return len(self.font_categories.get(category, [])) 