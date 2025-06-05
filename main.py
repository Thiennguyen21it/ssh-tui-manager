#!/usr/bin/env python3

import sys
from src.tui.interface import SSHManagerApp

def main():
    try:
        app = SSHManagerApp()
        app.run()
    except KeyboardInterrupt:
        print("\nExiting SSH Manager...")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 