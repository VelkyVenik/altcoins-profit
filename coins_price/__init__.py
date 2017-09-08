import logging
import configparser

from coinbase.wallet.client import Client
from influxdb import InfluxDBClient

config = configparser.ConfigParser()
config.read(['config.ini', '../config.ini'])

logger = logging.getLogger(__name__)

influx_client = InfluxDBClient(
    config.get('InfluxDB', 'HOST'),
    config.get('InfluxDB', 'PORT'),
    config.get('InfluxDB', 'USER'),
    config.get('InfluxDB', 'PASS'),
    config.get('InfluxDB', 'DATABASE'),
    True, True
)

coinbase_client = Client(
    config.get('CoinBase', 'API_KEY'),
    config.get('CoinBase', 'API_SECRET'),
    api_version=config.get('CoinBase', 'API_VERSION')
)


def _get_price(pair):
    return float(coinbase_client.get_sell_price(currency_pair=pair).amount)


def _get_point(coin, fiat):
    point = {
        "measurement": "currencies",
        "tags": {
            'coin': coin
        },
        "fields": {
            fiat: _get_price(f'{coin}-{fiat}')
        }
    }

    return point


def save(fiat_currencies, crypto_currencies):
    points = []
    for fiat in fiat_currencies:
        for coin in crypto_currencies:
            points.append(_get_point(coin, fiat))

    logger.info("Coins prices saved to InfluxDB")
    influx_client.write_points(points)


def get_prices(interval, offset):
    query = f'SELECT MEAN("EUR") as "EUR", MEAN("CZK") as "CZK", MEAN("USD") AS "USD" ' \
            f'from currencies WHERE time > now() {offset} GROUP BY coin,time({interval}) fill(null)'

    result = influx_client.query(query)
    coins_result = {}
    for k in result.keys():
        coin = (k[1]['coin'])
        coins_result[coin] = list(result.get_points(tags={'coin': coin}))

    return coins_result


if __name__ == '__main__':
    save(['EUR', 'CZK', 'USD'], ['ETH', 'BTC', 'LTC'])

    prices = get_prices('5m', '-10m')
    for crypto_coin in prices:
        print(f"--- {crypto_coin} ---")
        for record in prices[crypto_coin]:
            print(record)
