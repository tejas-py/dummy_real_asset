from algosdk import mnemonic
from algosdk.future.transaction import *
from algod_connection import *


# Declaring Mnemonics of accounts for minting assets
mnemonic1 = "valley fiction rescue truth useful lady amused submit boost eight trash abandon dust smoke ranch tribe regular sphere obtain picnic cruise embark glimpse abstract upset"
mnemonic2 = "hood route distance bargain element drink ripple worth wink brown puzzle fox cannon banana south hollow gospel hub correct build under run style able receive"


def mint_asset(client, private_key1, private_key2, total_units, unit_name, asset_name, note, url):

    params = client.suggested_params()

    public_address1 = account.address_from_private_key(private_key1)
    public_address2 = account.address_from_private_key(private_key2)

    print('Minting {} asset'.format(note))

    txn = AssetConfigTxn(
        sender=public_address1,
        sp=params,
        total=total_units,
        default_frozen=False,
        unit_name=unit_name,
        asset_name=asset_name,
        manager=public_address2,
        reserve=public_address2,
        freeze=public_address2,
        clawback=public_address2,
        url=url,
        note=note,
        decimals=0)

    print('Signing transaction...')
    stxn = txn.sign(private_key1)
    txid = client.send_transaction(stxn)
    print("Signed transaction with txID: {}".format(txid))

    return txid


if __name__ == "__main__":

    algod_client = algo_conn()

    creator_private_key = mnemonic.to_private_key(mnemonic1)
    manager_private_key = mnemonic.to_private_key(mnemonic2)


    asset = mint_asset(algod_client, creator_private_key, manager_private_key,1,"DLT",'algorand','real','www.webmobinfo.ch')

    print(asset)