import pytest
from plugins.frameworks.capstone_adapter import CapstoneAdapter
from plugins.frameworks.asar_adapter import AsarAdapter
from plugins.frameworks.reko_adapter import RekoAdapter
from plugins.frameworks.retro_porting_toolkit import RetroPortingToolkitPlugin
from plugins.frameworks.reagent_adapter import ReagentAdapter

def test_capstone_adapter():
    cap = CapstoneAdapter()
    disasm = cap.disassemble("65c816", b"\xa9\x34\x12")
    assert len(disasm) > 0

def test_asar_adapter():
    asar = AsarAdapter()
    res = asar.assemble_patch("org $c08000\nlda #$1234", "dummy.sfc")
    assert res["success"] == True

def test_reko_adapter():
    reko = RekoAdapter()
    ir = reko.decompile_binary("dummy.exe", "x86")
    assert ir["format"] == "Reko_IR"

def test_rpt_adapter():
    rpt = RetroPortingToolkitPlugin()
    engine = rpt.get_engine("N64Recomp")
    assert engine is not None
    res = engine.recompile_rom("dummy.z64")
    assert res["status"] == "SUCCESS"

def test_reagent_adapter():
    reagent = ReagentAdapter()
    res = reagent.run_reagent_analysis("dummy.elf")
    assert res["status"] in ["SUCCESS", "fallback"]
    parity = reagent.verify_decompilation_parity("nop", "void f() {}")
    assert parity["parity_exact"] == True
