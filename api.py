from restless.fl import FlaskResource
from restless.preparers import FieldsPreparer, CollectionSubPreparer

from wallet import WalletStorage

coin_account_preparer = FieldsPreparer(fields={
    'address': 'address',
    'coin': 'coin',
    'fiat_currency': 'fiat_currency',

    'coin_balance': 'coin_balance',
    'coin_price': 'coin_price',
    'coin_price_str': 'coin_price_str',

    'fiat_price': 'fiat_price',
    'fiat_price_str': 'fiat_price_str',

    'web_url': 'web_url',

    'last_update': 'last_update'
})

wallet_preparer = FieldsPreparer(fields={
    'wallet_id': 'wallet_id',
    'fiat_currency': 'fiat_currency',
    'invested': 'invested',
    'invested_str': 'invested_str',
    'coins_balance': 'coins_balance',
    'coins_balance_str': 'coins_balance_str',
    'coins_price': 'coins_price',
    'fiat_price': 'fiat_price',
    'fiat_price_str': 'fiat_price_str',
    'profit_p': 'profit_p',
    'profit_p_str': 'profit_p_str',
    'profit': 'profit',
    'profit_str': 'profit_str',
    'last_update': 'last_update',
    'coins_accounts': CollectionSubPreparer('coins_accounts', coin_account_preparer)
})


class WalletResource(FlaskResource):
    preparer = wallet_preparer

    def detail(self, pk):
        wallet = WalletStorage.get(pk)
        wallet.update()

        return wallet.get_all()

    def is_authenticated(self):
        if self.request.method == 'POST':
            return True

        pk = self.request.view_args.get('pk', None)

        if not pk:
            return False

        a = WalletStorage.exists(pk)
        return a

    def update(self, pk):
        invested = self.data.get('settings_investment')
        currency = self.data.get('settings_currency')

        WalletStorage.update(pk, fiat_currency=currency, invested=invested)
        wallet = WalletStorage.get(pk)
        wallet.update()

        return wallet.get_all()

    # {"settings_investment": 3557, "settings_coins_address": "0x1C7C21822fC30939A362fF3900C0b550D507bb41",
    #  "settings_currency": "EUR"}

    def create(self):
        if not self.data:
            return "", 555

        invested = self.data.get('settings_investment')
        currency = self.data.get('settings_currency')
        coins_address = self.data.get('settings_coins_address')

        wallet = WalletStorage.create([coins_address], currency, invested)
        wallet.update()

        return wallet.get_all()
