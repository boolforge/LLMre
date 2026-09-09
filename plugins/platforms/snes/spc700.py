class SPC700Audio:
    """SPC700 APU Audio subsystem & DSP register emulation."""

    def __init__(self):
        self.dsp_regs = [0] * 128
        self.dropped_frames = 0
        self.buffer_highwater = 0

    def write_dsp(self, reg: int, val: int):
        if 0 <= reg < 128:
            self.dsp_regs[reg] = val & 0xFF

    def read_dsp(self, reg: int) -> int:
        if 0 <= reg < 128:
            return self.dsp_regs[reg]
        return 0
