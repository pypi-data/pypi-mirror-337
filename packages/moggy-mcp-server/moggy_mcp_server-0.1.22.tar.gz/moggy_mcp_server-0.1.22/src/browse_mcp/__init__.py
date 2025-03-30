from .browse_operation_server import BrowserNavigationServer as server, main as start_server
import asyncio

def main():
    """Main entry point for the package."""
    asyncio.run(start_server())

# Optionally expose other important items at package level
__all__ = ['main', 'server']