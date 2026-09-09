from typing import Dict, Any

class NeoGeoEngine:
    """NeoGeo arcade platform memory & sprite tile mapping engine."""

    def map_address(self, addr: int) -> Dict[str, Any]:
        if addr < 0x100000:
            return {"space": "68000_PROGRAM", "offset": addr}
        elif 0x400000 <= addr < 0x402000:
            return {"space": "PALETTE_RAM", "offset": addr - 0x400000}
        return {"space": "WORK_RAM", "offset": addr}
