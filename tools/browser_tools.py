"""Browser interaction tools for GenericAgent using TMWebDriver."""

from TMWebDriver import Session
from typing import Optional

# Tool schemas for LLM function calling
TOOL_SCHEMAS = [
    {
        "name": "navigate",
        "description": "Navigate the browser to a given URL.",
        "parameters": {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "The URL to navigate to."
                }
            },
            "required": ["url"]
        }
        "name": "click",
        "description": "Click on an element identified by a CSS selector or XPath.",
        "parameters": {
            "type": "object",
            "properties": {
                "selector": {
                    "type": "string",
                    "description": "CSS selector or XPath of the element to click."
                }
            },
            "required": ["selector"]
        }
    },
    {
        "name": "type_text",
        "description": "Type text into an input field identified by a CSS selector.",
        "parameters": {
            "type": "object",
            "properties": {
                "selector": {
                    "type": "string",
                    "description": "CSS selector of the input element."
                },
                "text": {
                    "type": "string",
                    "description": "The text to type into the field."
                },
                "clear_first": {
                    "type": "boolean",
                    "description": "Whether to clear the field before typing. Defaults to true."
                }
            },
            "required": ["selector", "text"]
        }
    },
    {
        "name": "get_page_content",
        "description": "Get the visible text content or HTML of the current page.",
        "parameters": {
            "type": "object",
            "properties": {
                "as_html": {
                    "type": "boolean",
                    "description": "If true, return raw HTML. Otherwise return visible text. Defaults to false."
                }
            },
            "required": []
        }
    },
    {
        "name": "get_current_url",
        "description": "Get the current URL of the browser.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    }
]


class BrowserTools:
    """Wraps TMWebDriver. Exposes browser actions as agent-callable tools."""

    def __init__(self, session: Session):
        self.session = session

    def navigate(self, url: str) -> str:
        """Navigate to a URL and return confirmation."""
        self.session.url = url
        return f"Navigated to {url}"

    def click(self, selector: str) -> str:
        """Click an element by CSS selector or XPath."""
        try:
            el = self.session.find(selector)
            el.click()
            return f"}"
        except Exception as e:
            return f"Failed to click '{selector}': {e}"

    def type_text(self, selector: str, text: str, clear_first: bool = True) -> str:
        """Type text into an input field."""
        try:
            el = self.session.find(selector)
            if clear_first:
                el.clear()
            el.send_keys(text)
            return f"Typed text into '{selector}'"
        except Exception as e:
            return f"Failed to type into '{selector}': {e}"

    def get_page_content(self, as_html: bool = False) -> str:
        """Get the current page content as text or HTML."""
        if as_html:
            return self.session.page_source
        # Return visible text; strip excessive whitespace for cleaner output
        return self.session.find('body').text.strip()

    def get_current_url(self) -> str:
        """Return the current URL."""
        return self.session.url
