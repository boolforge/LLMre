from typing import Dict, Any

class SA1Coprocessor:
    """SA-1 Parallel CPU & Shared Memory/IRQ messaging subsystem."""

    def __init__(self):
        self.shared_ram = bytearray(0x800) # 2KB Dual-port RAM
        self.sa1_pc = 0x0000
        self.irq_vector = 0x0000

    def write_shared_ram(self, offset: int, value: int):
        if 0 <= offset < len(self.shared_ram):
            self.shared_ram[offset] = value & 0xFF

    def read_shared_ram(self, offset: int) -> int:
        if 0 <= offset < len(self.shared_ram):
            return self.shared_ram[offset]
        return 0x00
