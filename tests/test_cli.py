import pytest
from click.testing import CliRunner
from cli.main import cli

def test_cli_decompile():
    runner = CliRunner()
    result = runner.invoke(cli, ['decompile', '--binary', 'dummy.sfc', '--arch', '65c816'])
    assert result.exit_code == 0
    assert "Decompiling" in result.output

def test_cli_recompile():
    runner = CliRunner()
    result = runner.invoke(cli, ['recompile', '--arch', '65c816', '--bank', '0xC0', '--pc', '0x8000', '--asm-file', 'dummy.s'])
    assert result.exit_code == 0
    assert "Recompiled C Output" in result.output

def test_cli_verify_trace():
    runner = CliRunner()
    result = runner.invoke(cli, ['verify-trace', '--gold', 'gold.txt', '--cand', 'cand.txt'])
    assert result.exit_code == 0
    assert "Trace Audit Result" in result.output

def test_cli_agent_loop():
    runner = CliRunner()
    result = runner.invoke(cli, ['agent-loop', '--goal', 'Recompile Bank C0', '--steps', '2'])
    assert result.exit_code == 0
    assert "Goal completed successfully" in result.output
