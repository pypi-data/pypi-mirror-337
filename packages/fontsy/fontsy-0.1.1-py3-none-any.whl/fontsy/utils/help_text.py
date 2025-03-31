from typing import List


def get_help_text(available_styles: List[str]) -> str:
    """Generate the help text for the application"""
    
    help_text = "\n".join([
        "[bold white]Available commands:[/bold white]",
        "- Type your [bold]text[/bold] and press Enter to see it in different fonts",
        "- Press [bold]Enter[/bold] with empty input to see new fonts for the same text",
        "- Type a [bold]font category[/bold] to filter fonts:",
        f"  {', '.join(sorted(available_styles))}",
        "- Type [bold]grid[/bold] to show fonts in a grid layout (easier comparison)",
        "- Type [bold]list[/bold] to show fonts in list layout (more detail)",
        "- Type [bold]showcase[/bold] to see your text in ALL fonts (in a scrollable view)",
        "  • [bold]showcase [category][/bold] (e.g. 'showcase small')",
        "  • [bold]showcase [number][/bold] (e.g. 'showcase 20' for 20 random fonts)",
        "  • [bold]showcase [range][/bold] (e.g. 'showcase 10-30' for fonts 10 to 30)",
        "- Type a [bold]number[/bold] (e.g. '3') to favorite the font with that number",
        "- Type [bold]clipboard [number][/bold] (e.g. 'clipboard 5') to copy a font to clipboard",
        "- Type [bold]favorite [font_name][/bold] to mark a specific font as favorite",
        "- Type [bold]favorites[/bold] to see only your favorite fonts",
        "- Type [bold]clear[/bold] to clear all your favorites",
        "- Type [bold]title[/bold] to show the welcome screen again",
        "- Export commands:",
        "  • [bold]export html[/bold] - Export last view as HTML",
        "  • [bold]export text[/bold] - Export last view as plain text",
        "  • [bold]export md[/bold] - Export last view as Markdown",
        "- Type [bold]help[/bold] to show this help message",
        "- Type [bold]quit[/bold] to exit"
    ])
    
    return help_text 