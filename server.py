import schedule
import time
import logging
import coins_price


def save_prices():
    coins_price.save(['EUR', 'CZK', 'USD'], ['ETH', 'BTC', 'LTC'])


logging.basicConfig(format="%(asctime)s %(name)-20s %(levelname)-8s %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("Starting server")
schedule.every(1).minutes.do(save_prices)

while True:
    schedule.run_pending()
    time.sleep(1)
