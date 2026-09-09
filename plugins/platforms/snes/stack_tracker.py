class StackTracker:
    """Tracks PHP/PLP/RTI dynamic 8-bit / 16-bit processor flag state transitions."""

    def __init__(self):
        self.stack = []

    def push_flags(self, m_bit: int, x_bit: int):
        self.stack.append((m_bit, x_bit))

    def pop_flags(self) -> tuple[int, int]:
        if self.stack:
            return self.stack.pop()
        return (0, 0)
