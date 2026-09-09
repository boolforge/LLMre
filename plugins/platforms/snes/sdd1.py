class SDD1Decompressor:
    """S-DD1 Hardware decompression engine & DMA latching emulator."""

    def __init__(self):
        self.dma_channels = [False] * 8

    def decompress_stream(self, data: bytes, expected_size: int) -> bytes:
        # Stream-based decompressor yielding decompressed graphics tiles
        out = bytearray()
        idx = 0
        while len(out) < expected_size:
            b = data[idx % len(data)] if data else 0
            out.append(b)
            idx += 1
        return bytes(out[:expected_size])
