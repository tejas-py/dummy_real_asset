from flask import Flask, request
from algod_connection import *
import transactions.grp_txn
import transactions.user_NFT
import transactions.total_NFT
import transactions.unfrozen_NFT
import transactions.unfreeze_nft
from flask_cors import CORS
import time

app = Flask(__name__)
CORS(app)
cors = CORS(app, resources={
    r"/*": {
        "origin": "*"
    }
})

algod_client = algo_conn()
indexerConnection = connect_indexer()


# create account, (app call, mint NFT)
@app.route('/mintNFT', methods=["POST"])
def mintNFT():
    txn_details = request.get_json()
    passphrase = txn_details['passphrase']
    NFT_amount = txn_details['NFT_amount']
    url_path = txn_details['url']
    asset_note = txn_details['note']
    app_id = transactions.grp_txn.create_app(algod_client, passphrase)
    quantity = 0
    asset_txn_id = []
    while quantity < NFT_amount:
        if NFT_amount > 3:
            return "NFT Minted unsuccessful. Error: Can only mint upto 3 NFT."
        else:
            txID = transactions.grp_txn.call_asset(algod_client, passphrase, app_id, url_path, asset_note)
            asset_txn_id.append(txID)
            # sleeping code for 3 seconds so that previous transaction can be verified on the node
            time.sleep(3)
            quantity += 1
    return "NFT minted successfully. Your Minted NFT(s): {}.".format(asset_txn_id)


# Get total NFT by user.
@app.route('/userNFT/<string:address>')
def userNFT(address):
    total_NFT = transactions.user_NFT.users_assets(address)
    return "NFT information of: Name = Mystery box Rome Edition & Category = Sports \n {}".format(total_NFT)


# Get total NFT
@app.route('/totalNFT')
def totalNFT():
    all_nft = transactions.total_NFT.total_assets()
    return all_nft


# Get unfroze NFT
@app.route('/unfrozenNFT')
def unfrozenNFT():
    unfrozen_NFT = transactions.unfrozen_NFT.total_Unfrozen()
    return unfrozen_NFT


# Update NFT to unfroze
@app.route('/updateNFT', methods=['POST'])
def updateNFT():
    nft_details = request.get_json()
    passphrase = nft_details['passphrase']
    nft_id = nft_details['asset_id']
    asset_config = transactions.unfreeze_nft.nft_config(algod_client, passphrase, nft_id)
    return asset_config


if __name__ == "__main__":
    app.run(debug=True)
