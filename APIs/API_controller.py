from flask import Flask, request
from algod_connection import *
import transactions.grp_txn
import transactions.user_NFT
import transactions.total_NFT
import transactions.unfrozen_NFT
import json

app = Flask(__name__)

algod_client = algo_conn()
indexerConnection = connect_indexer()


# create account, (app call, mint NFT)
@app.route('/mintNFT', methods=["POST"])
def mintNFT():
    txn_details = request.get_json()
    passphrase = txn_details['passphrase']
    total_NFT = txn_details['total_NFT']
    url_path = txn_details['url']
    asset_note = txn_details['note']
    app_id = transactions.grp_txn.create_app(algod_client, passphrase)
    txID = transactions.grp_txn.call_asset(algod_client, passphrase, app_id, total_NFT, url_path, asset_note)
    return "NFT minted, transaction id: {}.".format(txID)


# Get total NFT by user.
@app.route('/userNFT')
def userNFT():
    user_details = request.get_json()
    account_address = user_details['address']
    total_NFT = transactions.user_NFT.users_assets(account_address)
    return "NFT information of: Name = Mystery box Rome Edition & Category = Sports \n {}".format(total_NFT)


# Get total NFT
@app.route('/totalNFT')
def totalNFT():
    response = indexerConnection.search_assets(name="Mystery box Rome Edition", unit="Sports")
    total_number = len(response)
    asset_info = json.dumps(response, indent=2, sort_keys=True)
    return "Total number of NFT of Sports and Mystery box Rome Edition: {} " \
           "\n Assets information are = {}".format(total_number, asset_info)


# Get unfroze NFT
@app.route('/unfrozenNFT')
def unfrozenNFT():
    unfrozen_NFT = transactions.unfrozen_NFT.total_Unfrozen()
    return unfrozen_NFT


if __name__ == "__main__":
    app.run(debug=True)



