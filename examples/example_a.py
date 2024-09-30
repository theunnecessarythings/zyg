import ctypes
from zyg.zyg import *


@zig_struct
class StructA(ZigStruct):
    a: i64
    b: i64
    c: i32 = 0

    d: Const[Slice[Const[u8]]] = "Hello, world!"

    Self: Const[Infer] = This()

    def init(a: i64, b: i64) -> Self:
        return {a: a, b: b}


@zig()
def zig_fn(a: i64, b: i64) -> Error[anyerror, i64]:
    std: Const[Infer] = Import("std")
    print: Const[Infer] = std.debug.print
    print("Hello, {} world!\n", (a,))

    comptime_a: comptime | Var[i64] = 1
    comptime_a += 1
    print("{d}\n", (comptime_a,))

    c: Var[i64] = 1
    c += 1
    if c == 2:
        c += 1
    else:
        c -= 1
    c = 0 if c == 1 else 1

    s: Const[Array[Const[u8]]] = "Hello, world!"
    print("{s}\n", (s,))
    l1: Const[Infer] = list([1, 2, 3], i64)
    for t in l1:
        print("{d} ", (t,))
    print("\n", ())

    with comptime:
        c_a: Const[i64] = 1
        c_b: Const[i64] = 2
        _ = c_a + c_b
        # Cannot use assert because it is a keyword in Python

    l2: Var[Infer] = std.ArrayList(i64).init(std.heap.page_allocator)
    Try(l2.append(1))
    print("{any}\n", (l2.items,))
    with defer:
        l2.deinit()
    with errdefer:
        l2.deinit()
    return (a * b) + DivTrunc(c, 2) + (-1) + (1 << 2) + (1 >> 2)


@zig()
def fibonacci(n: i64) -> i64:
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)


def fibonacci_py(n: int) -> int:
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci_py(n - 1) + fibonacci_py(n - 2)


@zig()
def call_fns() -> i64:
    std: Const[Infer] = Import("std")
    a: Const[Infer] = fibonacci(10)
    std.debug.print("{d}\n", (a,))
    # _ = zig_fn(1, 5)
    return a


@zig()
def list_test() -> Error[anyerror, Slice[i32]]:
    a: Const[Infer] = chr('a')
    _ = a

    std: Const[Infer] = Import("std")
    alloc: Const[Infer] = std.heap.page_allocator
    l: Var[Infer] = std.ArrayList(i32).init(alloc)
    Try(l.append(1))
    Try(l.append(2))
    Try(l.append(69))
    Try(l.append(420))
    _ = call_fns()
    return l.items


def main():
    print(zig_fn(1, 5))

    # Warm up
    a = fibonacci(10)
    print(a)

    # Time the code
    import time
    start = time.time()
    print(fibonacci(25))
    end = time.time()
    print(f"Time taken: {end - start}")

    start = time.time()
    print(fibonacci_py(25))
    end = time.time()
    print(f"Time taken: {end - start}")

    # call_fns()
    l1 = list_test()
    for i in range(l1.len):
        print(l1.ptr[i])


@zig_struct
class Full(ZigPackedStruct):
    number: u16


@zig_union(tag=Full)
class U(ZigTaggedUnion):
    a: u8
    b: u16


if __name__ == "__main__":
    main()
