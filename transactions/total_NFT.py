import json
import algod_connection
from billiard.five import string

indexerConnection = algod_connection.connect_indexer()


def total_assets():
    response = indexerConnection.search_assets(name="Mystery box Rome Edition", unit="Sports")
    total_number = len(response)
    asset_info = json.dumps(response, indent=2, sort_keys=True)
    return string(asset_info), string(total_number)
