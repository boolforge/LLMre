from dataclasses import dataclass, field
from typing import List

@dataclass
class CPUPatch:
    arch: str
    bank: int
    pc: int
    c_code: str
    called_targets: List[str] = field(default_factory=list)

class RecompilerARM:
    def lift_block(self, asm_text: str, bank: int = 0, pc: int = 0, strategy: str = "global_registers") -> CPUPatch:
        called_targets = []
        c_lines = ["volatile uint32_t REG_R[16] = {0};", "void arm_block(void) {"]
        for line in asm_text.strip().split("\n"):
            line = line.strip()
            if "MOV R0," in line:
                val = line.split("#")[1]
                c_lines.append(f"    REG_R[0] = {val};")
            elif "BL" in line:
                target = line.split()[1]
                called_targets.append(target)
                c_lines.append(f"    call_arm({target});")
        c_lines.append("}")
        return CPUPatch(arch="ARM", bank=bank, pc=pc, c_code="\n".join(c_lines), called_targets=called_targets)
