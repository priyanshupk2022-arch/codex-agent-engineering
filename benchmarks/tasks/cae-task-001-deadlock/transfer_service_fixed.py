import threading

class Account:
    def __init__(self, account_id: int, balance: float):
        self.id = account_id
        self.balance = balance
        self.lock = threading.Lock()

class TransferService:
    @staticmethod
    def transfer(source: Account, target: Account, amount: float):
        if amount < 0:
            return False
        # Guard against self-transfer deadlock: acquire lock only once if accounts are identical
        if source.id == target.id:
            with source.lock:
                return source.balance >= amount

        # FIX: Acquire locks in deterministic order based on account id
        first, second = (source, target) if source.id < target.id else (target, source)
        with first.lock:
            with second.lock:
                if source.balance >= amount:
                    source.balance -= amount
                    target.balance += amount
                    return True
                return False
