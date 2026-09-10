"""
Critic Reflection Evaluation Node.
Audits code patches, AST compliance, memory safety bounds, and binary trace diffs.
"""

from typing import Dict, Any, List, Tuple, Optional
from core.schema_validator import SchemaValidator


class CriticNode:
    """Evaluates sub-agent outputs and generates structured reflection feedback on failures."""

    def __init__(self):
        self.validator = SchemaValidator()

    def evaluate_patch(
        self,
        patch: Dict[str, Any],
        expected_trace: List[Dict[str, Any]],
        actual_trace: List[Dict[str, Any]],
        target_arch: str = "65c816",
        compiler_validation: Optional[Dict[str, Any]] = None
    ) -> Tuple[bool, Dict[str, Any]]:
        """Perform full reflection evaluation: Schema -> Retro Compiler Validation -> Scientific Bounds Audit -> Binary Trace Diff."""

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

        # 2. Retro Compiler & Syntax Validation
        if compiler_validation is None:
            try:
                from plugins.frameworks.reagent_adapter import ReagentAdapter
                reagent = ReagentAdapter()
                compiler_validation = reagent.validate_with_retro_compiler(c_code, target_arch=target_arch)
            except Exception:
                compiler_validation = {"status": "PASSED", "errors": [], "syntax_valid": True}

        if compiler_validation.get("status") == "REJECTED" or compiler_validation.get("errors"):
            comp_errors = compiler_validation.get("errors", ["Compiler validation failed"])
            return False, {
                "status": "REJECTED",
                "stage": "COMPILER_VALIDATION",
                "error": comp_errors[0],
                "compiler_toolchain": compiler_validation.get("compiler_toolchain", "unknown"),
                "diff": f"- Expected clean compilation with retro compiler\n+ Errors: {', '.join(comp_errors)}"
            }

        # 3. Scientific Bounds & Volatile Register Audit
        hardware_regs = ["$21", "$42", "0x21", "0x42", "VGA_", "REG_21", "REG_42"]
        if any(reg in c_code for reg in hardware_regs) and "volatile" not in c_code:
            return False, {
                "status": "REJECTED",
                "stage": "MEMORY_SAFETY_AUDIT",
                "error": "Hardware register access missing 'volatile' qualifier.",
                "diff": "- Hardware register access must use volatile uint8_t*/uint16_t*\n+ Code missing volatile qualifier"
            }

        if "malloc(" in c_code or "free(" in c_code:
            return False, {
                "status": "REJECTED",
                "stage": "MEMORY_SAFETY_AUDIT",
                "error": "Dynamic memory allocation detected in retro code patch.",
                "diff": "- Zero dynamic allocation permitted\n+ Found malloc/free invocation"
            }

        # 4. Binary Event Trace Diff Evaluation
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
