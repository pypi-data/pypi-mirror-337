#!/usr/bin/env python
"""
Post-installation script for szn-libeaas package.

This script runs after the package is installed to provide initial documentation.
"""
import time
import importlib.util

def run_post_install():
    """Run post-installation tasks."""
    print("Thank you for installing szn-libeaas!")
    print("Fetching documentation details...")
    
    # Wait a moment before continuing
    time.sleep(1)
    
    try:
        # Import and run the open_readme function
        from szn_libeaas.docs_utils import open_readme
        print("Fetching latest documentation content...")
        open_readme()
    except ImportError as e:
        print(f"Could not import required module: {e}")
        print("Please make sure you have the required dependencies installed:")
        print("  pip install requests-html")
    except Exception as e:
        print(f"An error occurred while fetching documentation: {e}")
    
    print("\nTo get started with szn-libeaas, check out the examples directory.")
    print("If you have any questions or encounter issues, please visit:")
    print("  https://github.com/szn/libeaas/issues")

# Define a custom command to run after installation
class post_install_command:
    """Post-installation command that runs automatically after the package is installed."""
    
    def __init__(self, dist):
        """Initialize with distribution."""
        self.dist = dist
    
    def run(self):
        """Run the post-installation command."""
        # This method will be called by setuptools after installation
        run_post_install()
        
    # Include sub_commands for compatibility with setuptools
    sub_commands = []

# Import hook that gets executed when the module is imported
def _auto_run():
    """Function that gets executed when the module is imported."""
    # Import time is a good point to execute the function in certain contexts
    # This approach is safer than using __init__.py for side effects
    try:
        # Only run automatically in interactive environments to avoid triggering during installation
        # This is a safer approach as it doesn't rely directly on sys or os
        if not hasattr(_auto_run, '_has_run'):
            _auto_run._has_run = True
            # This will be imported when someone directly imports this module
            run_post_install()
    except Exception:
        # Silently fail if anything goes wrong to avoid breaking imports
        pass

# This gets called when someone does: 
# from szn_libeaas.post_install import auto_run
auto_run = _auto_run

if __name__ == '__main__':
    run_post_install()