"""
Core Schema Validator for LLM Determinism and AST Compliance.
"""

from typing import Dict, Any, Tuple, Optional
import json


TOOL_CALL_SCHEMA = {
    "type": "object",
    "properties": {
        "tool_name": {"type": "string"},
        "target_platform": {"type": "string"},
        "arguments": {"type": "object"}
    },
    "required": ["tool_name", "target_platform", "arguments"]
}

RECOMP_PATCH_SCHEMA = {
    "type": "object",
    "properties": {
        "address": {"type": "integer"},
        "bank": {"type": "integer"},
        "symbol_name": {"type": "string"},
        "c_code": {"type": "string"},
        "m_width": {"type": "boolean"},
        "x_width": {"type": "boolean"},
        "volatile_registers": {"type": "array", "items": {"type": "string"}}
    },
    "required": ["address", "symbol_name", "c_code"]
}


class SchemaValidator:
    """Validates intermediate representations, patch outputs, and tool requests."""

    @staticmethod
    def validate_dict(data: Dict[str, Any], schema: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """Validate a Python dictionary against a JSON schema-like specification."""
        reqs = schema.get("required", [])
        for req in reqs:
            if req not in data:
                return False, f"Missing required property: '{req}'"

        props = schema.get("properties", {})
        for key, val in data.items():
            if key in props:
                expected_type = props[key].get("type")
                if expected_type == "string" and not isinstance(val, str):
                    return False, f"Property '{key}' must be string, got {type(val).__name__}"
                elif expected_type == "integer" and not isinstance(val, int):
                    return False, f"Property '{key}' must be integer, got {type(val).__name__}"
                elif expected_type == "object" and not isinstance(val, dict):
                    return False, f"Property '{key}' must be dict, got {type(val).__name__}"
                elif expected_type == "array" and not isinstance(val, list):
                    return False, f"Property '{key}' must be list, got {type(val).__name__}"
                elif expected_type == "boolean" and not isinstance(val, bool):
                    return False, f"Property '{key}' must be bool, got {type(val).__name__}"

        return True, None

    @staticmethod
    def validate_patch(patch_data: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        return SchemaValidator.validate_dict(patch_data, RECOMP_PATCH_SCHEMA)

    @staticmethod
    def validate_tool_call(tool_data: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        return SchemaValidator.validate_dict(tool_data, TOOL_CALL_SCHEMA)
