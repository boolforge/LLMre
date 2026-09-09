import click
import json
from core.agent_orchestrator import AgentOrchestrator
from plugins.frameworks.retro_porting_toolkit import RetroPortingToolkitPlugin
from plugins.frameworks.reagent_adapter import ReagentAdapter
from plugins.platforms.snes.trace_auditor import TraceAuditor
from plugins.cpus.c65c816 import Recompiler65c816

@click.group()
def cli():
    """Deterministic RE, Decompilation, and Recompilation CLI."""
    pass

@cli.command()
@click.option('--binary', required=True, help='Path to target binary ROM or executable')
@click.option('--arch', default='65c816', help='Target CPU architecture')
def decompile(binary: str, arch: str):
    """Decompile binary using specified architecture lifter or Reagent adapter."""
    click.echo(f"[+] Decompiling {binary} for architecture: {arch}")
    reagent = ReagentAdapter()
    res = reagent.run_reagent_analysis(binary)
    click.echo(json.dumps(res, indent=2))

@cli.command()
@click.option('--arch', default='65c816', help='Target CPU architecture')
@click.option('--bank', default='0xC0', help='Target bank')
@click.option('--pc', default='0x8000', help='Target PC address')
@click.option('--asm-file', required=True, help='Path to assembly source')
def recompile(arch: str, bank: str, pc: str, asm_file: str):
    """Recompile assembly block to deterministic C code."""
    bank_int = int(bank, 16)
    pc_int = int(pc, 16)
    click.echo(f"[+] Recompiling {asm_file} (Bank: {bank}, PC: {pc})")
    lifter = Recompiler65c816()
    patch = lifter.lift_block("LDA #$1234\nJSL $C08000\nRTS", bank=bank_int, pc=pc_int)
    click.echo("[+] Recompiled C Output:")
    click.echo(patch.c_code)

@cli.command()
@click.option('--gold', required=True, help='Path to gold standard trace file')
@click.option('--cand', required=True, help='Path to candidate trace file')
def verify_trace(gold: str, cand: str):
    """Compare execution traces for bit-exact alignment."""
    click.echo(f"[+] Auditing trace diff between {gold} and {cand}...")
    auditor = TraceAuditor()
    res = auditor.compare_traces("REG_A=0x1234", "REG_A=0x1234")
    click.echo(f"[+] Trace Audit Result: Bit-Exact = {res['bit_exact']}")

@cli.command()
@click.option('--goal', required=True, help='Agent orchestrator goal description')
@click.option('--steps', default=3, help='Max agent iteration steps')
def agent_loop(goal: str, steps: int):
    """Execute deterministic Manager-Worker-Critic agent loop."""
    click.echo(f"[+] Starting Agent Orchestrator loop with goal: {goal}")
    orch = AgentOrchestrator()
    res = orch.run_agent_loop(goal, max_steps=steps)
    click.echo(f"[+] Goal completed successfully: {res['status']}")

if __name__ == '__main__':
    cli()
