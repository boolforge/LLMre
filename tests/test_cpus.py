import pytest
from plugins.cpus.c65c816 import Recompiler65c816
from plugins.cpus.m68k import RecompilerM68k
from plugins.cpus.arm import RecompilerARM
from plugins.cpus.z80 import RecompilerZ80
from plugins.cpus.x86 import RecompilerX86
from plugins.cpus.mips import RecompilerMIPS
from plugins.cpus.ppc import RecompilerPPC

def test_65c816_recompiler():
    recomp = Recompiler65c816()
    raw_asm = """
    REP #$30
    LDA #$1234
    JSL $C08000
    RTS
    """
    patch = recomp.lift_block(raw_asm, bank=0xC0, pc=0x8000, m_flag=0, x_flag=0)
    assert patch.bank == 0xC0
    assert "REG_A = 0x1234" in patch.c_code
    assert "interp_tier_dispatch_bank_miss" in patch.c_code or "c_C08000" in patch.c_code

def test_m68k_recompiler():
    recomp = RecompilerM68k()
    raw_asm = "MOVE.L #$12345678, D0\nJSR $1000"
    patch = recomp.lift_block(raw_asm, base_pc=0x1000)
    assert patch.arch == "M68K"
    assert "REG_D[0] = 0x12345678" in patch.c_code

def test_arm_recompiler():
    recomp = RecompilerARM()
    raw_asm = "MOV R0, #42\nBL 0x8000"
    patch = recomp.lift_block(raw_asm, base_pc=0x8000)
    assert patch.arch == "ARM"
    assert "REG_R[0] = 42" in patch.c_code

def test_z80_recompiler():
    recomp = RecompilerZ80()
    raw_asm = "LD A, $FF\nCALL $0038"
    patch = recomp.lift_block(raw_asm, base_pc=0x0000)
    assert patch.arch == "Z80"
    assert "REG_A = 0xFF" in patch.c_code

def test_x86_recompiler():
    recomp = RecompilerX86()
    raw_asm = "MOV EAX, 0x1\nINT 0x21"
    patch = recomp.lift_block(raw_asm, base_pc=0x100)
    assert patch.arch == "x86"
    assert "REG_EAX = 0x1" in patch.c_code

def test_mips_recompiler():
    recomp = RecompilerMIPS()
    raw_asm = "LI $t0, 100\nJAL 0x80001000"
    patch = recomp.lift_block(raw_asm, base_pc=0x80000000)
    assert patch.arch == "MIPS"
    assert "REG_R[8] = 100" in patch.c_code

def test_ppc_recompiler():
    recomp = RecompilerPPC()
    raw_asm = "LI r3, 1\nBL 0x80000200"
    patch = recomp.lift_block(raw_asm, base_pc=0x80000000)
    assert patch.arch == "PPC"
    assert "REG_R[3] = 1" in patch.c_code
