import json
import algod_connection
from billiard.five import string

indexerConnection = algod_connection.connect_indexer()


def users_assets(address):
    response = indexerConnection.search_assets(creator=address, name="Mystery box Rome Edition", unit="Sports")
    asset_info = json.dumps(response, indent=2, sort_keys=True)
    return string(asset_info)


# YRUXAUFC7Z5BL3V3XBJ64I5BIN3A4YOJPBLUHGSEDPWNYVGUMOKBIV4N2I
