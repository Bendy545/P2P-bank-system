from .transactions import Transactions
from .errors import AccountNotEmpty, AccountNotFound, NotEnoughFunds, DuplicateAccount

MAX_AMOUNT = 9223372036854775807

class Account:
    def __init__(self, db, tx_dao=None):
        self.db = db
        self.tx_dao = tx_dao or Transactions(db)

    def create_account(self, bank_code, account_no):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            sql = """
            INSERT INTO accounts (account_no, bank_code, balance)
            VALUES (%s, %s, 0)
            """

            cursor.execute(sql, (account_no, bank_code))
            conn.commit()
            return f"{account_no}/{bank_code}"
        except Exception as e:
            conn.rollback()
            msg = str(e).lower()
            if "unique" in msg or "duplicate" in msg or "constraint" in msg:
                raise DuplicateAccount("Account already exists") from e
            raise
        finally:
            cursor.close()

    def get_balance(self, account_no, bank_code):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            sql = """
            SELECT balance FROM accounts
            WHERE account_no = %s and bank_code = %s
            """
            cursor.execute(sql, (account_no, bank_code))
            row = cursor.fetchone()
            if not row:
                raise AccountNotFound("Account not found")
            return int(row[0])
        finally:
            cursor.close()

    def deposit(self, account_no, bank_code, amount):
        account_no = int(account_no)
        amount = int(amount)
        if amount < 0 or amount > MAX_AMOUNT:
            raise ValueError("Amount out of range")

        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT id, balance FROM accounts WHERE account_no=%s AND bank_code=%s FOR UPDATE",
                (account_no, bank_code)
            )
            row = cursor.fetchone()
            if not row:
                raise AccountNotFound("Account not found")

            account_id, balance = row
            new_balance = int(balance) + amount

            cursor.execute(
                "UPDATE accounts SET balance=%s WHERE id=%s",
                (new_balance, account_id)
            )

            self.tx_dao.add_tx(cursor, account_id, 'D', amount)

            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            cursor.close()

    def withdraw(self, account_no, bank_code, amount):
        account_no = int(account_no)
        amount = int(amount)
        if amount < 0 or amount > MAX_AMOUNT:
            raise ValueError("Amount out of range")

        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT id, balance FROM accounts WHERE account_no=%s AND bank_code=%s FOR UPDATE",
                (account_no, bank_code)
            )
            row = cursor.fetchone()
            if not row:
                raise AccountNotFound("Account not found")

            account_id, balance = row
            balance = int(balance)

            if balance < amount:
                raise NotEnoughFunds("Not enough funds")

            new_balance = balance - amount

            cursor.execute(
                "UPDATE accounts SET balance=%s WHERE id=%s",
                (new_balance, account_id)
            )

            self.tx_dao.add_tx(cursor, account_id, "W", amount)

            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            cursor.close()

    def delete_account(self, account_no, bank_code):
        account_no = int(account_no)
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT id, balance FROM accounts WHERE account_no=%s AND bank_code=%s FOR UPDATE",
                (account_no, bank_code)
            )
            row = cursor.fetchone()
            if not row:
                raise AccountNotFound("Account not found")

            account_id, balance = row
            if int(balance) != 0:
                raise AccountNotEmpty("Cannot delete bank account that has balance")

            cursor.execute("DELETE FROM accounts WHERE id=%s", (account_id,))

            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            cursor.close()

    def bank_total_amount(self, bank_code):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT COALESCE(SUM(balance), 0) FROM accounts WHERE bank_code=%s",
                (bank_code,)
            )
            return int(cursor.fetchone()[0])
        finally:
            cursor.close()

    def bank_number_of_clients(self, bank_code):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT COUNT(*) FROM accounts WHERE bank_code=%s",
                (bank_code,)
            )
            return int(cursor.fetchone()[0])
        finally:
            cursor.close()

    def account_exists(self, account_no, bank_code):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "SELECT 1 FROM accounts WHERE account_no=%s AND bank_code=%s LIMIT 1",
                (account_no, bank_code)
            )
            return cursor.fetchone() is not None
        finally:
            cursor.close()