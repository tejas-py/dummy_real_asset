from algosdk.future import transaction
from algosdk import account, mnemonic
import utilities


def nft_config(client, mnemonics, asset_id):

    # define address from private key of creator
    private_key = mnemonic.to_private_key(mnemonics)
    creator_account = account.address_from_private_key(private_key)

    # set suggested params
    params = client.suggested_params()

    txn = transaction.AssetFreezeTxn(sender=creator_account, sp=params, index=asset_id, target=creator_account,
                                     new_freeze_state=False)
    # signing transaction
    sign_txn = txn.sign(private_key)
    tx_id = client.send_transaction(sign_txn)
    print("Signed transaction with txID: {}".format(tx_id))
    confirmed_txn = utilities.wait_for_confirmation(client, tx_id)
    print("Result confirmed in round: {}".format(confirmed_txn['confirmed-round']))
    
    return "Transaction completed, asset unfrozen, transaction ID: {}".format(tx_id)



