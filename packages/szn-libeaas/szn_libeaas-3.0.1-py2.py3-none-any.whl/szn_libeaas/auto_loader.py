"""
Auto-loading module for szn-libeaas.

This module is imported when the package is loaded and helps trigger
the post-installation function.
"""

# Import the auto-run function to trigger the open_readme automatically
from .post_install import auto_run

# This line will trigger the auto_run function when this module is imported
auto_run()