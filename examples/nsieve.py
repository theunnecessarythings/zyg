"""Adapted from https://github.com/hanabi1224/Programming-Language-Benchmarks/blob/main/bench/algorithm/nsieve/2.zig"""

from zyg.zyg import *


@zig()
def nsieve_zig(n: usize) -> Error[anyerror, void]:
    std: Const[Infer] = Import("std")
    global_allocator: Const[Infer] = std.heap.page_allocator
    DynamicBitSet: Const[Infer] = std.bit_set.DynamicBitSet

    count: Var[usize] = 0
    flags: Var[Infer] = Try @ DynamicBitSet.initEmpty(global_allocator, n)

    with defer:
        flags.deinit()

    i: Var[usize] = 2
    while i < n:
        if not flags.isSet(i):
            count += 1
            j: Var[usize] = i << 1
            while j < n:
                flags.set(j)
                j += i
        i += 1

    std.debug.print("Primes up to {d:8} {d:8}\n", (n, count))


@zig()
def calc_zig(N: u32) -> Error[anyerror, void]:
    n: Const[u6] = IntCast(N)
    i: Var[u6] = 0
    while i < 3:
        base: Const[usize] = 10000
        Try @ nsieve_zig(base << (n - i))
        i += 1


def nsieve(n):
    count = 0
    flags = [True] * n
    for i in range(2, n):
        if flags[i]:
            count += 1
            flags[slice(i << 1, n, i)] = [False] * ((n - 1) // i - 1)
    print(f'Primes up to {n:8} {count:8}')


def calc(N):
    for i in range(0, 3):
        nsieve(10000 << (N-i))


if __name__ == "__main__":
    import timeit
    print("Without warmup...")
    print(timeit.timeit("calc_zig(10)", globals=globals(), number=1))
    print(timeit.timeit("calc(10)", globals=globals(), number=1))

    print("With warmup...")
    print(timeit.timeit("calc_zig(10)", globals=globals(), number=1))
    print(timeit.timeit("calc(10)", globals=globals(), number=1))
