from pyteal import *


def approval_program():

    group_transaction = If(And(
        Global.group_size() == Int(3),
        Txn.application_args[0] == Bytes("New Reveal")
    ), Approve(), Reject())

    program = Cond(
        [Txn.application_id() == Int(0), Approve()],
        [Txn.on_completion() == OnComplete.NoOp, group_transaction]
    )

    return program


if __name__ == "__main__":
    with open("approval program.teal", "w") as f:
        compiled = compileTeal(approval_program(), mode=Mode.Application, version=5)
        f.write(compiled)
