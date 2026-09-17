import threading
import time

class Account:
    def __init__(self, account_id: int, balance: float):
        self.id = account_id
        self.balance = balance
        self.lock = threading.Lock()

class TransferService:
    @staticmethod
    def transfer(source: Account, target: Account, amount: float):
        # BUG: Acquires source then target without ordering -> deadlock if A->B and B->A occur concurrently
        with source.lock:
            time.sleep(0.01) # Simulates network/DB latency
            with target.lock:
                if source.balance >= amount:
                    source.balance -= amount
                    target.balance += amount
                    return True
                return False
