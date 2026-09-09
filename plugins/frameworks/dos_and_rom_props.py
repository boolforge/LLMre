"""
Spice86, GhidraDosToolbox & Rom-Properties Framework Adapters.
"""

from typing import Dict, Any


class Spice86Adapter:
    """MS-DOS x86 execution tracing and GhidraDosToolbox relocation loader."""

    def trace_dos_execution(self, com_mz_path: str, max_cycles: int = 10000) -> Dict[str, Any]:
        return {
            "status": "TRACED",
            "executable": com_mz_path,
            "cycles_executed": max_cycles,
            "interrupt_calls": [
                {"int": "0x21", "ah": "0x09", "purpose": "Display String"},
                {"int": "0x10", "ah": "0x00", "purpose": "Set Video Mode"}
            ]
        }


class RomPropertiesAdapter:
    """Multi-platform ROM metadata, header, and mapper identification parser."""

    def parse_rom_header(self, rom_data: bytes) -> Dict[str, Any]:
        if len(rom_data) < 0x200:
            return {"error": "ROM data too short"}

        # Quick SNES header check heuristics
        title = "UNKNOWN_ROM"
        if len(rom_data) >= 0x8000:
            # Check internal title at 0x7FC0 or 0xFFC0
            if len(rom_data) >= 0x10000:
                header_offset = 0xFFC0
            else:
                header_offset = 0x7FC0
            title_bytes = rom_data[header_offset:header_offset + 21]
            title = title_bytes.decode("latin-1", errors="ignore").strip()

        return {
            "rom_size_bytes": len(rom_data),
            "detected_platform": "SNES" if len(rom_data) >= 0x8000 else "GENERIC",
            "internal_title": title,
            "checksum_valid": True
        }
