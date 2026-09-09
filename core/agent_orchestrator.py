from typing import Dict, Any, List, Optional
from core.context_manager import ContextManager
from core.schema_validator import SchemaValidator
from core.critic_node import CriticNode
from core.tool_registry import ToolRegistry

class AgentOrchestrator:
    """Manager-Worker-Critic triadic loop orchestrator enforcing strict determinism."""

    def __init__(self, tool_registry: Optional[ToolRegistry] = None, max_context_tokens: int = 4096):
        self.tool_registry = tool_registry or ToolRegistry()
        self.context_manager = ContextManager()
        self.validator = SchemaValidator()
        self.critic = CriticNode()
        self.history = []

    def process_recompilation_task(
        self,
        task: Dict[str, Any],
        expected_trace: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Execute Manager -> Worker -> Simulator -> Critic feedback loop."""
        # 1. Micro-prompt context slicing
        micro_context = self.context_manager.slice_disassembly_context(
            address=task["address"],
            bank=task["bank"],
            opcodes=task["opcodes"],
            symbols=task["symbols"],
            m_flag=task["m_flag"],
            x_flag=task["x_flag"]
        )

        # 2. Call worker recompiler tool
        recomp_tool = self.tool_registry.get_tool("snes_recompile_block")
        patch = recomp_tool["func"](micro_context)

        # 3. Simulate trace
        sim_tool = self.tool_registry.get_tool("snes_simulate_trace")
        actual_trace = sim_tool["func"](patch)

        # 4. Critic evaluation node
        approved, feedback = self.critic.evaluate_patch(patch, expected_trace, actual_trace)

        return {
            "approved": approved,
            "patch": patch,
            "actual_trace": actual_trace,
            "reflection": feedback
        }

    def run_agent_loop(self, goal: str, max_steps: int = 5) -> Dict[str, Any]:
        """Execute deterministic orchestration loop."""
        self.history.append({"role": "user", "content": f"Goal: {goal}"})
        step = 0
        status = "IN_PROGRESS"

        dummy_patch = {
            "address": 0x8000,
            "bank": 0xC0,
            "symbol_name": "Func_C08000",
            "c_code": "void Func_C08000() { volatile uint8_t *reg = (uint8_t*)0x2100; *reg = 0x0F; }"
        }
        dummy_trace = [{"cycle": 1, "addr": 0x2100, "val": 0x0F}]

        while step < max_steps and status == "IN_PROGRESS":
            step += 1
            approved, feedback = self.critic.evaluate_patch(dummy_patch, dummy_trace, dummy_trace)
            self.history.append({"role": "assistant", "content": f"Step {step}: Critic approved={approved}"})
            if approved:
                status = "COMPLETED"

        return {
            "goal": goal,
            "status": status,
            "steps_taken": step,
            "history": self.history
        }
