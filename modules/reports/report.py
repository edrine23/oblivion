import logging
from typing import Dict, List
from pathlib import Path
import jinja2
from weasyprint import HTML
from rich.console import Console
from datetime import datetime

logger = logging.getLogger(__name__)
console = Console()

class ReportGenerator:
    """Generates HTML and PDF reports."""
    
    def __init__(self, config: Dict):
        self.config = config
        self.results: Dict[str, List] = {}
        self.env = jinja2.Environment(loader=jinja2.DictLoader({
            "report_template": """
            <!DOCTYPE html>
            <html>
            <head><title>Oblivion Report</title></head>
            <body>
            <h1>Oblivion Scan Report</h1>
            <p>Generated: {{ timestamp }}</p>
            {% for module, results in results.items() %}
            <h2>{{ module }}</h2>
            <ul>
            {% for result in results %}
            <li>{{ result }}</li>
            {% endfor %}
            </ul>
            {% endfor %}
            </body>
            </html>
            """
        }))
    
    def add_results(self, module: str, results: List) -> None:
        """Add results to the report."""
        self.results[module] = results
    
    def generate_report(self, format: str = "html") -> str:
        """Generate a report in HTML or PDF."""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            template = self.env.get_template("report_template")
            html_content = template.render(timestamp=timestamp, results=self.results)
            output_file = Path(self.config['output_dir']) / f"report_{timestamp}.{format}"
            
            if format == "html":
                with output_file.open('w') as f:
                    f.write(html_content)
            elif format == "pdf":
                HTML(string=html_content).write_pdf(output_file)
            else:
                raise ValueError("Unsupported format")
            
            console.print(f"[green]Report saved to {output_file}[/green]")
            return str(output_file)
        except Exception as e:
            logger.error(f"Report generation failed: {e}")
            raise