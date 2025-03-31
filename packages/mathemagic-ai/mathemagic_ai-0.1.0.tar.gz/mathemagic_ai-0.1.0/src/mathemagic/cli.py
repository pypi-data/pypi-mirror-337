import sys
import typer
from typing import Optional
import signal

try:
    # Try relative import first (for when used as a package)
    from . import mathemagic
except ImportError:
    # Fall back to absolute import (for when run directly)
    import sys
    from pathlib import Path
    # Add the src directory to the path
    sys.path.insert(0, str(Path(__file__).parent.parent))
    # Import the module directly
    from mathemagic import mathemagic

# Create a Typer app for compatibility with entry points
app = typer.Typer(help="Mathemagic: AI calculator for science and engineering problems")


@app.command()
def main(
    problem: Optional[str] = typer.Argument(None, help="Math problem to solve"),
    output_python: bool = typer.Option(False, "--output-python", "-p", help="Output the generated Python code")
):
    """
    Convert a natural language math problem to Python and execute it.
    
    If no problem is provided, enters interactive mode.
    """
    # Handle Ctrl+C gracefully
    def signal_handler(sig, frame):
        print("\nExiting Mathemagic. Goodbye!")
        sys.exit(0)
        
    signal.signal(signal.SIGINT, signal_handler)
    
    if problem:
        process_problem(problem, output_python)
    else:
        # Interactive mode
        typer.echo("Mathemagic Calculator (Press Ctrl+C to exit)")
        typer.echo("Enter your math problem:")
        
        while True:
            try:
                problem = typer.prompt("")
                process_problem(problem, output_python)
                typer.echo("\nEnter another problem:")
            except KeyboardInterrupt:
                typer.echo("\nExiting Mathemagic. Goodbye!")
                sys.exit(0)


def process_problem(problem: str, output_python: bool):
    """Process a single math problem"""
    typer.echo(f"Processing: {problem}")
    
    # Convert problem to Python
    python_code = mathemagic.prompt_to_py(problem)
    
    # Show Python code if requested
    if output_python:
        typer.echo("\nGenerated Python code:")
        typer.echo(f"```python\n{mathemagic.extract_python_code(python_code)}\n```")
    
    # Execute the Python code
    result, success = mathemagic.execute_py(python_code)
    
    # Display result
    typer.echo("\nResult:")
    if success:
        typer.echo(result)
    else:
        typer.echo(f"Error: {result}", err=True)


if __name__ == "__main__":
    app()
