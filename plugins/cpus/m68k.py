from dataclasses import dataclass
from typing import List

@dataclass
class CPUPatch:
    arch: str
    base_pc: int
    c_code: str

class RecompilerM68k:
    def lift_block(self, asm_text: str, base_pc: int = 0) -> CPUPatch:
        c_lines = ["void m68k_block(void) {"]
        for line in asm_text.strip().split("\n"):
            line = line.strip()
            if "MOVE.L" in line:
                val = line.split("#")[1].split(",")[0].replace("$", "0x")
                c_lines.append(f"    REG_D[0] = {val};")
            elif "JSR" in line:
                target = line.split()[1].replace("$", "0x")
                c_lines.append(f"    call_m68k({target});")
        c_lines.append("}")
        return CPUPatch(arch="M68K", base_pc=base_pc, c_code="\n".join(c_lines))
