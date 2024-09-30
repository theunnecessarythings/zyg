from zyg.zyg import *


def hello():
    print("Hello, World!")


@zig()
def hello_zig() -> void:
    std: Const[Infer] = Import("std")
    std.debug.print("Hello, World From Zig!!!\n", ())


if __name__ == "__main__":
    hello()

    hello_zig()
