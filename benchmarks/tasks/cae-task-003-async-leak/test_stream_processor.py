import asyncio
import pytest
from stream_processor import StreamProcessor, MockResource

@pytest.fixture(autouse=True)
def reset_resource_counter():
    # Ensure fresh state for each test
    MockResource.active_instances = 0
    yield
    # Post-check: ensure no leaked resources remain
    assert MockResource.active_instances == 0, f"Leaked {MockResource.active_instances} unclosed instances after test!"

@pytest.mark.asyncio
async def test_process_stream_success():
    proc = StreamProcessor()
    res = await proc.process_stream(should_fail=False)
    assert len(res) == 4
    assert MockResource.active_instances == 0

@pytest.mark.asyncio
async def test_process_stream_leak_on_exception():
    proc = StreamProcessor()
    with pytest.raises(RuntimeError):
        await proc.process_stream(should_fail=True)
    assert MockResource.active_instances == 0, f"Leaked {MockResource.active_instances} unclosed resources!"

@pytest.mark.asyncio
async def test_multiple_sequential_failures():
    proc = StreamProcessor()
    for _ in range(10):
        with pytest.raises(RuntimeError):
            await proc.process_stream(should_fail=True)
        assert MockResource.active_instances == 0

@pytest.mark.asyncio
async def test_concurrent_mixed_streams():
    proc = StreamProcessor()
    coros = [proc.process_stream(should_fail=(i % 2 == 0)) for i in range(12)]
    results = await asyncio.gather(*coros, return_exceptions=True)
    
    # 6 should be exceptions, 6 should be lists of chunks
    exceptions = [r for r in results if isinstance(r, Exception)]
    successes = [r for r in results if isinstance(r, list)]
    assert len(exceptions) == 6
    assert len(successes) == 6
    assert MockResource.active_instances == 0
