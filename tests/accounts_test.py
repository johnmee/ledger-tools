import unittest
import unittest.mock

from ledgertools.ledgertools import accounts as acc


YAML_TESTFILE = 'tests/test_data/accounts.yaml'


class TestAccountMerchants(unittest.TestCase):
    """Read the list of accounts."""

    def test_read_accounts(self):
        """Load the list of accounts."""
        accounts = acc.AccountFile(YAML_TESTFILE)
        print(accounts.raw)

    def test_read_merchant_accounts(self):
        """Determine the merchants for each account."""
        accounts = acc.AccountFile(YAML_TESTFILE)

        print("Accounts")
        for account, merchants in accounts.account_merchants.items():
            print(account, merchants)
        print()

        print("Merchants")
        for merchant, account in accounts.merchant_accounts.items():
            print(merchant, ' => ', account)

    def test_merchant_matcher(self):
        accounts = acc.AccountFile(YAML_TESTFILE)
        print(accounts.match('Aldi 104'))
        self.assertEqual("Expenses:Food:Groceries", accounts.match('Aldi 104'))
        self.assertEqual("Expenses:Food:Groceries", accounts.match('ALDI 104'))   # ensure case sensitive
        self.assertEqual("Expenses:Food:Groceries", accounts.match('Coles 929023912 asdf Nsa'))
        self.assertEqual("Expenses:Household:Consumables", accounts.match('Bunnings 2019'))

    def test_accounts_list(self):
        """Spit out all the accounts"""
        accounts = acc.AccountFile(YAML_TESTFILE)
        for account in sorted(accounts.account_merchants.keys()):
            print('2016-06-25 open %s' % account)


class TestModuleRoutines(unittest.TestCase):
    """Test top level routines."""

    pubs = {'Pubs': ['Ivanhoe', '4.*']}

    def test_unknowns(self):
        """Test the unknowns routine.  Should find unknowns."""
        with unittest.mock.patch.dict(acc.account_file.raw, self.pubs):

            # We know the pines.
            assert acc.unknowns(["4 Pines"]) == []

            # We don't know bobs.
            assert acc.unknowns(["Bobs bar"]) != []

            # Put the most frequently occuring unknowns first.
            assert acc.unknowns([
                "Bobs bar", "Bobs bar", "Sallys", "Ivanhoe"
            ]) == ["Bobs bar", "Sallys"]
