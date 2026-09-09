import pytest
from plugins.platforms.snes.addressing import ExLoROMMap
from plugins.platforms.snes.sdd1 import SDD1Decompressor
from plugins.platforms.snes.sa1 import SA1Coprocessor
from plugins.platforms.snes.spc700 import SPC700Audio
from plugins.platforms.msdos.msdos_engine import MSDOSEngine
from plugins.platforms.neogeo.neogeo_engine import NeoGeoEngine
from plugins.platforms.android.android_engine import AndroidEngine

def test_snes_exlorom_mapping():
    mapper = ExLoROMMap(rom_size=0x600000)
    assert mapper.is_rom_address(0xC00000) == True
    assert mapper.is_rom_address(0xC08000) == True
    assert mapper.rom_offset(0xC08000) == 0x0000
    assert mapper.rom_offset(0xC18000) == 0x8000

def test_snes_sdd1_decompression():
    sdd1 = SDD1Decompressor()
    compressed_data = bytes([0x01, 0x02, 0x03, 0x04])
    decomp = sdd1.decompress_stream(compressed_data, expected_size=8)
    assert len(decomp) == 8

def test_snes_sa1_coprocessor():
    sa1 = SA1Coprocessor()
    sa1.write_shared_ram(0x00, 0xAB)
    assert sa1.read_shared_ram(0x00) == 0xAB

def test_snes_spc700_audio():
    spc = SPC700Audio()
    spc.write_dsp(0x00, 0x7F)
    assert spc.read_dsp(0x00) == 0x7F
    assert spc.dropped_frames == 0

def test_msdos_engine():
    dos = MSDOSEngine()
    result = dos.emulate_interrupt(0x21, {"ah": 0x4C, "al": 0x00})
    assert result["exit_code"] == 0

def test_neogeo_engine():
    neogeo = NeoGeoEngine()
    addr = neogeo.map_address(0x1000)
    assert addr["space"] == "68000_PROGRAM"

def test_android_engine():
    android = AndroidEngine()
    symbols = android.lift_ndk_library(b"\x7fELFfake_so_bytes")
    assert symbols["status"] == "parsed"
