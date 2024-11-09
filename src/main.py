"""Main entry point"""

import asyncio
import click
from typing import Optional

from .ui.streamlit_app import main as streamlit_main
from .utils.system_check import print_system_status
from .utils.validation import validate_config
from .utils.logging import setup_logging

logger = setup_logging()

@click.group()
def cli():
    """Mac & iOS Control CLI"""
    pass

@cli.command()
def check():
    """Check system requirements"""
    if not print_system_status():
        exit(1)
    
    if errors := validate_config():
        click.echo("Configuration errors found:")
        for error in errors:
            click.echo(f"❌ {error}")
        exit(1)
        
    click.echo("✅ System check passed!")

@cli.command()
def ui():
    """Start the Streamlit UI"""
    # Run system check first
    if not print_system_status():
        exit(1)
    
    if errors := validate_config():
        logger.error("Configuration errors found:")
        for error in errors:
            logger.error(error)
        exit(1)
    
    # Start UI
    streamlit_main()

if __name__ == "__main__":
    cli() 