from dataclasses import dataclass

@dataclass
class CPUPatch:
    arch: str
    base_pc: int
    c_code: str

class RecompilerARM:
    def lift_block(self, asm_text: str, base_pc: int = 0) -> CPUPatch:
        c_lines = ["void arm_block(void) {"]
        for line in asm_text.strip().split("\n"):
            line = line.strip()
            if "MOV R0," in line:
                val = line.split("#")[1]
                c_lines.append(f"    REG_R[0] = {val};")
            elif "BL" in line:
                target = line.split()[1]
                c_lines.append(f"    call_arm({target});")
        c_lines.append("}")
        return CPUPatch(arch="ARM", base_pc=base_pc, c_code="\n".join(c_lines))
