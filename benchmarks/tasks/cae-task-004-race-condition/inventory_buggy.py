import time

class InventoryService:
    def __init__(self, initial_stock: int):
        self.stock = initial_stock

    def order(self, quantity: int) -> bool:
        # BUG: Non-atomic read-check-modify allows overselling
        if self.stock >= quantity:
            time.sleep(0.001) # Context switch window
            self.stock -= quantity
            return True
        return False
