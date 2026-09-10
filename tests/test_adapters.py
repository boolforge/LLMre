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
    res = reagent.run_reagent_analysis("dummy.elf", arch="z80", strategy="global_registers")
    assert res["status"] == "SUCCESS"
    assert "prompt_profile" in res
    assert res["prompt_profile"]["arch"] == "z80"

    prompt = reagent.generate_retro_prompt(arch="6502", strategy="high_level_refactoring")
    assert "6502" in prompt["system_prompt"]
    assert prompt["strategy"] == "high_level_refactoring"

    val_ok = reagent.validate_with_retro_compiler("volatile uint8_t *reg = (uint8_t*)0x2100;\nvoid main() { *reg = 1; }", target_arch="6502")
    assert val_ok["status"] == "PASSED"

    val_bad = reagent.validate_with_retro_compiler("void main() { int *p = malloc(10); }", target_arch="z80")
    assert val_bad["status"] == "REJECTED"
    assert "forbidden" in val_bad["errors"][0]

    parity = reagent.verify_decompilation_parity("nop", "volatile uint8_t a = 0; void f() {}")
    assert parity["parity_exact"] == True
