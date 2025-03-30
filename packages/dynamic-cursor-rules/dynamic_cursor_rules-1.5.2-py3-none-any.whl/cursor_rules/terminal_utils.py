"""
Terminal utilities for CLI output formatting.
"""
import colorama
from colorama import Fore, Style, Back

# Initialize colorama for cross-platform color support
colorama.init(autoreset=True)

# Console output helpers
def print_header(text):
    """Print a styled header"""
    print(f"\n{Back.BLUE}{Fore.WHITE}{Style.BRIGHT} {text} {Style.RESET_ALL}")

def print_success(text):
    """Print a success message"""
    print(f"{Fore.GREEN}{Style.BRIGHT}✓ {text}{Style.RESET_ALL}")

def print_info(text):
    """Print an info message"""
    print(f"{Fore.CYAN}ℹ {text}{Style.RESET_ALL}")

def print_warning(text):
    """Print a warning message"""
    print(f"{Fore.YELLOW}⚠ {text}{Style.RESET_ALL}")

def print_error(text):
    """Print an error message"""
    print(f"{Fore.RED}✗ {text}{Style.RESET_ALL}")

def print_step(text):
    """Print a step in a process"""
    print(f"{Fore.MAGENTA}→ {text}{Style.RESET_ALL}") 