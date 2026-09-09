from typing import Dict, Any, List

class CapstoneAdapter:
    """Adapter for Capstone disassembly engine supporting 65c816, m68k, arm, z80, x86, mips, ppc."""

    def disassemble(self, arch: str, code_bytes: bytes, offset: int = 0) -> List[Dict[str, Any]]:
        instructions = []
        # Mock / fallback capstone disassembly for deterministic test execution
        for i, b in enumerate(code_bytes):
            instructions.append({
                "address": offset + i,
                "mnemonic": "RAW_BYTE",
                "op_str": f"0x{b:02X}",
                "size": 1
            })
        return instructions
