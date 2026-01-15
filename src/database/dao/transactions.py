class Transactions:
    def __init__(self, db):
        self.db = db

    def add_tx(self, cursor,account_id, tx_type, amount):
        amount = int(amount)
        if amount < 0:
            raise ValueError("Amount cannot be negative")
        if tx_type not in ("D", "W"):
            raise ValueError("Invalid transaction type")

        cursor.execute(
            "INSERT INTO account_tx (account_id, tx_type, amount) VALUES (%s, %s, %s)",
            (account_id, tx_type, amount)
        )
