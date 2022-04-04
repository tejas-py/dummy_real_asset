from algosdk.future import transaction
from algosdk import account, mnemonic
import utilities
from billiard.five import string

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


# creator create asset and calling app id.
def call_asset(client, mnemonics, appid, total_nft, url_path, asset_note):
    # define address from private key of creator
    private_key = mnemonic.to_private_key(mnemonics)
    creator_account = account.address_from_private_key(private_key)

    # set suggested params
    params = client.suggested_params()

    print("Calling Campaign Application...")

    args = ["App Call"]

    # creator to call app(campaign): transaction 1
    sender = creator_account
    txn_1 = transaction.ApplicationNoOpTxn(sender, params, appid, args)
    print("Created Transaction 1: ", txn_1.get_txid())

    # creating asset: transaction 2
    params_NFT = client.suggested_params()
    # params_NFT.fee = 25000000

    txn_2 = transaction.AssetConfigTxn(sender=sender, sp=params_NFT, total=total_nft, default_frozen=False,
                                       unit_name="Sports", asset_name="Mystery box Rome Edition", manager=creator_account,
                                       reserve=creator_account, freeze=creator_account, clawback=creator_account,
                                       url=url_path, note=asset_note, decimals=0)

    print("Created Transaction 2: ", txn_2.get_txid())

    # grouping both the txn to give the group id
    print("Grouping Transactions...")
    group_id = transaction.calculate_group_id([txn_1, txn_2])
    print("groupID of the Transaction: ", group_id)
    txn_1.group = group_id
    txn_2.group = group_id

    # split transaction group
    print("Splitting unsigned transaction group...")

    # signing the transactions for app call txn
    stxn_1 = txn_1.sign(private_key)
    print("Investor signed txn_1: ", stxn_1.get_txid())

    # signing the transaction for asset creation
    stxn_2 = txn_2.sign(private_key)
    tx_id2 = stxn_2.get_txid()
    print("Investor signed txn_2: ", tx_id2)

    # grouping the sign transactions
    signedGroup = [stxn_1, stxn_2]

    # send transactions
    print("Sending transaction group...")
    tx_id = client.send_transactions(signedGroup)
    print(tx_id)

    return string(tx_id2)

