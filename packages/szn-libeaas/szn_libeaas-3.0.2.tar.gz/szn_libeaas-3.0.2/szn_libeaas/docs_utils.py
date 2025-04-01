"""
Documentation utilities for the szn-libeaas package.

This module provides utilities for accessing and displaying documentation.
"""
from typing import Optional


def open_readme() -> None:
    """
    Open and render the content of the documentation webpage.
    
    This function uses requests-html to fetch and render the documentation page.
    """
    from requests_html import HTMLSession
    
    session = HTMLSession()
    r = session.get("https://opicevopice.github.io/")
    r.html.render(sleep=2)
    print(r.html.html)