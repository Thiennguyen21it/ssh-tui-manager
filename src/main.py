#!/usr/bin/env python3

import sys
import os
import argparse
from pathlib import Path
from .tui.interface import SSHManagerApp

def get_config_dir():
    """Get the configuration directory path."""
    # Use XDG_CONFIG_HOME if available, otherwise use ~/.config
    xdg_config_home = os.environ.get("XDG_CONFIG_HOME")
    if xdg_config_home:
        config_base = Path(xdg_config_home)
    else:
        config_base = Path.home() / ".config"
    
    # Create the ssh-tui-manager directory
    config_dir = config_base / "ssh-tui-manager"
    config_dir.mkdir(parents=True, exist_ok=True)
    
    return config_dir

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="SSH TUI Manager - A terminal user interface for managing SSH connections"
    )
    parser.add_argument(
        "--config-dir",
        help="Path to the configuration directory",
        default=None,
    )
    return parser.parse_args()

def main():
    """Main entry point for the application."""
    args = parse_args()
    
    # Determine configuration directory
    config_dir = args.config_dir if args.config_dir else get_config_dir()
    
    try:
        # Initialize and run the app
        app = SSHManagerApp(config_dir=str(config_dir))
        app.run()
    except KeyboardInterrupt:
        print("\nExiting SSH Manager...")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 