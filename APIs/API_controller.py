from flask import Flask, request
from algod_connection import *
import transactions.burn_mint_nft
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
cors = CORS(app, resources={
    r"/*": {
        "origin": "*"
    }
})

algod_client = algo_conn()


# create account, (app call, mint NFT)
@app.route('/burn_mint_nft', methods=["POST"])
def mintNFT():
    txn_details = request.get_json()
    passphrase = txn_details['passphrase']
    nft_id = txn_details['NFT_id']
    asset_note = txn_details['note']
    url_path = txn_details['url_path']
    app_id = transactions.burn_mint_nft.create_app(algod_client, passphrase)
    tx_id = transactions.burn_mint_nft.call_burn(algod_client, passphrase, nft_id, app_id)
    tx_id2 = transactions.burn_mint_nft.call_asset(algod_client, passphrase, app_id, url_path, asset_note)
    return "NFT burned, Successfully with transaction id: {}." \
           "\n NFT minted, Successfully with transaction id: {}".format(tx_id, tx_id2)


if __name__ == "__main__":
    app.run(debug=True)
