from dataclasses import dataclass, field
from typing import List

@dataclass
class CPUPatch:
    arch: str
    bank: int
    pc: int
    c_code: str
    called_targets: List[str] = field(default_factory=list)

class RecompilerM68k:
    def lift_block(self, asm_text: str, bank: int = 0, pc: int = 0, strategy: str = "global_registers") -> CPUPatch:
        called_targets = []
        c_lines = ["volatile uint32_t REG_D[8] = {0};", "void m68k_block(void) {"]
        for line in asm_text.strip().split("\n"):
            line = line.strip()
            if "MOVE.L" in line:
                val = line.split("#")[1].split(",")[0].replace("$", "0x")
                c_lines.append(f"    REG_D[0] = {val};")
            elif "JSR" in line:
                target = line.split()[1].replace("$", "0x")
                called_targets.append(target)
                c_lines.append(f"    call_m68k({target});")
        c_lines.append("}")
        return CPUPatch(arch="M68K", bank=bank, pc=pc, c_code="\n".join(c_lines), called_targets=called_targets)
