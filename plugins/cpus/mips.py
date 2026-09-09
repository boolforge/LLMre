from dataclasses import dataclass

@dataclass
class CPUPatch:
    arch: str
    base_pc: int
    c_code: str

class RecompilerMIPS:
    def lift_block(self, asm_text: str, base_pc: int = 0) -> CPUPatch:
        c_lines = ["void mips_block(void) {"]
        for line in asm_text.strip().split("\n"):
            line = line.strip()
            if "LI $t0," in line:
                val = line.split(",")[1].strip()
                c_lines.append(f"    REG_R[8] = {val};")
            elif "JAL" in line:
                target = line.split()[1]
                c_lines.append(f"    call_mips({target});")
        c_lines.append("}")
        return CPUPatch(arch="MIPS", base_pc=base_pc, c_code="\n".join(c_lines))
