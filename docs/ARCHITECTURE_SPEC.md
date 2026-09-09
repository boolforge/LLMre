# Multi-Platform Reverse Engineering, Decompression, and AOT Recompilation Engine Architecture & Technical Specification

## 1. Executive Summary & System Philosophy

This framework establishes a deterministic, token-efficient, and modular multi-platform platform for reverse engineering, asset decompression, and Ahead-Of-Time (AOT) static/dynamic recompilation.

Designed for tight integration with Large Language Models (LLMs), the system guarantees **100% LLM determinism** through:
- **Strict AST and JSON Schema Validation:** Every tool invocation, code patch, and intermediate representation (IR) is validated against schema definitions prior to execution.
- **Micro-Prompt Context Compression:** Context windows passed to worker sub-agents are stripped of extraneous metadata, extracting only explicit variables, address maps, and disassemblies.
- **Critic Reflection Evaluation Loop:** Before any task is completed, a dedicated Critic agent evaluates output against structural invariants and binary trace diffs, executing automated retry loops on schema or trace failures.
- **Massive Code & Pattern Reuse:** Synthesizes patterns and capabilities from `RetroPortingToolkit` (N64Recomp, DolRecomp, GBARecomp, NESRecomp, SegaGenesisRecomp, PSXRecomp, CDiRecomp, RT64, GhidrAssistMCP, FreeBIOS, GCNLLE, XboxLLE), `m68k-recomp-core`, `arm-recomp-core`, `z80-recomp-core`, `Ghidra`, `Capstone`, `Asar`, `Reko`, `Spice86`, `GhidraDosToolbox`, `RetroGhidra`, `rom-properties`, and `agent-nexus`.

---

## 2. Agent Orchestration, Schema Validation & Critic Reflection Loop

```
+---------------------------------------------------------------------------------+
|                                 USER INPUT / CLI                                |
+---------------------------------------------------------------------------------+
                                         |
                                         v
+---------------------------------------------------------------------------------+
|                       Central Tool Registry & Manager Node                      |
|                     (Micro-Prompt Context Window Compression)                   |
+---------------------------------------------------------------------------------+
                                         |
                       +-----------------+-----------------+
                       |                                   |
                       v                                   v
+---------------------------------------------+ +----------------------------------+
|               Worker Sub-Agent              | |         Worker Sub-Agent         |
|         (Decompilation / Recompilation)     | |      (Decompression / AST)      |
+---------------------------------------------+ +----------------------------------+
                       |                                   |
                       +-----------------+-----------------+
                                         |
                                         v
+---------------------------------------------------------------------------------+
|                          AST / JSON Schema Validator                            |
+---------------------------------------------------------------------------------+
                                         |
                                         v
+---------------------------------------------------------------------------------+
|                        Critic Reflection Evaluation Node                        |
|             (Validates AST, Schema, Memory Bounds & Binary Trace Diffs)          |
+---------------------------------------------------------------------------------+
                                         |
                   +---------------------+---------------------+
                   | (Fail: Diff/Schema Error)                 | (Pass)
                   v                                           v
+-------------------------------------+      +------------------------------------+
|  Unified Diff / Reflection Feedback |      |        Final Execution / Patch      |
|           Returned to Manager       |      +------------------------------------+
+-------------------------------------+
```

### 2.1 Micro-Prompt Context Slicing
To minimize latency and token expenditure, context payloads passed to sub-agents contain solely:
1. Target memory address range / bank identifier.
2. Disassembled opcode instructions or C function AST node.
3. Explicit register state flags (`M`/`X` CPU widths, segment registers).
4. Local symbol table entries.

All global system prompts, full trace logs, and external file hierarchies remain sequestered in the Manager state.

### 2.2 Critic Reflection Evaluation Node
The Critic Node intercepts all generated code, trampolines, and IR patches. It performs:
1. **Schema Compliance:** Validates JSON/AST payload structure against formal schemas.
2. **Memory Safety Audit:** Asserts bounds checks on SRAM/WRAM access and verifies `volatile` qualifiers on hardware I/O registers ($21xx, $42xx, VGA ports, etc.).
3. **Binary Event-Stream Trace Diffing:** Compares execution trace events (register writes, DMA transfers, IRQ triggers) against gold baseline binary event logs.
4. **Reflection Feedback:** On divergence, generates a structured unified diff containing exact byte offsets, expected vs. actual values, and stack pointer state.

---

## 3. Tool Registry & Framework Ecosystem Integration

The framework implements an extensible Plugin Architecture divided into:
- **`plugins/frameworks/`**: Decompilation, disassembling, and build toolchain adapters.
- **`plugins/cpus/`**: Architecture-specific instruction set disassemblers, IR lifters, and C/C++ code generators.
- **`plugins/platforms/`**: Console/OS specific memory mappers, coprocessors, graphics, audio, and I/O hardware emulators.

