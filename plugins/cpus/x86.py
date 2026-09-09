from dataclasses import dataclass

@dataclass
class CPUPatch:
    arch: str
    base_pc: int
    c_code: str

class RecompilerX86:
    def lift_block(self, asm_text: str, base_pc: int = 0) -> CPUPatch:
        c_lines = ["void x86_block(void) {"]
        for line in asm_text.strip().split("\n"):
            line = line.strip()
            if "MOV EAX," in line:
                val = line.split(",")[1].strip()
                c_lines.append(f"    REG_EAX = {val};")
            elif "INT" in line:
                vec = line.split()[1]
                c_lines.append(f"    trigger_interrupt({vec});")
        c_lines.append("}")
        return CPUPatch(arch="x86", base_pc=base_pc, c_code="\n".join(c_lines))
