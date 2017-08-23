from flask import Flask, render_template, jsonify, request
from wallet import WalletStorage
from api import WalletResource

app = Flask(__name__)

WalletResource.add_url_rules(app, rule_prefix='/api/wallet/')


@app.route("/<wallet_id>")
def wallet_index(wallet_id):
    return render_template('index.html', wallet_id=wallet_id)


@app.route("/")
def wallet_new():
    return "unknow wallet"
    # wallet = WalletStorage.create(coins_addresses=['0x1C7C21822fC30939A362fF3900C0b550D507bb41'],
    #                               fiat_currency='EUR',
    #                               invested=3428)

    # return f"<a href='/{wallet.wallet_id}'>new wallet created</a>"
