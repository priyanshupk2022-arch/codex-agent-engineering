import pytest
from stream_processor import StreamProcessor, MockResource

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
