import asyncio

class MockResource:
    active_instances = 0

    def __init__(self):
        MockResource.active_instances += 1
        self.closed = False

    async def read_chunk(self, index: int):
        return f"chunk-{index}"

    async def close(self):
        if not self.closed:
            self.closed = True
            MockResource.active_instances -= 1

class StreamProcessor:
    async def process_stream(self, should_fail: bool = False):
        res = MockResource()
        try:
            results = []
            for i in range(4):
                if should_fail and i == 2:
                    raise RuntimeError("Processing aborted prematurely")
                data = await res.read_chunk(i)
                results.append(data)
            return results
        finally:
            await res.close()
