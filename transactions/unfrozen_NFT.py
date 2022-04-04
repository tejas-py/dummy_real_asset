import json
import algod_connection
from billiard.five import string

indexerConnection = algod_connection.connect_indexer()


def total_Unfrozen():
    response = indexerConnection.search_assets(name="Mystery box Rome Edition", unit="Sports")
    asset_info = response['assets']
    params_info = asset_info[4]
    for info in params_info.items():
    #asset_info = json.dumps(response, indent=2, sort_keys=True)
    #return string(asset_info)


#print(total_Unfrozen())

total_Unfrozen()