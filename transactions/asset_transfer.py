# Ignore this file

from algosdk.future import transaction
from algosdk import account, mnemonic
import utilities
import algod_connection


def optin_asset(client, phase, mnemonics, receiver, assetID):
    global txid
    private_key1 = mnemonic.to_private_key(phase)
    private_key = mnemonic.to_private_key(mnemonics)
    creator_account = account.address_from_private_key(private_key)

    params = algod_client.suggested_params()

    account_info = client.account_info(receiver)
    holding = None
    idx = 0
    for my_account_info in account_info['assets']:
        scrutinized_asset = account_info['assets'][idx]
        idx = idx + 1
        if scrutinized_asset['asset-id'] == assetID:
            holding = True
            break

    if not holding:

        # Use the AssetTransferTxn class to transfer assets and opt-in
        txn = transaction.AssetTransferTxn(
            sender=receiver,
            sp=params,
            receiver=receiver,
            amt=0,
            index=assetID)
        stxn = txn.sign(private_key1)
        # Send the transaction to the network and retrieve the txid.
        try:
            txid = algod_client.send_transaction(stxn)
            print("Signed transaction with txID: {}".format(txid))
            # Wait for the transaction to be confirmed
            confirmed_txn = utilities.wait_for_confirmation(client, txid)
            print("TXID: ", txid)
            print("Result confirmed in round: {}".format(confirmed_txn['confirmed-round']))

        except Exception as err:
            print(err)

    transfer = transaction.AssetTransferTxn(sender=creator_account,
                                            sp=params,
                                            receiver=receiver,
                                            amt=1,
                                            index=assetID)
    sign_txn = transfer.sign(private_key)
    txID = client.send_transaction(sign_txn)
    print("Signed transaction with txID: {}".format(txID))
    confirmed_txn = utilities.wait_for_confirmation(client, txID)
    print("Result confirmed in round: {}".format(confirmed_txn['confirmed-round']))
    return txID


if __name__ == "__main__":
    algod_client = algod_connection.algo_conn()
    passphrase1 = "easy song equip captain drama patient casino regret double tell august same opera please fan drip dress alien color blouse key essay mesh ability foam"
    passphrase = "save muffin scout pottery lawsuit one stone vicious raw already pony stay head science spawn vacant genre bean river lady divide toddler capable about globe"
    getter = "JJMRJBRW3RWKQQXZZOJKCFT5KN6VGOPTGK4LWJT5T7GVTQKYDLZ2SCMTFY"
    assetid = 82103241

    tx_id = optin_asset(algod_client, passphrase1, passphrase, getter, assetid)

    print(tx_id)

