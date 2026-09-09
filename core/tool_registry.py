"""
Central Plugin Tool Registry for Multi-Platform Framework.
"""

from typing import Dict, Any, Callable, Optional


class ToolRegistry:
    """Central registry for framework, CPU, and target platform tools."""

    def __init__(self):
        self._tools: Dict[str, Callable[..., Any]] = {}
        self._metadata: Dict[str, Dict[str, Any]] = {}

    def register_tool(self, name: str, category: str, description: str, func: Callable[..., Any]):
        """Register a tool with its execution function and schema metadata."""
        self._tools[name] = func
        self._metadata[name] = {
            "name": name,
            "category": category,
            "description": description
        }

    def execute_tool(self, name: str, **kwargs) -> Any:
        """Execute a registered tool by name."""
        if name not in self._tools:
            raise KeyError(f"Tool '{name}' is not registered in ToolRegistry.")
        return self._tools[name](**kwargs)

    def get_tool(self, name: str) -> Dict[str, Any]:
        """Get function and metadata for a registered tool."""
        if name not in self._tools:
            raise KeyError(f"Tool '{name}' is not registered in ToolRegistry.")
        return {
            "func": self._tools[name],
            "metadata": self._metadata[name]
        }

    def get_tool_metadata(self, name: str) -> Optional[Dict[str, Any]]:
        return self._metadata.get(name)

    def list_tools(self, category: Optional[str] = None) -> Dict[str, Dict[str, Any]]:
        if category:
            return {k: v for k, v in self._metadata.items() if v["category"] == category}
        return self._metadata
