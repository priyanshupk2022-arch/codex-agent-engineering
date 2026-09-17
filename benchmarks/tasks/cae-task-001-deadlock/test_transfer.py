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

def test_negative_and_zero_amount():
    acc1 = Account(1, 100.0)
    acc2 = Account(2, 50.0)
    assert TransferService.transfer(acc1, acc2, -20.0) is False
    assert acc1.balance == 100.0
    assert acc2.balance == 50.0
    assert TransferService.transfer(acc1, acc2, 0.0) is True
    assert acc1.balance == 100.0
    assert acc2.balance == 50.0

def test_self_transfer_no_deadlock():
    acc = Account(1, 100.0)
    res = [None]
    def do_transfer():
        res[0] = TransferService.transfer(acc, acc, 30.0)
    t = threading.Thread(target=do_transfer, daemon=True)
    t.start()
    t.join(timeout=0.5)
    assert not t.is_alive(), "Self-transfer deadlocked!"
    assert res[0] is True
    assert acc.balance == 100.0

    res_fail = [None]
    def do_transfer_fail():
        res_fail[0] = TransferService.transfer(acc, acc, 200.0)
    t2 = threading.Thread(target=do_transfer_fail, daemon=True)
    t2.start()
    t2.join(timeout=0.5)
    assert not t2.is_alive(), "Self-transfer deadlocked on overdraft!"
    assert res_fail[0] is False

def test_concurrent_transfers_no_deadlock():
    acc1 = Account(1, 1000.0)
    acc2 = Account(2, 1000.0)
    
    threads = []
    for _ in range(6):
        t1 = threading.Thread(target=TransferService.transfer, args=(acc1, acc2, 10.0), daemon=True)
        t2 = threading.Thread(target=TransferService.transfer, args=(acc2, acc1, 10.0), daemon=True)
        t3 = threading.Thread(target=TransferService.transfer, args=(acc1, acc1, 5.0), daemon=True)
        threads.extend([t1, t2, t3])
        
    for t in threads:
        t.start()
        
    deadline = time.time() + 2.0
    for t in threads:
        remaining = max(0.001, deadline - time.time())
        t.join(timeout=remaining)

    for t in threads:
        assert not t.is_alive(), "Deadlock detected: thread failed to finish within timeout!"
        
    assert acc1.balance == 1000.0
    assert acc2.balance == 1000.0

def test_three_way_circular_concurrent_transfers():
    acc1 = Account(1, 1000.0)
    acc2 = Account(2, 1000.0)
    acc3 = Account(3, 1000.0)
    initial_total = acc1.balance + acc2.balance + acc3.balance

    threads = []
    for _ in range(8):
        threads.append(threading.Thread(target=TransferService.transfer, args=(acc1, acc2, 10.0), daemon=True))
        threads.append(threading.Thread(target=TransferService.transfer, args=(acc2, acc3, 10.0), daemon=True))
        threads.append(threading.Thread(target=TransferService.transfer, args=(acc3, acc1, 10.0), daemon=True))

    for t in threads:
        t.start()

    deadline = time.time() + 2.0
    for t in threads:
        remaining = max(0.001, deadline - time.time())
        t.join(timeout=remaining)

    for t in threads:
        assert not t.is_alive(), "Deadlock in 3-way circular transfer!"

    final_total = acc1.balance + acc2.balance + acc3.balance
    assert final_total == initial_total, f"System balance not conserved! {final_total} != {initial_total}"
