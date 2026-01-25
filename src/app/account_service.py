class AccountService:
    def __init__(self, account_dao):
        self._account_dao = account_dao

    def get_accounts(self, bank_code):
        rows = self._account_dao.get_accounts(bank_code)

        accounts = []
        for r in rows:
            accounts.append({
                "account_no": r[0],
                "balance": r[1],
            })

        return accounts
