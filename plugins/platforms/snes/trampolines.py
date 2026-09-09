class LLETrampoline:
    """Low-Level Emulation trampolines for switching between C patches and interpreter tier."""

    @staticmethod
    def generate_stub_code(bank: int, pc: int, variants: list[str]) -> str:
        lines = [f"// Unresolved trampoline for Bank 0x{bank:02X}, PC 0x{pc:04X}"]
        for var in variants:
            lines.append(f"void unresolved_stub_{bank:02x}_{pc:04x}_{var}(void) {{")
            lines.append(f"    interp_tier_dispatch_bank_miss(0x{bank:02X}{pc:04X});")
            lines.append("}")
        return "\n".join(lines)