### 3.1 Framework Adapters
- **RetroPortingToolkit Adapter:** Unified integration with `N64Recomp`, `DolRecomp`, `NESRecomp`, `GBARecomp`, `SegaGenesisRecomp`, `VBRecomp`, `NDSRecomp`, `PSXRecomp`, `CDiRecomp`, `RT64`, `GhidrAssistMCP`, `FreeBIOS`, `GCNLLE`, and `XboxLLE`.
- **Ghidra Adapter & Ghidra-65816 / Ghidra-SNES-Loader:** Headless script execution for automated disassembling, symbol export, and C decompiler IR extraction.
- **Reko & Capstone Adapters:** Multi-architecture static lifting and disassembly fallback.
- **Asar Assembler Plugin:** Native SNES patch assembly and symbol table generation.
- **Spice86 / GhidraDosToolbox Plugin:** MS-DOS 16-bit x86 execution tracing, segment relocation mapping, and BIOS interrupt hooks.
- **Rom-Properties Plugin:** Automatic ROM header parsing, mapper identification, checksum verification, and chip detector across all supported systems.

---

## 4. CPU Recompiler Cores (`plugins/cpus/`)

Portable CPU lifter modules convert architecture-specific opcode streams into typed C IR:
- **`65c816-recomp-core`:** 65C816 CPU engine supporting 8-bit/16-bit dynamic accumulator ($M$) and index ($X$) widths, status flag tracking (`REP`/`SEP`), and stack-pushed status register reconstruction (`PHP`/`PLP`/`RTI`).
- **`m68k-recomp-core`:** Motorola 68000/68020 engine handling supervisor modes, exception vectors, bit manipulation, and 16/32-bit register context marshalling.
- **`arm-recomp-core`:** ARM32 / THUMB / ARM64 engine with condition code lifting, pipeline emulation, and Dalvik/ELF DEX interop.
- **`z80-recomp-core`:** Zilog Z80 engine for NES/Game Boy/Sega Genesis audio CPUs and NeoGeo sound control.
- **`mips-recomp-core`:** MIPS III (R4300i) engine for N64/PSX AOT recompilation.
- **`ppc-recomp-core`:** PowerPC 750CL / Broadway engine for GameCube/Wii.
- **`x86-recomp-core`:** 16-bit Real Mode and 32-bit Protected Mode x86 engine for MS-DOS executables.

---

## 5. Deep SNES Target Engine Subsystem (`plugins/platforms/snes/`)

The SNES reference module provides hardware-level static recompilation capabilities specifically engineered for complex cartridges such as **Star Ocean** and **Street Fighter Alpha 2**.

```
+---------------------------------------------------------------------------------+
|                             SNES Target Platform                                |
+---------------------------------------------------------------------------------+
|                                                                                 |
|  +---------------------+  +----------------------+  +------------------------+  |
|  | Memory Mapper       |  | Coprocessor Engine   |  | CPU Engine             |  |
|  | - LoROM / HiROM     |  | - S-DD1 Decompressor |  | - 65C816 Disassembler  |  |
|  | - ExLoROM ($C0-$FF) |  | - SA-1 Parallel CPU  |  | - REP/SEP Width Switch |  |
|  | - ExHiROM           |  | - Super FX / GSU     |  | - PHP/PLP/RTI Stack    |  |
|  | - BS-X / MMC        |  | - Cx4 / DSP-1..4     |  |   Status Tracker       |  |
|  +---------------------+  +----------------------+  +------------------------+  |
|                                                                                 |
|  +---------------------+  +----------------------+  +------------------------+  |
|  | Audio Engine        |  | PPU / Graphics       |  | Tier-Down LLE          |  |
|  | - SPC700 Core       |  | - Mode 7 Matrix      |  |   Trampolines          |  |
|  | - S-DSP BRR Decode  |  | - PPU Register Latch |  | - Register Context     |  |
|  | - $2140-$2143 Ring  |  | - HDMA Scroll Tables |  |   Marshalling ABI      |  |
|  +---------------------+  +----------------------+  +------------------------+  |
|                                                                                 |
|  +---------------------------------------------------------------------------+  |
|  |                  Binary Event-Stream Trace Audit Engine                   |  |
|  +---------------------------------------------------------------------------+  |
+---------------------------------------------------------------------------------+
```

