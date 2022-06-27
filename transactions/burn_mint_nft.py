from algosdk.future import transaction
from algosdk import account, mnemonic
import utilities
import algod_connection

local_ints = 1
local_bytes = 1
global_ints = 20
global_bytes = 20
global_schema = transaction.StateSchema(global_ints, global_bytes)
local_schema = transaction.StateSchema(local_ints, local_bytes)

# Declare the approval program source
approval_program_source_initial = b"""#pragma version 5
txn ApplicationID
int 0
==
bnz main_l6
txn OnCompletion
int NoOp
==
bnz main_l3
err
main_l3:
global GroupSize
int 3
==
txna ApplicationArgs 0
byte "New Reveal"
==
&&
bnz main_l5
int 0
return
main_l5:
int 1
return
main_l6:
int 1
return
"""

# Declare clear state program source
clear_program_source = b"""#pragma version 5
int 1
"""


# Create new application
def create_app(client, mnemonics):
    print("Creating application...")

    private_key = mnemonic.to_private_key(mnemonics)

    # Fetching public and private address from the passphrase, passed as argument.
    address = account.address_from_private_key(private_key)

    account_info = client.account_info(address)
    print("Account balance: {} microAlgos".format(account_info.get('amount')) + "\n")

    sender = address
    on_complete = transaction.OnComplete.NoOpOC.real

    params = client.suggested_params()

    approvalprogram = utilities.compile_program(client, approval_program_source_initial)
    clearprogram = utilities.compile_program(client, clear_program_source)

    txn = transaction.ApplicationCreateTxn(sender, params, on_complete,
                                           approvalprogram, clearprogram,
                                           global_schema, local_schema)

    signed_txn = txn.sign(private_key)
    tx_id = signed_txn.transaction.get_txid()
    client.send_transactions([signed_txn])
    utilities.wait_for_confirmation(client, tx_id)

    transaction_response = client.pending_transaction_info(tx_id)
    app_id = transaction_response['application-index']
    print("Created new App ID: ", app_id)

    return app_id


# (Calling Application, Burning NFT and Mint NFT)
def call_burn_mint(client, mnemonics, nft_id, app_id, url_path, asset_note):
    # define address from private key of creator
    private_key = mnemonic.to_private_key(mnemonics)
    creator_account = account.address_from_private_key(private_key)

    # set suggested params
    params = client.suggested_params()
    print("Calling {} Application...".format(app_id))
    args = ["New Reveal"]

    # creator to call app: transaction 1
    sender = creator_account
    txn_1 = transaction.ApplicationNoOpTxn(sender, params, app_id, args)
    print("Created Transaction 1: ", txn_1.get_txid())

    # burning NFT: transaction 2
    txn_2 = transaction.AssetConfigTxn(
        sender=creator_account,
        sp=params,
        index=nft_id,
        strict_empty_address_check=False
    )
    print("Created Transaction 2: ", txn_2.get_txid())

    # Minting NFT: Transaction 3

    txn_3 = transaction.AssetConfigTxn(sender=sender, sp=params, total=1, default_frozen=False,
                                       unit_name="Sports", asset_name="Mystery box Rome Edition",
                                       manager=creator_account,
                                       reserve=creator_account, freeze=creator_account, clawback=creator_account,
                                       url=url_path, note=asset_note, decimals=0)
    print("Created Transaction 3: ", txn_3.get_txid())

    # grouping both the txn to give the group id
    print("Grouping Transactions...")
    group_id = transaction.calculate_group_id([txn_1, txn_2, txn_3])
    print("groupID of the Transaction: ", group_id)
    txn_1.group = group_id
    txn_2.group = group_id
    txn_3.group = group_id

    # split transaction group
    print("Splitting unsigned transaction group...")

    # signing the transactions for app call txn
    stxn_1 = txn_1.sign(private_key)
    print("Creator signed txn_1: ", stxn_1.get_txid())
    stxn_2 = txn_2.sign(private_key)
    print("Creator signed txn_2: ", stxn_2.get_txid())
    stxn_3 = txn_3.sign(private_key)
    print("Creator Signed txn_3: ", stxn_3.get_txid())

    # grouping the sign transactions
    signedGroup = [stxn_1, stxn_2, stxn_3]

    # send transactions
    print("Sending transaction group...")
    tx_id = client.send_transactions(signedGroup)

    return tx_id


if __name__ == "__main__":
    algod_client = algod_connection.algo_conn()

    passphrase = "rabbit split erupt method oval dream lazy divide burden duty nominee lamp curious turtle verify skate lunch execute over caught enroll absurd laundry above electric"

    app_id = create_app(algod_client, passphrase)

    nftID = 85015115
    url_path = "www.webmobinfo.ch"
    note = "Real"
    txID = call_burn_mint(algod_client, passphrase, nftID, app_id, url_path, note)

    print("transactions completed with transaction id: ", txID)
