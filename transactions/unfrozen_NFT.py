import json
import algod_connection
from billiard.five import string

indexerConnection = algod_connection.connect_indexer()


def total_Unfrozen():
    response = indexerConnection.search_transactions(txn_type="afrz")
    asset_info = json.dumps(response, indent=2, sort_keys=True)
    return string(asset_info)
