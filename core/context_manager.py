"""
Micro-Prompt Context Compression Manager.
Filters and strips large context windows down to minimal explicit variables.
"""

from typing import Dict, Any, List


class ContextManager:
    """Slices context windows down to micro-prompts for worker sub-agents."""

    @staticmethod
    def slice_disassembly_context(
        address: int,
        bank: int,
        opcodes: List[Dict[str, Any]],
        symbols: Dict[int, str],
        m_flag: bool,
        x_flag: bool
    ) -> Dict[str, Any]:
        """Produce a compressed payload containing only explicit variables needed by worker sub-agents."""
        compact_opcodes = []
        for op in opcodes:
            compact_opcodes.append({
                "addr": hex(op.get("address", 0)),
                "mnemonic": op.get("mnemonic", ""),
                "operands": op.get("operands", "")
            })

        relevant_symbols = {
            hex(addr): sym for addr, sym in symbols.items()
            if abs(addr - address) < 0x1000
        }

        return {
            "target": f"${bank:02X}:{address:04X}",
            "opcodes": compact_opcodes,
            "cpu_state": {"M": m_flag, "X": x_flag},
            "local_symbols": relevant_symbols
        }

    @staticmethod
    def slice_patch_context(c_patch: str, target_symbol: str) -> Dict[str, Any]:
        """Compress C patch for Critic validation."""
        lines = [line.strip() for line in c_patch.splitlines() if line.strip()]
        return {
            "symbol": target_symbol,
            "loc": len(lines),
            "code_snippet": "\n".join(lines[:50])
        }