### 5.1 Memory Mappers & Memory-Mapped I/O
- **Mappers Supported:** LoROM, HiROM, ExLoROM (`$C00000-$FFFFFF`), ExHiROM, SuperMMC, BS-X, Sufami Turbo.
- **Address Resolution:** Addresses in ExLoROM space (`$C0-$FF`) retain cross-bank `JSL`/`JSR` call targets below `$8000`. Memory checks query `is_rom_address` and `rom_offset` dynamically.
- **Safety Assertions:** All WRAM (`$7E0000-$7FFFFF`) and SRAM writes are wrapped in compile-time static assertions and runtime range guards.

### 5.2 Coprocessors & S-DD1 Hardware Decompression
- **S-DD1 Coprocessor:** Real-time hardware decompression emulation for registers `$4800-$4807`.
- **DMA Latching Protocol:** Tracks S-DD1 DMA channel latch states to ensure asynchronous DMA graphics transfers do not corrupt PPU VRAM during frame rendering.
- **Additional Coprocessors:** SA-1 (parallel 65C816 at 10.74 MHz, custom DMA, variable length bit processing), Super FX / GSU-1/2 (RISC math pipeline), Cx4 (wireframe math), DSP-1/2/3/4, OBC1, S-RTC, ST010/011/018.

### 5.3 65C816 CPU & PHP/PLP/RTI Dynamic Stack Tracking
- **Width States:** Handles all 4 CPU register width combinations (`M0X0`, `M0X1`, `M1X0`, `M1X1`) set by `REP`/`SEP`.
- **Stack Status Tracking:** Dynamically traces stack pushes (`PHP`, `PEA`, `PHB`, `PHK`, `PHA`, `PHX`, `PHY`) and stack pulls (`PLP`, `PLA`, `PLX`, `PLY`, `RTI`). Restores exact $M$/$X$ register width flags upon returning from IRQ/NMI or subroutines.

### 5.4 Audio SPC700 & S-DSP Synchronization
- **Sound Core:** SPC700 8-bit MCU and S-DSP BRR sample decoding.
- **IPC Ring-Buffer:** Synchronizes hardware communication ports `$2140-$2143` with zero dropped sound frames, eliminating audio buffer starvation (`hiwater` overflow).

### 5.5 Tier-Down LLE Context Marshalling Trampolines
When calling functions in uncompiled or partially compiled banks (e.g., `$C9`, `$CB`), the recompiler context-switches via an ABI trampoline:
```c
typedef struct {
    uint16_t A, X, Y, S, D;
    uint8_t PB, DB, P;
} CPU65C816State;

void lle_trampoline_dispatch(CPU65C816State *cpu, uint32_t target_address);
```
Preserves exact CPU register width, data bank ($DB$), and program bank ($PB$) alignment across execution tier boundaries.

### 5.6 Binary Event-Stream Trace Auditing
Replaces non-deterministic plain-text log searches (`rg.exe`) with structured binary event-stream logging:
- Logs hardware writes (`$21xx`, `$42xx`), DMA channels, PPU frame latches, and SPC700 IPC exchanges as fixed-size 64-bit binary trace records.
- Performs byte-exact binary trace diffing against gold references with millisecond phase alignment.

---

## 6. Multi-Platform Extension Modules

### 6.1 MS-DOS / x86 PC Module (`plugins/platforms/msdos/`)
- 16-bit Real Mode MZ / COM executable parser.
- Segment relocation table mapping (`CS:IP`, `DS`, `ES`, `SS:SP`).
- BIOS/DOS interrupt trampolines (`INT 10h` video, `INT 21h` file I/O).
- VGA $3Cx register emulation and direct frame-buffer surface mapping.

### 6.2 NeoGeo Module (`plugins/platforms/neogeo/`)
- M68000 main CPU and Z80 sound CPU execution pipelines.
- YM2610 FM/ADPCM audio decoding.
- NeoGeo BIOS vector dispatch and Fix/Sprite tile graphics renderer.

### 6.3 Android / ARM Module (`plugins/platforms/android/`)
- Dalvik DEX bytecode parser and ARM32/ARM64 AOT lifting.
- ELF dynamic symbol linkage and JNI C/C++ boundary marshalling.

---

## 7. Verification and Test Protocol

The test suite in `tests/` enforces:
1. **Schema Integrity:** 100% compliance of tool requests and outputs against JSON schemas.
2. **Context Efficiency:** Verifies micro-prompts stay under strict character limits.
3. **Critic Loop Accuracy:** Simulates syntax and trace errors to verify auto-repair generation.
4. **SNES Coprocessor & Recompiler Tests:** Unit tests for 65C816 disassembly, S-DD1 decompression, SA-1 DMA, SPC700 IPC, and ExLoROM trampoline dispatch.
5. **MS-DOS & NeoGeo Tests:** Verifies x86 MZ header parsing, DOS interrupt trapping, and M68K disassembly.
