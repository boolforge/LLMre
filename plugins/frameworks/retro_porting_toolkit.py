"""
RetroPortingToolkit Ecosystem Plugin Adapter.
Interfaces with RetroPortingToolkit recompiler suites:
N64Recomp, DolRecomp, NESRecomp, GBARecomp, SegaGenesisRecomp, VBRecomp,
NDSRecomp, PSXRecomp, CDiRecomp, RT64, GhidrAssistMCP, FreeBIOS, GCNLLE, XboxLLE.
"""

from typing import Dict, Any, List

class RPTSubEngine:
    def __init__(self, name: str, parent: "RetroPortingToolkitPlugin"):
        self.name = name
        self.parent = parent

    def recompile_rom(self, rom_path: str, out_dir: str = "./recompiled_output") -> Dict[str, Any]:
        return self.parent.invoke_recompiler(self.name, {"target_file": rom_path, "out_dir": out_dir})

class RetroPortingToolkitPlugin:
    """Unified plugin adapter for the RetroPortingToolkit recompiler ecosystem."""

    SUPPORTED_RECOMPILERS = [
        "N64Recomp", "DolRecomp", "NESRecomp", "GBARecomp", "SegaGenesisRecomp",
        "VBRecomp", "NDSRecomp", "PSXRecomp", "CDiRecomp", "RT64",
        "GhidrAssistMCP", "FreeBIOS", "GCNLLE", "XboxLLE"
    ]

    def get_supported_recompilers(self) -> List[str]:
        return self.SUPPORTED_RECOMPILERS

    def get_engine(self, engine_name: str) -> RPTSubEngine:
        if engine_name not in self.SUPPORTED_RECOMPILERS:
            raise ValueError(f"Unknown engine {engine_name}")
        return RPTSubEngine(engine_name, self)

    def invoke_recompiler(self, recompiler_name: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """Simulate or route invocation to specified RetroPortingToolkit engine."""
        if recompiler_name not in self.SUPPORTED_RECOMPILERS:
            raise ValueError(f"Unknown RetroPortingToolkit recompiler: {recompiler_name}")

        target_file = config.get("target_file", "unknown_rom")
        out_dir = config.get("out_dir", "./recompiled_output")

        return {
            "recompiler": recompiler_name,
            "status": "SUCCESS",
            "target": target_file,
            "output_directory": out_dir,
            "generated_files": [
                f"{out_dir}/{recompiler_name.lower()}_entry.c",
                f"{out_dir}/{recompiler_name.lower()}_symbols.h"
            ]
        }
