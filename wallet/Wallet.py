import arrow
import attr
from babel.numbers import format_currency
from babel.dates import format_date, format_datetime, format_time

from .CoinsAccount import CoinsAccount

@attr.s
class Wallet:
    wallet_id = attr.ib()

    coins_addresses = attr.ib(default=[])
    coins_accounts = attr.ib(default=[])
    fiat_currency = attr.ib(default='EUR')

    invested = attr.ib(default=0.0)
    invested_str = attr.ib(init=False)

    fiat_price = attr.ib(init=False, default=0.0)
    fiat_price_str = attr.ib(init=False)

    coins_balance = attr.ib(init=False, default=0.0)
    coins_balance_str = attr.ib(init=False)
    coins_price = attr.ib(init=False, default={})

    profit = attr.ib(init=False)
    profit_str = attr.ib(init=False)
    profit_p = attr.ib(init=False)
    profit_p_str = attr.ib(init=False)

    last_update = attr.ib(default=None, init=False)

    def update(self):
        # FIXME: attrs is caching coins_accounts????
        self.coins_accounts = []

        if not self.coins_accounts:
            self.fiat_price = 0.0

            for adr in self.coins_addresses:
                account = CoinsAccount(address=adr, fiat_currency=self.fiat_currency)
                account.fetch()

                self.fiat_price += account.fiat_price
                self.coins_balance += account.coin_balance

                self.coins_price[account.coin] = {'price': account.coin_price, 'price_str': account.coin_price_str}

                self.coins_accounts.append(account)

        self.invested_str = format_currency(self.invested, self.fiat_currency)
        self.fiat_price_str = format_currency(self.fiat_price, self.fiat_currency)
        self.coins_balance_str = format_currency(self.coins_balance, 'ETH', locale='cs')

        self.profit = self.fiat_price - float(self.invested)
        self.profit_str = format_currency(self.profit, self.fiat_currency)
        self.profit_p = self.profit / float(self.invested) * 100
        self.profit_p_str = f"{self.profit_p:0.2f}%"

        self.last_update = format_datetime(arrow.now().datetime, locale='cs')

    def get_all(self):
        retval = attr.asdict(self)

        return retval

    def get_settings(self):
        settings = {
            'wallet_id': self.wallet_id,
            'coins_addresses': self.coins_addresses,
            'fiat_currency': self.fiat_currency,
            'invested': self.invested
        }

        return settings
