from flask import Flask, render_template
from api import WalletResource

app = Flask(__name__)

WalletResource.add_url_rules(app, rule_prefix='/api/wallet/')


@app.route("/<wallet_id>")
def wallet_details(wallet_id):
    return render_template('details.html', wallet_id=wallet_id)


@app.route("/")
def wallet_new():
    return render_template('index.html')

