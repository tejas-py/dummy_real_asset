from pyteal import *


def contract(benefactor):
    Fee = Int(1000)

    #Only the benefactor account can withdraw from this escrow
    program = And(
        Txn.fee() <= Fee,
        Txn.receiver() == Addr(benefactor),
    )

    return program


if __name__ == "__main__":
    with open('sample.teal', "w") as f:
        account_address = "GRPTOLWIKGC7NS65TE36F65UZ7KYGW3PSIQGDHT2XJD7N2H2FCM3BZEZVU"
        compiled = compileTeal(contract(account_address), mode=Mode.Signature, version=5)
        f.write(compiled)
