from tinydb import TinyDB, Query
import attr
import random

from .Wallet import Wallet

DB_FILE = './db.json'


@attr.s
class WalletStorage:
    @staticmethod
    def get(wallet_id):
        db = TinyDB(DB_FILE, default_table='wallets')
        q = Query()
        wallet_dict = db.get(q.wallet_id == wallet_id)
        db.close()

        if not wallet_dict:
            return None

        wallet = Wallet(**wallet_dict)
        # print("Get", wallet.coins_accounts, wallet.coins_addresses, wallet.coins_balance, wallet_dict)

        return wallet

    @staticmethod
    def save(wallet_dict):
        db = TinyDB(DB_FILE, default_table='wallets')
        db.insert(wallet_dict)
        db.close()

    @staticmethod
    def update(wallet_id, ether_address=None, fiat_currency=None, invested=None):
        db = TinyDB(DB_FILE, default_table='wallets')
        q = Query()

        if fiat_currency:
            db.update({'fiat_currency': fiat_currency}, q.wallet_id == wallet_id)

        if invested:
            db.update({'invested': invested}, q.wallet_id == wallet_id)

        db.close()

    @staticmethod
    def create(coins_addresses, fiat_currency, invested, wallet_id=None):
        if not wallet_id:
            wallet_id = generate_id()

        wallet = Wallet(
            wallet_id=wallet_id,
            coins_addresses=coins_addresses,
            fiat_currency=fiat_currency,
            invested=invested)

        WalletStorage.save(wallet.get_settings())

        return wallet

    @staticmethod
    def delete(wallet_id):
        pass

    @staticmethod
    def exists(wallet_id):
        db = TinyDB(DB_FILE, default_table='wallets')
        q = Query()
        wallet_dict = db.get(q.wallet_id == wallet_id)
        db.close()

        return bool(wallet_dict)


def generate_id():
    dec_array = random.sample(range(0, 15), 15) + random.sample(range(0, 15), 15)
    hex_array = [hex(x)[2:] for x in dec_array]

    hex_str = ''.join(map(str, hex_array))

    return hex_str
