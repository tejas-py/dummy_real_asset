from algosdk import kmd
from algosdk.wallet import Wallet

kmd_token = "87eb0fb1a2d9678cca012b73587b4efdb4ade417a3b5ab107d53bd0a22abc346"
kmd_address = "127.0.0.1:7833"

# create a kmd client
kcl = kmd.KMDClient(kmd_token, kmd_address)

# create a wallet object
wallet = Wallet("MyTestWallet1", "testpassword", kcl)

# get wallet information
info = wallet.info()
print("Wallet name:", info["wallet"]["name"])

# create an account
address = wallet.generate_key()
print("New account:", address)
