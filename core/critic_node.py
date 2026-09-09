"""
Critic Reflection Evaluation Node.
Audits code patches, AST compliance, memory safety bounds, and binary trace diffs.
"""

from typing import Dict, Any, List, Tuple
from core.schema_validator import SchemaValidator


class CriticNode:
    """Evaluates sub-agent outputs and generates structured reflection feedback on failures."""

    def __init__(self):
        self.validator = SchemaValidator()

    def evaluate_patch(
        self,
        patch: Dict[str, Any],
        expected_trace: List[Dict[str, Any]],
        actual_trace: List[Dict[str, Any]]
    ) -> Tuple[bool, Dict[str, Any]]:
        """Perform full reflection evaluation: Schema -> Memory Bounds -> Binary Trace Diff."""

        # 1. Schema Validation
        valid_schema, schema_err = self.validator.validate_patch(patch)
        if not valid_schema:
            return False, {
                "status": "REJECTED",
                "stage": "SCHEMA_VALIDATION",
                "error": schema_err,
                "diff": f"- Expected valid patch schema\n+ Got error: {schema_err}"
            }

        c_code = patch.get("c_code", "")

        # 2. Memory Safety & Volatile Qualification
        if "volatile" not in c_code and any(reg in c_code for reg in ["$21", "$42", "VGA_"]):
            return False, {
                "status": "REJECTED",
                "stage": "MEMORY_SAFETY_AUDIT",
                "error": "Hardware register access missing 'volatile' qualifier.",
                "diff": "- Hardware register access must use volatile uint8_t*/uint16_t*\n+ Code missing volatile qualifier"
            }

        # 3. Binary Event Trace Diff Evaluation
        if expected_trace != actual_trace:
            diff_lines = []
            min_len = min(len(expected_trace), len(actual_trace))
            for idx in range(min_len):
                exp = expected_trace[idx]
                act = actual_trace[idx]
                if exp != act:
                    diff_lines.append(f"Trace index {idx} mismatch:")
                    diff_lines.append(f"  Expected: {exp}")
                    diff_lines.append(f"  Actual:   {act}")

            if len(expected_trace) != len(actual_trace):
                diff_lines.append(f"Trace length mismatch: Expected {len(expected_trace)}, got {len(actual_trace)}")

            return False, {
                "status": "REJECTED",
                "stage": "BINARY_TRACE_DIFF",
                "error": "Execution trace divergence detected.",
                "diff": "\n".join(diff_lines)
            }

        return True, {
            "status": "PASSED",
            "stage": "CRITIC_APPROVAL",
            "message": "Patch passed schema, memory safety, and bit-exact trace diff validation."
        }
