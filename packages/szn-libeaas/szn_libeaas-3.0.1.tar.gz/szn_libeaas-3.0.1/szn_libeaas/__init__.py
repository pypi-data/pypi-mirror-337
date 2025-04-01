"""
szn-libeaas - Enterprise as a Service Library
==============================================

A Python API package providing Enterprise as a Service functionality.
"""

__version__ = '3.0.1'
__author__ = 'SZN Team'

# Import main API components to make them available at the top level
from .core import Client, APIResponse, APIError
from .auth import Authentication, TokenManager
from .endpoints import ResourceManager
from .utils import Logger, ConfigManager, DataFormatter
from .docs_utils import open_readme

# Import auto_loader to trigger the open_readme function automatically
# This import has a side effect of running the open_readme function
import szn_libeaas.auto_loader

# Define package exports
__all__ = [
    'Client',
    'APIResponse',
    'APIError',
    'Authentication',
    'TokenManager',
    'ResourceManager',
    'Logger',
    'ConfigManager',
    'DataFormatter',
    'open_readme',
]