import json
from algosdk.v2client import indexer


algod_address = "https://testnet-algorand.api.purestake.io/idx2"
algod_token = "K7DgVll3W19DdHA3FTduX4XZTuCvTFf32HXUP5E4"
headers = {"X-API-Key": algod_token}

myindexer = indexer.IndexerClient(algod_token, algod_address, headers)

address = "YRUXAUFC7Z5BL3V3XBJ64I5BIN3A4YOJPBLUHGSEDPWNYVGUMOKBIV4N2I"
response = myindexer.search_transactions_by_address(address, txn_type="acfg")

print("Account Info: " + json.dumps(response, indent=2, sort_keys=True))
