from urllib.parse import urljoin

import arrow
import attr
import requests
from babel.numbers import format_currency

from . import config
from .CoinBasePrice import CoinBasePrice


@attr.s
class CoinsAccount:
    address = attr.ib()
    coin = attr.ib(default='ETH')

    fiat_currency = attr.ib(default='EUR')

    coin_balance = attr.ib(default=0.0, init=False)
    coin_price = attr.ib(default=0.0, init=False)
    coin_price_str = attr.ib(default='', init=False)

    fiat_price = attr.ib(default=0.0, init=False)
    fiat_price_str = attr.ib(default='', init=False)

    web_url = attr.ib(default='', init=False)

    last_update = attr.ib(default=None, init=False)

    _coin_base = None
    _config = config

    def _fetch_coin_base(self):
        if not self._coin_base:
            self._coin_base = CoinBasePrice(currency_pair=f"{self.coin}-{self.fiat_currency}")

        self._coin_base.fetch()
        self.coin_price = self._coin_base.sell_price
        self.coin_price_str = format_currency(self.coin_price, self.fiat_currency)

        return True

    def _fetch_etherchain(self):
        api_url = urljoin(self._config.get('Ethereum', 'API_URL'), self.address)

        try:
            r = requests.get(api_url)
        except requests.exceptions.RequestException as e:
            print('Unable to get ETH account', e)
            return False

        try:
            account_data = r.json()['data'][0]
        except (KeyError, ValueError, IndexError) as e:
            print('Unable to parse ETH response', e)
            return False

        self.coin_balance = int(account_data['balance']) / 1000000000000000000
        self.web_url = urljoin(self._config.get('Ethereum', 'WEB_URL'), self.address)

        return True

    def fetch(self):
        self._fetch_etherchain()
        self._fetch_coin_base()

        self.fiat_price = self.coin_balance * self.coin_price
        self.fiat_price_str = format_currency(self.fiat_price, self.fiat_currency)
        self.last_update = arrow.now().timestamp

    def get_all(self):
        self.fetch()

        return attr.asdict(self)


if __name__ == '__main__':
    account = CoinsAccount('0x1C7C21822fC30939A362fF3900C0b550D507bb41')
    if not account.fetch():
        exit(-1)

    print(f"{account.address} - {account.balance_eth:.2f} ETH")