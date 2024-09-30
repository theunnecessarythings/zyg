from zyg.zyg import *
from timeit import timeit
import numpy as np


class Matrix:
    def __init__(self, value, rows, cols):
        self.value = value
        self.rows = rows
        self.cols = cols

    def __getitem__(self, idxs):
        return self.value[idxs[0]][idxs[1]]

    def __setitem__(self, idxs, value):
        self.value[idxs[0]][idxs[1]] = value


def matmul_python(C, A, B):
    for m in range(C.rows):
        for k in range(A.cols):
            for n in range(C.cols):
                C[m, n] += A[m, k] * B[k, n]


@zig_struct(extern=False)
class MatrixZig(ZigStruct):
    value: Slice[f64]
    rows: usize
    cols: usize


@zig(export=False)
def matmul_zig(C: Ptr[MatrixZig], A: Ptr[MatrixZig], B: Ptr[MatrixZig]) -> void:
    for m in range(0, C.rows):
        for k in range(0, A.cols):
            for n in range(0, C.cols):
                C.value[m * C.cols + n] += A.value[m *
                                                   A.cols + k] * B.value[k * B.cols + n]


@zig()
def do_matmul_zig(M: usize, N: usize, K: usize) -> Error[anyerror, void]:
    std: Const[Infer] = Import("std")
    alloc: Const[Infer] = std.heap.page_allocator

    A: Var[MatrixZig] = {value: undefined, rows: M, cols: K}
    B: Var[MatrixZig] = {value: undefined, rows: K, cols: N}
    C: Var[MatrixZig] = {value: undefined, rows: M, cols: N}

    A.value = Try @ alloc.alloc(f64, M * K)
    B.value = Try @ alloc.alloc(f64, K * N)
    C.value = Try @ alloc.alloc(f64, M * N)

    with defer:
        alloc.free(A.value)
        alloc.free(B.value)
        alloc.free(C.value)

    matmul_zig(ref(C), ref(A), ref(B))


def benchmark_matmul_zig(M, N, K):
    secs = timeit(lambda: do_matmul_zig(M, N, K), number=2)/2
    gflops = ((2*M*N*K)/secs) / 1e9
    print(gflops, "GFLOP/s")
    return gflops


def benchmark_matmul_python(M, N, K):
    A = Matrix(list(np.random.rand(M, K)), M, K)
    B = Matrix(list(np.random.rand(K, N)), K, N)
    C = Matrix(list(np.zeros((M, N))), M, N)
    secs = timeit(lambda: matmul_python(C, A, B), number=2)/2
    gflops = ((2*M*N*K)/secs) / 1e9
    print(gflops, "GFLOP/s")
    return gflops


if __name__ == "__main__":
    zig_gflops = benchmark_matmul_zig(128, 128, 128)
    python_gflops = benchmark_matmul_python(128, 128, 128)
    zig_gflops = benchmark_matmul_zig(128, 128, 128)
