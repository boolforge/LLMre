import re
from typing import List, Dict, Any

class TraceAuditor:
    """Fast execution trace auditor and ripgrep regex diff analyzer."""

    def compare_traces(self, trace_gold: str, trace_candidate: str) -> Dict[str, Any]:
        gold_lines = [l.strip() for l in trace_gold.strip().split("\n") if l.strip()]
        cand_lines = [l.strip() for l in trace_candidate.strip().split("\n") if l.strip()]

        diffs = []
        for idx, (g, c) in enumerate(zip(gold_lines, cand_lines)):
            if g != c:
                diffs.append({"line": idx + 1, "gold": g, "candidate": c})

        return {
            "bit_exact": len(diffs) == 0,
            "total_lines": max(len(gold_lines), len(cand_lines)),
            "diff_count": len(diffs),
            "diffs": diffs
        }
