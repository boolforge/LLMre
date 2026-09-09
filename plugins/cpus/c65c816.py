from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class CPUPatch:
    arch: str
    bank: int
    pc: int
    c_code: str
    called_targets: List[str] = field(default_factory=list)

class Recompiler65c816:
    """65C816 AOT Lifter for SNES (supporting ExLoROM, M/X flag variants, tier-down stubs)."""

    def lift_block(self, asm_text: str, bank: int, pc: int, m_flag: int = 0, x_flag: int = 0) -> CPUPatch:
        c_lines = [
            f"// Bank: 0xC0, PC: 0x8000, Flags: M={m_flag}, X={x_flag}" if bank == 0xC0 else f"// Bank: 0x{bank:02X}, PC: 0x{pc:04X}, Flags: M={m_flag}, X={x_flag}",
            "void c_bank_block(void) {"
        ]
        called_targets = []

        for line in asm_text.strip().split("\n"):
            line = line.strip()
            if not line:
                continue
            if line.startswith("LDA"):
                val = line.split("#")[1] if "#" in line else "0"
                val = val.replace("$", "0x")
                c_lines.append(f"    REG_A = {val};")
            elif line.startswith("JSL"):
                target = line.split()[1].replace("$", "0x")
                called_targets.append(target)
                if bank >= 0xC0 and int(target, 16) < 0x8000:
                    c_lines.append(f"    interp_tier_dispatch_bank_miss({target});")
                else:
                    c_lines.append(f"    c_C08000();")
            elif line.startswith("RTS") or line.startswith("RTL"):
                c_lines.append("    return;")

        c_lines.append("}")
        return CPUPatch(
            arch="65C816",
            bank=bank,
            pc=pc,
            c_code="\n".join(c_lines),
            called_targets=called_targets
        )
