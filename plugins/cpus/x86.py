from dataclasses import dataclass, field
from typing import List

@dataclass
class CPUPatch:
    arch: str
    bank: int
    pc: int
    c_code: str
    called_targets: List[str] = field(default_factory=list)

class RecompilerX86:
    def lift_block(self, asm_text: str, bank: int = 0, pc: int = 0, strategy: str = "global_registers") -> CPUPatch:
        called_targets = []
        c_lines = ["volatile uint32_t REG_EAX = 0;", "void x86_block(void) {"]
        for line in asm_text.strip().split("\n"):
            line = line.strip()
            if "MOV EAX," in line:
                val = line.split(",")[1].strip()
                c_lines.append(f"    REG_EAX = {val};")
            elif "INT" in line:
                vec = line.split()[1]
                called_targets.append(vec)
                c_lines.append(f"    trigger_interrupt({vec});")
        c_lines.append("}")
        return CPUPatch(arch="x86", bank=bank, pc=pc, c_code="\n".join(c_lines), called_targets=called_targets)
