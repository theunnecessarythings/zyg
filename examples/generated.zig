const MatrixZig = struct {
    value: []f64,
    rows: usize,
    cols: usize,
};
pub fn matmul_zig(
    C: *MatrixZig,
    A: *MatrixZig,
    B: *MatrixZig,
) void {
    for (0..C.rows) |m| {
        for (0..A.cols) |k| {
            for (0..C.cols) |n| {
                C.value[((m * C.cols) + n)] += (A.value[((m * A.cols) + k)] * B.value[((k * B.cols) + n)]);
            }
        }
    }
}
pub fn do_matmul_zig(
    M: usize,
    N: usize,
    K: usize,
) anyerror!void {
    const std = @import("std");
    const alloc = std.heap.page_allocator;
    var A: MatrixZig = .{ .value = undefined, .rows = M, .cols = K };
    var B: MatrixZig = .{ .value = undefined, .rows = K, .cols = N };
    var C: MatrixZig = .{ .value = undefined, .rows = M, .cols = N };
    A.value = (try alloc.alloc(f64, (M * K)));
    B.value = (try alloc.alloc(f64, (K * N)));
    C.value = (try alloc.alloc(f64, (M * N)));
    defer {
        alloc.free(A.value);
        alloc.free(B.value);
        alloc.free(C.value);
    }
    matmul_zig(&C, &A, &B);
}
export fn _do_matmul_zig_zig(
    M: usize,
    N: usize,
    K: usize,
) void {
    return do_matmul_zig(
        M,
        N,
        K,
    ) catch unreachable;
}
