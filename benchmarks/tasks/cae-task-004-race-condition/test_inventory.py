import threading
import pytest
from inventory import InventoryService

def test_single_order():
    inv = InventoryService(10)
    assert inv.order(3) is True
    assert inv.stock == 7
    assert inv.order(10) is False
    assert inv.stock == 7

def test_invalid_quantity():
    inv = InventoryService(10)
    assert inv.order(0) is False
    assert inv.order(-5) is False
    assert inv.stock == 10

def test_concurrent_orders_no_oversell():
    initial_stock = 20
    inv = InventoryService(initial_stock)
    successful_orders = []
    lock = threading.Lock()

    def place_order():
        if inv.order(1):
            with lock:
                successful_orders.append(1)

    threads = [threading.Thread(target=place_order, daemon=True) for _ in range(50)]
    for t in threads:
        t.start()
    for t in threads:
        t.join(timeout=2.0)

    assert len(successful_orders) == initial_stock, f"Oversold! {len(successful_orders)} orders succeeded for {initial_stock} stock."
    assert inv.stock == 0
