from dataclasses import dataclass, field
from typing import List

@dataclass
class CPUPatch:
    arch: str
    bank: int
    pc: int
    c_code: str
    called_targets: List[str] = field(default_factory=list)

class RecompilerZ80:
    def lift_block(self, asm_text: str, bank: int = 0, pc: int = 0, strategy: str = "global_registers") -> CPUPatch:
        called_targets = []
        if strategy == "global_registers":
            c_lines = ["volatile uint8_t REG_A = 0;", "void z80_block(void) {"]
        else:
            c_lines = ["void z80_block(uint8_t *a_reg) {"]

        for line in asm_text.strip().split("\n"):
            line = line.strip()
            if "LD A," in line:
                val = line.split(",")[1].strip().replace("$", "0x")
                c_lines.append(f"    REG_A = {val};" if strategy == "global_registers" else f"    *a_reg = {val};")
            elif "CALL" in line:
                target = line.split()[1].replace("$", "0x")
                called_targets.append(target)
                c_lines.append(f"    call_z80({target});")
        c_lines.append("}")
        return CPUPatch(arch="Z80", bank=bank, pc=pc, c_code="\n".join(c_lines), called_targets=called_targets)
