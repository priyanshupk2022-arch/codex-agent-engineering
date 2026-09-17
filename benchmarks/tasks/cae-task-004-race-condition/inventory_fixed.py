import threading
import time

class InventoryService:
    def __init__(self, initial_stock: int):
        self.stock = initial_stock
        self._lock = threading.Lock()

    def order(self, quantity: int) -> bool:
        with self._lock:
            if self.stock >= quantity:
                self.stock -= quantity
                return True
            return False
