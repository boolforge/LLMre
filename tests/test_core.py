"""
Unit tests for Core Engine Infrastructure.
"""

from core.schema_validator import SchemaValidator
from core.context_manager import ContextManager
from core.tool_registry import ToolRegistry
from core.critic_node import CriticNode
from core.agent_orchestrator import AgentOrchestrator


def test_schema_validator():
    validator = SchemaValidator()

    valid_patch = {
        "address": 0x8000,
        "bank": 0xC0,
        "symbol_name": "Func_C08000",
        "c_code": "void Func_C08000() { volatile uint8_t *reg = (uint8_t*)0x2100; *reg = 0x0F; }"
    }
    ok, err = validator.validate_patch(valid_patch)
    assert ok, f"Patch should be valid: {err}"

    invalid_patch = {"address": "8000"} # missing required fields
    ok, err = validator.validate_patch(invalid_patch)
    assert not ok


def test_context_manager():
    ctx = ContextManager.slice_disassembly_context(
        address=0x8000,
        bank=0xC0,
        opcodes=[{"address": 0x8000, "mnemonic": "LDA", "operands": "#$0F"}],
        symbols={0x8000: "Start"},
        m_flag=True,
        x_flag=True
    )
    assert ctx["target"] == "$C0:8000"
    assert len(ctx["opcodes"]) == 1


def test_tool_registry():
    registry = ToolRegistry(auto_register_defaults=True)
    registry.register_tool("dummy_tool", "framework", "Dummy test tool", lambda x: x * 2)
    assert registry.execute_tool("dummy_tool", x=5) == 10
    assert len(registry.list_tools()) > 10
    assert "reagent_analyze" in registry.list_tools()
    assert "cpu_lift_65c816" in registry.list_tools()


def test_critic_and_orchestrator():
    registry = ToolRegistry()

    def mock_recomp(micro_context):
        return {
            "address": 0x8000,
            "bank": 0xC0,
            "symbol_name": "Func_C08000",
            "c_code": "void Func_C08000() { volatile uint8_t *reg = (uint8_t*)0x2100; *reg = 0x0F; }"
        }

    def mock_sim(patch):
        return [{"cycle": 1, "addr": 0x2100, "val": 0x0F}]

    registry.register_tool("snes_recompile_block", "recomp", "Recompiles SNES block", mock_recomp)
    registry.register_tool("snes_simulate_trace", "sim", "Simulates SNES trace", mock_sim)

    orchestrator = AgentOrchestrator(registry)
    expected_trace = [{"cycle": 1, "addr": 0x2100, "val": 0x0F}]

    result = orchestrator.process_recompilation_task(
        task={
            "address": 0x8000,
            "bank": 0xC0,
            "opcodes": [{"address": 0x8000, "mnemonic": "LDA", "operands": "#$0F"}],
            "symbols": {0x8000: "Start"},
            "m_flag": True,
            "x_flag": True
        },
        expected_trace=expected_trace
    )

    assert result["approved"]
    assert result["reflection"]["status"] == "PASSED"

    retro_res = orchestrator.process_retro_decompilation_task("dummy_rom.sfc", arch="65c816", strategy="global_registers")
    assert retro_res["status"] == "SUCCESS"
    assert retro_res["verified_count"] > 0
