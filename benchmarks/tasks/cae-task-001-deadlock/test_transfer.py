import threading
import time
import pytest
from transfer_service import Account, TransferService

def test_single_transfer():
    acc1 = Account(1, 100.0)
    acc2 = Account(2, 50.0)
    success = TransferService.transfer(acc1, acc2, 30.0)
    assert success is True
    assert acc1.balance == 70.0
    assert acc2.balance == 80.0

def test_concurrent_transfers_no_deadlock():
    acc1 = Account(1, 1000.0)
    acc2 = Account(2, 1000.0)
    
    threads = []
    for _ in range(4):
        t1 = threading.Thread(target=TransferService.transfer, args=(acc1, acc2, 10.0), daemon=True)
        t2 = threading.Thread(target=TransferService.transfer, args=(acc2, acc1, 10.0), daemon=True)
        threads.extend([t1, t2])
        
    for t in threads:
        t.start()
        
    for t in threads:
        t.join(timeout=0.2)
        assert not t.is_alive(), "Deadlock detected: thread failed to finish within timeout!"
        
    assert acc1.balance == 1000.0
    assert acc2.balance == 1000.0
