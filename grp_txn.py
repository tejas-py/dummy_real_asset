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
int 2
==
txna ApplicationArgs 0
byte "App Call"
==
&&
bnz main_l5
err
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


# Create new campaign
def create_app(client, private_key, approval_program, clear_program, globalSchema, localSchema):
    print("Creating application...")

    # Fetching public and private address from the passphrase, passed as argument.
    address = account.address_from_private_key(private_key)

    account_info = client.account_info(address)
    print("Account balance: {} microAlgos".format(account_info.get('amount')) + "\n")

    sender = address
    on_complete = transaction.OnComplete.NoOpOC.real

    params = client.suggested_params()

    txn = transaction.ApplicationCreateTxn(sender, params, on_complete,
                                           approval_program, clear_program,
                                           globalSchema, localSchema)

    signed_txn = txn.sign(private_key)
    tx_id = signed_txn.transaction.get_txid()
    client.send_transactions([signed_txn])
    utilities.wait_for_confirmation(client, tx_id)

    transaction_response = client.pending_transaction_info(tx_id)
    app_id = transaction_response['application-index']
    print("Created new App ID: ", app_id)

    return app_id


# creator create asset and calling app id.
def call_asset(client, private_key, appid, total_nft, unit_name, asset_name, file_path, note):
    # define address from private key of creator
    creator_account = account.address_from_private_key(private_key)
    creatorprivate_key = private_key

    # set suggested params
    params = client.suggested_params()

    print("Calling Campaign Application...")

    args = ["App Call"]

    # creator to call app(campaign): transaction 1
    sender = creator_account
    txn_1 = transaction.ApplicationNoOpTxn(sender, params, appid, args)
    print("Created Transaction 1: ", txn_1.get_txid())

    # creating asset: transaction 2
    txn_2 = transaction.AssetConfigTxn(sender=sender, sp=params, total=total_nft, default_frozen=False,
                                       unit_name=unit_name, asset_name=asset_name, manager=creator_account,
                                       reserve=creator_account, freeze=creator_account, clawback=creator_account,
                                       url=file_path, note=note, decimals=0)

    print("Created Transaction 2: ", txn_2.get_txid())

    # grouping both the txn to give the group id
    print("Grouping Transactions...")
    group_id = transaction.calculate_group_id([txn_1, txn_2])
    print("groupID of the Transaction: ", group_id)
    txn_1.group = group_id
    txn_2.group = group_id

    # split transaction group
    print("Splitting unsigned transaction group...")

    # signing the transactions
    stxn_1 = txn_1.sign(creatorprivate_key)
    print("Investor signed txn_1: ", stxn_1.get_txid())

    stxn_2 = txn_2.sign(creatorprivate_key)
    print("Investor signed txn_2: ", stxn_2.get_txid())

    # grouping the sign transactions
    signedGroup = [stxn_1, stxn_2]

    # send transactions
    print("Sending transaction group...")
    tx_id = client.send_transactions(signedGroup)

    return tx_id


if __name__ == "__main__":
    algod_client = algod_connection.algo_conn()

    passphrase = "focus silent connect teach minor subject hole observe enemy link recipe screen random core run " \
                 "target peanut autumn summer wall expose already tobacco above find"

    creator_private_key = mnemonic.to_private_key(passphrase)
    approvalprogram = utilities.compile_program(algod_client, approval_program_source_initial)
    clearprogram = utilities.compile_program(algod_client, clear_program_source)

    app_id = create_app(algod_client, creator_private_key, approvalprogram, clearprogram, global_schema, local_schema)

    unitName = "Webmob"
    assetName = "Tejas"
    url_path = "www.webmobinfo.ch"
    asset_note = "Real"
    call_asset(algod_client, creator_private_key, app_id, 1, unitName, assetName, url_path, asset_note)


