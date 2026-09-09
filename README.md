# Multi-Platform Reverse Engineering, Asset Decompression, and AOT Recompilation Framework

An open, deterministic, token-efficient, and pluggable framework for static/dynamic reverse engineering, asset decompression, and Ahead-Of-Time (AOT) binary recompilation. Designed with native support for Large Language Model (LLM) agents, strict AST/JSON schema validation, micro-prompt context window slicing, and a dedicated **Critic Reflection Evaluation Loop**.

---

## Key Architecture & Features

### 1. Deterministic LLM Agent & Micro-Prompt Slicing
- **Micro-Prompt Context Manager:** Context payloads passed to sub-agents contain only address ranges, disassembled opcode streams, and symbol tables, preventing token window exhaustion and reducing latency.
- **Strict AST / JSON Schema Validation:** Every tool invocation and code patch is validated against schemas prior to execution.
- **Critic Reflection Evaluation Node:** Intercepts generated code, trampolines, and IR patches to evaluate schema compliance, memory safety bounds, and binary event-stream trace diffs. Returns structured unified diff feedback on failures.

### 2. Deep SNES Target Subsystem (`plugins/platforms/snes/`)
- **Memory Mappers:** LoROM, HiROM, ExLoROM (`$C00000-$FFFFFF`), ExHiROM, SuperMMC, BS-X, Sufami Turbo.
- **65C816 Engine:** Dynamic accumulator ($M$) and index ($X$) width tracking (`REP`/`SEP`), along with dynamic status register stack tracking (`PHP`/`PLP`/`RTI`).
- **Coprocessor Suite:**
  - **S-DD1:** Real-time hardware graphics decompression ($4800-$4807) with DMA latch tracking.
  - **SA-1:** Parallel 10.74 MHz 65C816 CPU, custom DMA, and variable bit processing.
  - **Super FX / GSU-1/2, Cx4, DSP-1..4, OBC1, S-RTC, ST010/011/018.**
- **Audio SPC700 & S-DSP:** Zero-dropped-frame IPC ring-buffer ($2140-$2143) synchronization.
- **Tier-Down LLE Trampolines:** ABI context marshalling (`CPU65C816State`) for execution fallback into unresolved banks.
- **Binary Event-Stream Trace Auditing:** Byte-exact 64-bit binary trace logging and diffing.

### 3. RetroPortingToolkit & Multi-Platform Framework Ecosystem
- **RetroPortingToolkit Integration:** `N64Recomp`, `DolRecomp`, `NESRecomp`, `GBARecomp`, `SegaGenesisRecomp`, `VBRecomp`, `NDSRecomp`, `PSXRecomp`, `CDiRecomp`, `RT64`, `GhidrAssistMCP`, `FreeBIOS`, `GCNLLE`, `XboxLLE`.
- **CPU Cores (`plugins/cpus/`):** `65c816-recomp-core`, `m68k-recomp-core`, `arm-recomp-core`, `z80-recomp-core`, `mips-recomp-core`, `ppc-recomp-core`, `x86-recomp-core`.
- **Additional Target Platforms:**
  - **MS-DOS / x86 PC:** Real Mode MZ/COM parser, segment relocation mapping, BIOS/DOS interrupts (`INT 10h`, `INT 21h`), VGA register emulation.
  - **NeoGeo:** M68000 CPU, Z80 sound CPU, YM2610 FM/ADPCM audio, Fix/Sprite video pipelines.
  - **Android / ARM:** Dalvik DEX bytecode parser, ARM32/ARM64 AOT lifter, JNI C/C++ boundary marshalling.

---

## Directory Structure

```
├── docs/
│   └── ARCHITECTURE_SPEC.md   # Architectural & technical specification
├── core/
│   ├── tool_registry.py        # Central tool registry
│   ├── schema_validator.py     # JSON Schema / AST validator
│   ├── context_manager.py      # Micro-prompt context compression manager
│   ├── critic_node.py          # Critic reflection evaluation loop
│   └── agent_orchestrator.py   # Deterministic LangChain/LangGraph manager node
├── plugins/
│   ├── frameworks/             # RetroPortingToolkit, Ghidra, Reko, Capstone, Asar, etc.
│   ├── cpus/                   # 65C816, M68K, ARM, Z80, MIPS, PPC, x86 recompiler cores
│   └── platforms/              # SNES, MS-DOS, NeoGeo, Android, N64, GBA, etc.
├── tests/                      # Unit, integration, and E2E verification suite
└── README.md
```

---

## Installation & Setup

1. **Clone and Install Dependencies:**
   ```bash
   pip install langchain-core langgraph pydantic pytest jsonschema textual capstone
   ```

2. **Run Tests:**
   ```bash
   pytest tests/
   ```

3. **Launch CLI / Agent Pipeline:**
   ```bash
   python -m core.agent_orchestrator --target snes --rom path/to/rom.sfc
   ```

---

## Plugin Development Guide

To register a new platform or CPU recompiler plugin:
1. Create a module under `plugins/platforms/<platform_name>/` or `plugins/cpus/<cpu_name>/`.
2. Implement the standard plugin interface:
   ```python
   class PlatformPlugin:
       def parse_header(self, rom_bytes: bytes) -> dict: ...
       def disassemble(self, address: int, data: bytes) -> list: ...
       def lift_to_ir(self, opcodes: list) -> str: ...
   ```
3. Register the plugin in `core/tool_registry.py`.
