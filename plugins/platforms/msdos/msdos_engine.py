from typing import Dict, Any

class MSDOSEngine:
    """MS-DOS execution tracing & interrupt handling adapter."""

    def emulate_interrupt(self, int_vector: int, regs: Dict[str, Any]) -> Dict[str, Any]:
        if int_vector == 0x21:
            ah = regs.get("ah", 0)
            if ah == 0x4C: # Terminate Process
                return {"status": "terminated", "exit_code": regs.get("al", 0)}
        return {"status": "handled", "int": int_vector}
