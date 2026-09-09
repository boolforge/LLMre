from dataclasses import dataclass

@dataclass
class CPUPatch:
    arch: str
    base_pc: int
    c_code: str

class RecompilerZ80:
    def lift_block(self, asm_text: str, base_pc: int = 0) -> CPUPatch:
        c_lines = ["void z80_block(void) {"]
        for line in asm_text.strip().split("\n"):
            line = line.strip()
            if "LD A," in line:
                val = line.split(",")[1].strip().replace("$", "0x")
                c_lines.append(f"    REG_A = {val};")
            elif "CALL" in line:
                target = line.split()[1].replace("$", "0x")
                c_lines.append(f"    call_z80({target});")
        c_lines.append("}")
        return CPUPatch(arch="Z80", base_pc=base_pc, c_code="\n".join(c_lines))
