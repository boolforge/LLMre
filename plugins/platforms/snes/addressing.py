class ExLoROMMap:
    """ExLoROM SNES Memory Mapping ($C0-$FF)."""

    def __init__(self, rom_size: int = 0x600000):
        self.rom_size = rom_size

    def is_rom_address(self, full_addr: int) -> bool:
        bank = (full_addr >> 16) & 0xFF
        offset = full_addr & 0xFFFF
        if bank >= 0xC0 and bank <= 0xFF:
            return True
        if bank < 0x80 and offset >= 0x8000:
            return True
        return False

    def rom_offset(self, full_addr: int) -> int:
        bank = (full_addr >> 16) & 0xFF
        offset = full_addr & 0xFFFF
        if bank >= 0xC0:
            raw_bank = bank - 0xC0
            bank_offset = offset - 0x8000 if offset >= 0x8000 else offset
            return (raw_bank * 0x8000) + bank_offset
        elif bank < 0x80 and offset >= 0x8000:
            return (bank * 0x8000) + (offset - 0x8000)
        return offset
