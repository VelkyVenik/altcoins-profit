import attr
import arrow
from coinbase.wallet.client import Client

from .Config import config

@attr.s
class CoinBasePrice:
    currency_pair = attr.ib(default='ETH-EUR')

    spot_price = attr.ib(init=False, default=0.0)
    sell_price = attr.ib(init=False, default=0.0)
    buy_price = attr.ib(init=False, default=0.0)

    client = None
    config = config

    _last_update = attr.ib(init=False, default=None)

    def connect(self):
        self.client = Client(
            self.config.get('CoinBase', 'API_KEY'),
            self.config.get('CoinBase', 'API_SECRET'),
            api_version=self.config.get('CoinBase', 'API_VERSION')
        )


    def fetch(self):
        if not self.client:
            self.connect()

        self.sell_price = float(self.client.get_sell_price(currency_pair=self.currency_pair).amount) * 0.985
        # self.spot_price = float(self.client.get_spot_price(currency_pair=self.currency_pair).amount)
        # self.buy_price = float(self.client.get_buy_price(currency_pair=self.currency_pair).amount)

        self._last_update = arrow.now()

    def __str__(self):
        return f"{self.currency_pair} - " \
               f"{self.sell_price}/{self.spot_price}/{self.buy_price} " \
               f"(sell/spot/buy), {self._last_update}"


if __name__ == '__main__':
    cb = CoinBasePrice()
    cb.fetch()

    print(cb)