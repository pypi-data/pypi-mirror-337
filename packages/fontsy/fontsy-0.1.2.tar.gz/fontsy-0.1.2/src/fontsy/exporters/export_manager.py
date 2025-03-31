import os
import datetime
from pathlib import Path
from typing import List

from rich.console import Console
from art import text2art


class ExportManager:
    """Manages the export of ASCII art to various formats"""
    
    def __init__(self, console: Console, app_state):
        """Initialize the export manager"""
        self.console = console
        self.app_state = app_state
        
        # Create exports directory if it doesn't exist
        self.exports_dir = Path(os.path.expanduser("~")) / "ascii_art_exports"
        self.exports_dir.mkdir(exist_ok=True)
    
    def export(self, format_type: str, fonts_to_export: List[str], display_text: str) -> str:
        """Export the current display to the specified format"""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename_base = f"ascii_art_{display_text[:20].replace(' ', '_')}_{timestamp}"
        
        if format_type == "text":
            return self._export_text(filename_base, fonts_to_export, display_text)
        elif format_type == "html":
            return self._export_html(filename_base, fonts_to_export, display_text)
        elif format_type == "md":
            return self._export_markdown(filename_base, fonts_to_export, display_text)
        else:
            self.console.print(f"[yellow]Unknown export format: {format_type}[/yellow]")
            return ""
    
    def _export_text(self, filename_base: str, fonts_to_export: List[str], display_text: str) -> str:
        """Export to text format"""
        filename = self.exports_dir / f"{filename_base}.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"ASCII Art Export for '{display_text}'\n")
            f.write(f"Generated on {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            for i, font in enumerate(fonts_to_export):
                try:
                    art = text2art(display_text, font=font)
                    f.write(f"Font {i+1}: {font}\n")
                    f.write(f"{art}\n")
                    f.write("-" * 80 + "\n\n")
                except Exception:
                    f.write(f"Font {i+1}: {font} - Rendering failed\n\n")
        
        self.console.print(f"[green]Exported to text file: [bold]{filename}[/bold][/green]")
        return str(filename)
    
    def _export_html(self, filename_base: str, fonts_to_export: List[str], display_text: str) -> str:
        """Export to HTML format"""
        filename = self.exports_dir / f"{filename_base}.html"
        
        with open(filename, 'w', encoding='utf-8') as f:
            # Write HTML header and styles
            f.write(f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ASCII Art Export for '{display_text}'</title>
    <style>
        body {{ font-family: monospace; background-color: #1e1e1e; color: #f0f0f0; padding: 20px; }}
        h1, h2 {{ color: #3aa8c1; }}
        .font-container {{ margin-bottom: 30px; border: 1px solid #444; padding: 15px; border-radius: 5px; }}
        .font-name {{ color: #e9950c; font-weight: bold; margin-bottom: 5px; display: flex; justify-content: space-between; align-items: center; }}
        .ascii-art {{ white-space: pre; background-color: #252525; padding: 15px; border-radius: 3px; }}
        .favorite {{ color: #ff9900; }}
        .copy-btn {{ background-color: #2d5e6c; color: white; border: none; border-radius: 3px; padding: 3px 10px; 
                   cursor: pointer; font-family: sans-serif; font-size: 12px; }}
        .copy-btn:hover {{ background-color: #3aa8c1; }}
        footer {{ margin-top: 50px; color: #888; text-align: center; font-size: 0.8em; }}
        .copy-feedback {{ position: fixed; top: 20px; right: 20px; background-color: #3aa8c1; color: white; 
                        padding: 10px 20px; border-radius: 4px; display: none; transition: opacity 0.5s; }}
    </style>
</head>
<body>
    <h1>ASCII Art Export for '{display_text}'</h1>
    <p>Generated on {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    <div id="copyFeedback" class="copy-feedback">Copied to clipboard!</div>
    
    <script>
        function copyToClipboard(text) {{
            const textarea = document.createElement('textarea');
            textarea.value = text;
            document.body.appendChild(textarea);
            textarea.select();
            document.execCommand('copy');
            document.body.removeChild(textarea);
            
            // Show feedback
            const feedback = document.getElementById('copyFeedback');
            feedback.style.display = 'block';
            setTimeout(() => {{
                feedback.style.opacity = '0';
                setTimeout(() => {{
                    feedback.style.display = 'none';
                    feedback.style.opacity = '1';
                }}, 500);
            }}, 1500);
        }}
    </script>
""")
            
            # Write each font section
            for i, font in enumerate(fonts_to_export):
                try:
                    art = text2art(display_text, font=font)
                    star = "★ " if font in self.app_state.favorite_fonts else ""
                    favorite_class = " favorite" if font in self.app_state.favorite_fonts else ""
                    
                    f.write(f"""    <div class="font-container">
        <div class="font-name{favorite_class}">
            <span>{i+1}. {star}{font}</span>
            <button class="copy-btn" onclick="copyToClipboard(`{art.replace('`', '\\`')}`)">Copy to Clipboard</button>
        </div>
        <pre class="ascii-art">{art}</pre>
    </div>
""")
                except Exception:
                    f.write(f"""    <div class="font-container">
        <div class="font-name">{i+1}. {font}</div>
        <div class="ascii-art">Rendering failed</div>
    </div>
""")
            
            # Write footer
            f.write(f"""    <footer>
        Created with ASCII Art Font Explorer | <a href="https://www.ascii-art.site" style="color: #3aa8c1;">www.ascii-art.site</a>
    </footer>
</body>
</html>""")
        
        self.console.print(f"[green]Exported to HTML file: [bold]{filename}[/bold][/green]")
        return str(filename)
    
    def _export_markdown(self, filename_base: str, fonts_to_export: List[str], display_text: str) -> str:
        """Export to Markdown format"""
        filename = self.exports_dir / f"{filename_base}.md"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"# ASCII Art Export for '{display_text}'\n\n")
            f.write(f"Generated on {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            for i, font in enumerate(fonts_to_export):
                try:
                    art = text2art(display_text, font=font)
                    star = "★ " if font in self.app_state.favorite_fonts else ""
                    f.write(f"## {i+1}. {star}{font}\n\n")
                    f.write("```\n")
                    f.write(f"{art}\n")
                    f.write("```\n\n")
                    f.write("---\n\n")
                except Exception:
                    f.write(f"## {i+1}. {font}\n\n")
                    f.write("Rendering failed\n\n")
                    f.write("---\n\n")
            
            f.write(f"\n\n*Created with ASCII Art Font Explorer | [www.ascii-art.site](https://www.ascii-art.site)*")
        
        self.console.print(f"[green]Exported to Markdown file: [bold]{filename}[/bold][/green]")
        return str(filename) 