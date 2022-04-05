import json
import algod_connection


indexerConnection = algod_connection.connect_indexer()


def total_assets():
    response = indexerConnection.search_assets(name="Mystery box Rome Edition", unit="Sports")
    asset_info = json.dumps(response, indent=2, sort_keys=True)
    return asset_info


