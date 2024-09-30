const Point = extern struct {
    x: i32,
    y: i32,
};
const PointF = extern struct {
    x: f32,
    y: f32,
};
const Point2 = packed struct {
    x: f32,
    y: f32,
};
const Foo = extern struct {
    a: i32 = 1234,
    b: i32,
};
const Full = packed struct {
    number: u16,
};
const Divided = packed struct {
    half1: u8,
    quarter3: u4,
    quarter4: u4,
};
const BitField = packed struct {
    a: u3,
    b: u3,
    c: u2,
};
const Type = enum {
    ok,
    not_ok,
};
const Value = enum(u2) {
    zero,
    one,
    two,
};
const Value2 = enum(u32) {
    hundred = 100,
    thousand = 1000,
    million = 1000000,
};
const Value3 = enum(u4) {
    a,
    b = 8,
    c,
    d = 4,
    e,
};
const Suit = enum {
    clubs,
    spades,
    diamonds,
    hearts,
    const Self = @This();
    pub fn isClubs(
        self: Self,
    ) bool {
        return self == Suit.clubs;
    }
};
const Foo2 = enum {
    string,
    number,
    none,
};
const Small = enum {
    one,
    two,
    three,
    four,
};
const Color = enum {
    automatic,
    off,
    on,
};
const Number = enum(u8) {
    one,
    two,
    three,
    _,
};
const Payload = union {
    int: i64,
    float: f64,
    boolean: bool,
};
const ComplexTypeTag = enum {
    ok,
    not_ok,
};
const ComplexType = union(ComplexTypeTag) {
    ok: u8,
    not_ok: void,
};
const Variant = union(enum) {
    int: i32,
    boolean: bool,
    none: void,
    const Self = @This();
    pub fn truthy(
        self: Self,
    ) bool {
        const ret = switch (self) {
            Variant.int => |x_int| blk: {
                break :blk x_int != 0;
            },
            Variant.boolean => |x_bool| blk: {
                break :blk x_bool;
            },
            Variant.none => blk: {
                break :blk false;
            },
        };
        return ret;
    }
};
const Number2 = union {
    int: i32,
    float: f64,
};
const Point3 = extern struct {
    x: u8,
    y: u8,
};
const Item = union(enum) {
    a: u32,
    c: Point3,
    d: void,
    e: u32,
};
const Struct1 = struct {
    a: u32,
    b: ?u32,
};
const SliceTypeA = extern struct {
    len: usize,
    ptr: [*]u32,
};
const SliceTypeB = extern struct {
    ptr: [*]SliceTypeA,
    len: usize,
};
const AnySlice = union(enum) {
    a: SliceTypeA,
    b: SliceTypeB,
    c: []const u8,
    d: []AnySlice,
};
const EventuallyNullSequence = extern struct {
    var numbers_left: u32 = undefined;
    pub fn eventuallyNullSequence() ?u32 {
        if (numbers_left == 0) {
            return null;
        } else {}
        numbers_left -= 1;
        return numbers_left;
    }
};
const EventuallyErrorSequence = extern struct {
    var numbers_left: u32 = undefined;
    pub fn eventuallyErrorSequence() anyerror!u32 {
        if (numbers_left == 0) {
            return error.ReachedZero;
        } else {}
        numbers_left -= 1;
        return numbers_left;
    }
};
const Call2Op = extern struct {
    const fnCall = *const fn (i8, i8) i8;
};
const FileOpenError = error{
    FileNotFound,
    AccessDenied,
    OutOfMemory,
};
const AllocationError = error{
    OutOfMemory,
};
const A = error{
    NotDir,
    PathNotFound,
};
const B = error{
    OutOfMemory,
    PathNotFound,
};
const MergeErrorSets = extern struct {
    const C = A || B;
    pub fn foo() C!void {
        return error.NotDir;
    }
};
const ErrorSet = error{
    Overflow,
};
const E = enum {
    one,
    two,
    three,
};
const U = union(E) {
    one: i32,
    two: f32,
    three: void,
};
const U2 = union(enum) {
    a: void,
    b: f32,
    pub fn tag(
        self: @This(),
    ) usize {
        switch (self) {
            .a => {
                return 1;
            },
            .b => {
                return 2;
            },
        }
    }
};
const Err = error{
    A,
    B,
    C,
};
const CmdFn = struct {
    name: []const u8,
    func: fn (i32) i32,
};
const Point4 = extern struct {
    x: u32,
    y: u32,
    var z: u32 = 1;
};
const Foo5 = extern struct {
    nope: i32,
    var blah = "xxx";
    const hi = 1;
};
pub fn hello() anyerror!void {
    const std = @import("std");
    const stdout = std.io.getStdOut().writer();
    try (stdout.print("Hello, {s}!\n", .{"world"}));
}
export fn _hello_zig() void {
    return hello() catch unreachable;
}
pub fn hello2() void {
    const std = @import("std");
    std.debug.print("Hello, world!\n", .{});
}
export fn _hello2_zig() void {
    return hello2();
}
pub fn values() void {
    const std = @import("std");
    const print = std.debug.print;
    const assert = std.debug.assert;
    const one_plus_one: i32 = (1 + 1);
    print("1 + 1 = {}\n", .{one_plus_one});
    const seven_div_three: f32 = (7.0 / 3.0);
    print("7.0 / 3.0 = {}\n", .{seven_div_three});
    print("{}\n{}\n{}\n", .{ true and false, true or false, (!true) });
    var optional_value: ?[]const u8 = null;
    assert(optional_value == null);
    print("\noptional 1\ntype: {}\nvalue: {?s}\n", .{ @TypeOf(optional_value), optional_value });
    optional_value = "hi";
    assert(optional_value != null);
    print("\noptional 2\ntype: {}\nvalue: {?s}\n", .{ @TypeOf(optional_value), optional_value });
    var number_or_error: anyerror!i32 = error.ArgNotFound;
    print("\nerror union 1\ntype: {}\nvalue: {!}\n", .{ @TypeOf(number_or_error), number_or_error });
    number_or_error = 1234;
    print("\nerror union 2\ntype: {}\nvalue: {!}\n", .{ @TypeOf(number_or_error), number_or_error });
}
export fn _values_zig() void {
    return values();
}
pub fn assign_undefined() void {
    const std = @import("std");
    const print = std.debug.print;
    var x: i32 = undefined;
    x = 1;
    print("{d}\n", .{x});
}
export fn _assign_undefined_zig() void {
    return assign_undefined();
}
pub fn make_point(
    x: i32,
) Point {
    return .{ .x = x, .y = (x * 2) };
}
export fn _make_point_zig(
    x: i32,
) Point {
    return make_point(
        x,
    );
}
pub fn arrays() void {
    const std = @import("std");
    const mem = std.mem;
    const assert = std.debug.assert;
    const message = [_]u8{ 'h', 'e', 'l', 'l', 'o' };
    const alt_message: [5]u8 = .{ 'h', 'e', 'l', 'l', 'o' };
    comptime {
        assert(mem.eql(u8, &message, &alt_message));
        assert(message.len == 5);
    }
    const same_message = "hello";
    comptime {
        assert(mem.eql(u8, &message, same_message));
    }
    var sum: usize = 0;
    for (message) |byte| {
        sum += byte;
    }
    assert(sum == ((('h' + 'e') + ('l' * 2)) + 'o'));
    var some_integers: [100]i32 = undefined;
    for (&some_integers, 0..) |*item, i| {
        item.* = @intCast(i);
    }
    assert(some_integers[10] == 10);
    assert(some_integers[99] == 99);
    const part_one = [_]i32{ 1, 2, 3, 4 };
    const part_two = [_]i32{ 5, 6, 7, 8 };
    const all_of_it = part_one ++ part_two;
    assert(mem.eql(i32, &all_of_it, &[_]i32{ 1, 2, 3, 4, 5, 6, 7, 8 }));
    const hello_ = "hello";
    const world = "world";
    const hello_world = hello_ ++ " " ++ world;
    assert(mem.eql(u8, hello_world, "hello world"));
    const pattern = "ab" ** 3;
    assert(mem.eql(u8, pattern, "ababab"));
    const all_zero = [_]u16{0} ** 10;
    assert(all_zero.len == 10);
    assert(all_zero[5] == 0);
    const more_points: [10]Point = [_]Point{make_point(3)} ** 10;
    assert(more_points[4].x == 3);
    assert(more_points[4].y == 6);
    assert(more_points.len == 10);
}
export fn _arrays_zig() void {
    return arrays();
}
pub fn multidimensional_arrays() void {
    const std = @import("std");
    const assert = std.debug.assert;
    const mat4x4: [4][4]f32 = .{ .{ 1.0, 0.0, 0.0, 0.0 }, .{ 0.0, 1.0, 0.0, 1.0 }, .{ 0.0, 0.0, 1.0, 0.0 }, .{ 0.0, 0.0, 0.0, 1.0 } };
    assert(mat4x4[1][1] == 1.0);
    const all_zero: [4][4]f32 = .{ .{ 0.0, 0.0, 0.0, 0.0 }, .{ 0.0, 0.0, 0.0, 0.0 }, .{ 0.0, 0.0, 0.0, 0.0 }, .{ 0.0, 0.0, 0.0, 0.0 } };
    assert(all_zero[0][0] == 0.0);
}
export fn _multidimensional_arrays_zig() void {
    return multidimensional_arrays();
}
pub fn zero_terminated_sentinel_array() void {
    const std = @import("std");
    const assert = std.debug.assert;
    const array: [4:0]u8 = .{ 1, 2, 3, 4 };
    assert(@TypeOf(array) == [4:0]u8);
    assert(array.len == 4);
    assert(array[4] == 0);
}
export fn _zero_terminated_sentinel_array_zig() void {
    return zero_terminated_sentinel_array();
}
pub fn extra_zeros_in_zero_terminated_sentinel_array() void {
    const std = @import("std");
    const assert = std.debug.assert;
    const array: [4:0]u8 = .{ 1, 0, 0, 4 };
    assert(@TypeOf(array) == [4:0]u8);
    assert(array.len == 4);
    assert(array[4] == 0);
}
export fn _extra_zeros_in_zero_terminated_sentinel_array_zig() void {
    return extra_zeros_in_zero_terminated_sentinel_array();
}
pub fn basic_vector() void {
    const std = @import("std");
    const assert = std.debug.assert;
    const a = @Vector(4, i32){ 1, 2, 3, 4 };
    const b = @Vector(4, i32){ 5, 6, 7, 8 };
    const c = (a + b);
    assert(c[0] == 6);
    assert(c[1] == 8);
    assert(c[2] == 10);
    assert(c[3] == 12);
}
export fn _basic_vector_zig() void {
    return basic_vector();
}
pub fn vector_conversion() anyerror!void {
    const std = @import("std");
    const testing = std.testing;
    const arr1: [4]f32 = .{ 1.1, 3.2, 4.5, 5.6 };
    const vec: @Vector(4, f32) = arr1;
    const arr2: [4]f32 = vec;
    try (testing.expectEqual(arr1, arr2));
    const vec2: @Vector(2, f32) = arr1[1..3].*;
    const slice: []const f32 = &arr1;
    var offset: u32 = 1;
    _ = &offset;
    const vec3: @Vector(2, f32) = slice[offset..][0..2].*;
    try (testing.expectEqual(slice[offset], vec2[0]));
    try (testing.expectEqual(slice[(offset + 1)], vec2[1]));
    try (testing.expectEqual(vec2, vec3));
}
export fn _vector_conversion_zig() void {
    return vector_conversion() catch unreachable;
}
pub fn address_of_syntax() void {
    const std = @import("std");
    const assert = std.debug.assert;
    const x: i32 = 1234;
    const x_ptr = &x;
    assert(@TypeOf(x_ptr) == *const i32);
    assert(x_ptr.* == 1234);
    var y: i32 = 5678;
    const y_ptr = &y;
    assert(@TypeOf(y_ptr) == *i32);
    y_ptr.* += 1;
    assert(y_ptr.* == 5679);
}
export fn _address_of_syntax_zig() void {
    return address_of_syntax();
}
pub fn pointer_array_access() void {
    const std = @import("std");
    const assert = std.debug.assert;
    var array: [10]u8 = [_]u8{ 1, 2, 3, 4, 5, 6, 7, 8, 9, 10 };
    const ptr = &array[2];
    assert(@TypeOf(ptr) == *u8);
    assert(array[2] == 3);
    ptr.* += 1;
    assert(array[2] == 4);
}
export fn _pointer_array_access_zig() void {
    return pointer_array_access();
}
pub fn slice_syntax() void {
    const std = @import("std");
    const assert = std.debug.assert;
    var x: i32 = 1234;
    const x_ptr = &x;
    const x_array_ptr = x_ptr[0..1];
    assert(@TypeOf(x_array_ptr) == *[1]i32);
    const x_many_ptr: [*]i32 = x_array_ptr;
    assert(x_many_ptr[0] == 1234);
}
export fn _slice_syntax_zig() void {
    return slice_syntax();
}
pub fn pointer_arithmetic_with_slices() void {
    const std = @import("std");
    const assert = std.debug.assert;
    var array = [_]i32{ 1, 2, 3, 4 };
    var length: usize = 0;
    _ = &length;
    var slice = array[length..array.len];
    assert(slice[0] == 1);
    assert(slice.len == 4);
    slice.ptr += 1;
    assert(slice[0] == 2);
    assert(slice.len == 4);
}
export fn _pointer_arithmetic_with_slices_zig() void {
    return pointer_arithmetic_with_slices();
}
pub fn pointer_arithmetic_with_many_item_pointer() void {
    const std = @import("std");
    const assert = std.debug.assert;
    const array = [_]i32{ 1, 2, 3, 4 };
    var ptr: [*]const i32 = &array;
    assert(ptr[0] == 1);
    ptr += 1;
    assert(ptr[0] == 2);
    assert(ptr[1..] == (ptr + 1));
}
export fn _pointer_arithmetic_with_many_item_pointer_zig() void {
    return pointer_arithmetic_with_many_item_pointer();
}
pub fn comptime_pointers() anyerror!void {
    const std = @import("std");
    const testing = std.testing;
    comptime {
        var x: i32 = 1;
        const ptr = &x;
        ptr.* += 1;
        x += 1;
        try (testing.expect(ptr.* == 3));
    }
}
export fn _comptime_pointers_zig() void {
    return comptime_pointers() catch unreachable;
}
pub fn integer_pointer_conversion() anyerror!void {
    const std = @import("std");
    const testing = std.testing;
    const ptr: *i32 = @ptrFromInt(3735928544);
    const addr = @intFromPtr(ptr);
    try (testing.expect(@TypeOf(addr) == usize));
    try (testing.expect(addr == 3735928544));
}
export fn _integer_pointer_conversion_zig() void {
    return integer_pointer_conversion() catch unreachable;
}
pub fn comptime_ptr_from_int() anyerror!void {
    const std = @import("std");
    const testing = std.testing;
    comptime {
        const ptr: *i32 = @ptrFromInt(3735928544);
        const addr = @intFromPtr(ptr);
        try (testing.expect(@TypeOf(addr) == usize));
        try (testing.expect(addr == 3735928544));
    }
}
export fn _comptime_ptr_from_int_zig() void {
    return comptime_ptr_from_int() catch unreachable;
}
pub fn basic_slices() anyerror!void {
    const std = @import("std");
    const assert = std.debug.assert;
    const expectEqualSlices = std.testing.expectEqualSlices;
    var array = [_]i32{ 1, 2, 3, 4 };
    var known_at_runtime_zero: usize = 0;
    _ = &known_at_runtime_zero;
    const slice = array[known_at_runtime_zero..array.len];
    const alt_slice: []const i32 = &.{ 1, 2, 3, 4 };
    try (expectEqualSlices(i32, slice, alt_slice));
    assert(@TypeOf(slice) == []i32);
    assert(&slice[0] == &array[0]);
    assert(slice.len == array.len);
    const array_ptr = array[0..array.len];
    assert(@TypeOf(array_ptr) == *[array.len]i32);
    var runtime_start: usize = 1;
    _ = &runtime_start;
    const length = 2;
    const array_ptr_len = array[runtime_start..][0..length];
    assert(@TypeOf(array_ptr_len) == *[length]i32);
    assert(@TypeOf(&slice[0]) == *i32);
    assert(@TypeOf(slice.ptr) == [*]i32);
    assert(@intFromPtr(slice.ptr) == @intFromPtr(&slice[0]));
    slice[10] += 1;
    const empty1 = &[_]u8{};
    const empty2: []u8 = &.{};
    assert(empty1.len == 0);
    assert(empty2.len == 0);
}
export fn _basic_slices_zig() void {
    return basic_slices() catch unreachable;
}
pub fn using_slices_for_strings() anyerror!void {
    const std = @import("std");
    const assert = std.debug.assert;
    const fmt = std.fmt;
    const hello_: []const u8 = "hello";
    const world: []const u8 = "世界";
    var all_together: [100]u8 = undefined;
    var start: usize = 0;
    _ = &start;
    const all_together_slice = all_together[start..];
    const hello_world = try (fmt.bufPrint(all_together_slice, "{s} {s}", .{ hello_, world }));
    assert(std.mem.eql(u8, hello_world, "hello 世界"));
}
export fn _using_slices_for_strings_zig() void {
    return using_slices_for_strings() catch unreachable;
}
pub fn slice_pointer() anyerror!void {
    const std = @import("std");
    const assert = std.debug.assert;
    var array: [10]u8 = undefined;
    const ptr = &array;
    assert(@TypeOf(ptr) == *[10]u8);
    var start: usize = 0;
    var end: usize = 5;
    _ = &start;
    _ = &end;
    const slice = ptr[start..end];
    assert(@TypeOf(slice) == []u8);
    slice[2] = 3;
    assert(array[2] == 3);
    const ptr2 = slice[2..3];
    assert(ptr2.len == 1);
    assert(ptr2[0] == 3);
    assert(@TypeOf(ptr2) == *[1]u8);
}
export fn _slice_pointer_zig() void {
    return slice_pointer() catch unreachable;
}
pub fn zero_terminated_slice() void {
    const std = @import("std");
    const assert = std.debug.assert;
    const slice: [:0]const u8 = "hello";
    assert(slice.len == 5);
    assert(slice[5] == 0);
}
export fn _zero_terminated_slice_zig() void {
    return zero_terminated_slice();
}
pub fn zero_terminated_slicing() void {
    const std = @import("std");
    const assert = std.debug.assert;
    var array = [_]u8{ 3, 2, 1, 0, 3, 2, 1, 0 };
    var runtime_length: usize = 3;
    _ = &runtime_length;
    const slice = array[0..runtime_length :0];
    assert(@TypeOf(slice) == [:0]u8);
    assert(slice.len == 3);
}
export fn _zero_terminated_slicing_zig() void {
    return zero_terminated_slicing();
}
pub fn structs() anyerror!void {
    const assert = @import("std").debug.assert;
    const p: PointF = .{ .x = 0.12, .y = 0.34 };
    const p2: PointF = .{ .x = 0.12, .y = undefined };
    assert(p.x == 0.12);
    assert(p.y == 0.34);
    assert(p2.x == 0.12);
    const Vec3 = struct {
        x: f32,
        y: f32,
        z: f32,
        const Self = @This();
        pub fn init(
            x: f32,
            y: f32,
            z: f32,
        ) Self {
            return .{ .x = x, .y = y, .z = z };
        }
        pub fn dot(
            self: Self,
            other: Self,
        ) f32 {
            return (((self.x * other.x) + (self.y * other.y)) + (self.z * other.z));
        }
    };
    const v1 = Vec3.init(1.0, 0.0, 0.0);
    const v2 = Vec3.init(0.0, 1.0, 0.0);
    assert(v1.dot(v2) == 0.0);
    assert(Vec3.dot(v1, v2) == 0.0);
    const Empty = struct {
        const PI: f32 = 3.14;
    };
    assert(Empty.PI == 3.14);
    assert(@sizeOf(Empty) == 0);
    const does_nothing: Empty = .{};
    _ = does_nothing;
}
export fn _structs_zig() void {
    return structs() catch unreachable;
}
pub fn setYBasedOnX(
    x: *f32,
    y: f32,
) void {
    const point: *PointF = @fieldParentPtr("x", x);
    point.y = y;
}
export fn _setYBasedOnX_zig(
    x: *f32,
    y: f32,
) void {
    return setYBasedOnX(
        x,
        y,
    );
}
pub fn field_parent_pointer() anyerror!void {
    const assert = @import("std").debug.assert;
    var point: PointF = .{ .x = 0.1234, .y = 0.5678 };
    setYBasedOnX(&point.x, 0.9);
    assert(point.y == 0.9);
}
export fn _field_parent_pointer_zig() void {
    return field_parent_pointer() catch unreachable;
}
pub fn LinkedList(
    comptime T: type,
) type {
    const temp = struct {
        first: ?*Node,
        last: ?*Node,
        len: usize,
        const Node = struct {
            prev: ?*Node,
            next: ?*Node,
            data: T,
        };
    };
    return temp;
}
pub fn linked_list() anyerror!void {
    const std = @import("std");
    const assert = std.debug.assert;
    const expectEqual = std.testing.expectEqual;
    try (expectEqual(LinkedList(i32), LinkedList(i32)));
    const list: LinkedList(i32) = .{ .first = null, .last = null, .len = 0 };
    assert(list.len == 0);
    const ListOfInts = LinkedList(i32);
    assert(ListOfInts == LinkedList(i32));
    var node: ListOfInts.Node = .{ .prev = null, .next = null, .data = 1234 };
    const list2: LinkedList(i32) = .{ .first = &node, .last = &node, .len = 1 };
    assert(list2.first.?.data == 1234);
}
export fn _linked_list_zig() void {
    return linked_list() catch unreachable;
}
pub fn default_struct_initialization_fields() anyerror!void {
    const x: Foo = .{ .b = 5 };
    if ((x.a + x.b) != 1239) {
        comptime {
            unreachable;
        }
    } else {}
}
export fn _default_struct_initialization_fields_zig() void {
    return default_struct_initialization_fields() catch unreachable;
}
pub fn struct_bitcast() anyerror!void {
    const std = @import("std");
    const assert = std.debug.assert;
    const native_endian = @import("builtin").target.cpu.arch.endian();
    const full: Full = .{ .number = 4660 };
    const divided: Divided = @bitCast(full);
    assert(divided.half1 == 52);
    assert(divided.quarter3 == 2);
    assert(divided.quarter4 == 1);
    const ordered: [2]u8 = @bitCast(full);
    switch (native_endian) {
        .big => {
            assert(ordered[0] == 18);
            assert(ordered[1] == 52);
        },
        .little => {
            assert(ordered[0] == 52);
            assert(ordered[1] == 18);
        },
    }
}
export fn _struct_bitcast_zig() void {
    return struct_bitcast() catch unreachable;
}
pub fn struct_bitcast2() anyerror!void {
    try (struct_bitcast());
    comptime {
        try (struct_bitcast());
    }
}
export fn _struct_bitcast2_zig() void {
    return struct_bitcast2() catch unreachable;
}
pub fn bit_field_offsets() anyerror!void {
    const std = @import("std");
    const assert = std.debug.assert;
    assert(@bitOffsetOf(BitField, "a") == 0);
    assert(@bitOffsetOf(BitField, "b") == 3);
    assert(@bitOffsetOf(BitField, "c") == 6);
    assert(@offsetOf(BitField, "a") == 0);
    assert(@offsetOf(BitField, "b") == 0);
    assert(@offsetOf(BitField, "c") == 0);
}
export fn _bit_field_offsets_zig() void {
    return bit_field_offsets() catch unreachable;
}
pub fn fully_anonymous_struct() anyerror!void {
    const std = @import("std");
    const expect = std.testing.expect;
    const args = .{ .int = @as(u32, 1234), .float = @as(f64, 12.34), .b = true, .s = "hi" };
    try (expect(args.int == 1234));
    try (expect(args.float == 12.34));
    try (expect(args.b));
    try (expect(args.s[0] == 'h'));
    try (expect(args.s[1] == 'i'));
}
export fn _fully_anonymous_struct_zig() void {
    return fully_anonymous_struct() catch unreachable;
}
pub fn tuples() anyerror!void {
    const std = @import("std");
    const expect = std.testing.expect;
    const values_ = .{ @as(u32, 1234), @as(f64, 12.34), true, "hi" } ++ .{false} ** 2;
    try (expect(values_[0] == 1234));
    try (expect(values_[4] == false));
    inline for (values_, 0..) |v, i| {
        if (i != 2) {
            continue;
        } else {}
        try (expect(v));
    }
    try (expect(values_.len == 6));
    try (expect(values_[3][0] == 'h'));
}
export fn _tuples_zig() void {
    return tuples() catch unreachable;
}
pub fn enums() anyerror!void {
    const std = @import("std");
    const expect = std.testing.expect;
    const c = Type.ok;
    try (expect(c == Type.ok));
    try (expect(@intFromEnum(Value.zero) == 0));
    try (expect(@intFromEnum(Value.one) == 1));
    try (expect(@intFromEnum(Value.two) == 2));
    try (expect(@intFromEnum(Value2.hundred) == 100));
    try (expect(@intFromEnum(Value2.thousand) == 1000));
    try (expect(@intFromEnum(Value2.million) == 1000000));
    try (expect(@intFromEnum(Value3.a) == 0));
    try (expect(@intFromEnum(Value3.b) == 8));
    try (expect(@intFromEnum(Value3.c) == 9));
    try (expect(@intFromEnum(Value3.d) == 4));
    try (expect(@intFromEnum(Value3.e) == 5));
    const p = Suit.spades;
    try (expect((!p.isClubs())));
    const q: Foo2 = Foo2.number;
    const what_is_it = switch (q) {
        Foo2.string => blk: {
            break :blk "this is a string";
        },
        Foo2.number => blk: {
            break :blk "this is a number";
        },
        Foo2.none => blk: {
            break :blk "this is a none";
        },
    };
    try (expect(std.mem.eql(u8, what_is_it, "this is a number")));
    try (expect(std.mem.eql(u8, @tagName(Small.three), "three")));
}
export fn _enums_zig() void {
    return enums() catch unreachable;
}
pub fn enum_literals() anyerror!void {
    const std = @import("std");
    const expect = std.testing.expect;
    const color1: Color = .automatic;
    const color2: Color = Color.automatic;
    try (expect(color1 == color2));
    const color = Color.on;
    const result = switch (color) {
        .automatic => blk: {
            break :blk false;
        },
        .on => blk: {
            break :blk true;
        },
        .off => blk: {
            break :blk false;
        },
    };
    try (expect(result));
}
export fn _enum_literals_zig() void {
    return enum_literals() catch unreachable;
}
pub fn switch_non_exhaustive() anyerror!void {
    const std = @import("std");
    const expect = std.testing.expect;
    const number = Number.one;
    const result = switch (number) {
        Number.one => blk: {
            break :blk true;
        },
        Number.two, Number.three => blk: {
            break :blk false;
        },
        else => blk: {
            break :blk false;
        },
    };
    try (expect(result));
    const is_one = switch (number) {
        Number.one => blk: {
            break :blk true;
        },
        else => blk: {
            break :blk false;
        },
    };
    try (expect(is_one));
}
export fn _switch_non_exhaustive_zig() void {
    return switch_non_exhaustive() catch unreachable;
}
pub fn simple_union() anyerror!void {
    const std = @import("std");
    const expect = std.testing.expect;
    var payload: Payload = .{ .int = 1234 };
    try (expect(payload.int == 1234));
    payload = .{ .float = 12.34 };
    try (expect(payload.float == 12.34));
}
export fn _simple_union_zig() void {
    return simple_union() catch unreachable;
}
pub fn switch_on_tagged_union() anyerror!void {
    const std = @import("std");
    const expect = std.testing.expect;
    const c: ComplexType = .{ .ok = 42 };
    try (expect(@as(ComplexTypeTag, c) == ComplexTypeTag.ok));
    switch (c) {
        .ok => |value| {
            try (expect(value == 42));
        },
        .not_ok => {
            unreachable;
        },
    }
    try (expect(std.meta.Tag(ComplexType) == ComplexTypeTag));
}
export fn _switch_on_tagged_union_zig() void {
    return switch_on_tagged_union() catch unreachable;
}
pub fn modify_tagged_union_in_switch() anyerror!void {
    const std = @import("std");
    const expect = std.testing.expect;
    var c: ComplexType = .{ .ok = 42 };
    switch (c) {
        .ok => |*value| {
            value.* += 1;
        },
        .not_ok => {
            unreachable;
        },
    }
    try (expect(c.ok == 43));
}
export fn _modify_tagged_union_in_switch_zig() void {
    return modify_tagged_union_in_switch() catch unreachable;
}
pub fn union_method() anyerror!void {
    const std = @import("std");
    const expect = std.testing.expect;
    var v1: Variant = .{ .int = 1 };
    var v2: Variant = .{ .boolean = false };
    var v3: Variant = .none;
    try (expect(v1.truthy()));
    try (expect((!v2.truthy())));
    try (expect((!v3.truthy())));
}
export fn _union_method_zig() void {
    return union_method() catch unreachable;
}
pub fn anonymous_union_literal_syntax() anyerror!void {
    const std = @import("std");
    const expect = std.testing.expect;
    const i: Number2 = .{ .int = 42 };
    const f: Number2 = .{ .float = 12.34 };
    try (expect(i.int == 42));
    try (expect(f.float == 12.34));
}
export fn _anonymous_union_literal_syntax_zig() void {
    return anonymous_union_literal_syntax() catch unreachable;
}
pub fn access_variable_after_block_scope() void {
    {
        var x: i32 = 1;
        _ = &x;
    }
}
export fn _access_variable_after_block_scope_zig() void {
    return access_variable_after_block_scope();
}
pub fn labeled_block_expression() anyerror!void {
    const std = @import("std");
    const expect = std.testing.expect;
    var y: i32 = 123;
    const x = blk1: {
        y += 1;
        break :blk1 y;
    };
    try (expect(x == 124));
    try (expect(y == 124));
}
export fn _labeled_block_expression_zig() void {
    return labeled_block_expression() catch unreachable;
}
pub fn separate_scopes() void {
    {
        const pi: f32 = 3.14;
        _ = pi;
    }
    {
        var pi: bool = true;
        _ = &pi;
    }
}
export fn _separate_scopes_zig() void {
    return separate_scopes();
}
pub fn switch_simple() anyerror!void {
    const std = @import("std");
    const expect = std.testing.expect;
    const a: u64 = 10;
    const zz: u64 = 103;
    const b = switch (a) {
        1,
        2,
        3,
        => blk: {
            break :blk 0;
        },
        5...100 => blk: {
            break :blk 1;
        },
        101 => blk: {
            const c: u64 = 5;
            break :blk ((c * 2) + 1);
        },
        zz => blk: {
            break :blk zz;
        },
        else => blk: {
            break :blk 9;
        },
    };
    try (expect(b == 1));
}
export fn _switch_simple_zig() void {
    return switch_simple() catch unreachable;
}
pub fn switch_inside_function() anyerror!void {
    const builtin = @import("builtin");
    const os_msg = switch (builtin.target.os.tag) {
        .linux => blk: {
            break :blk "we found a linux user";
        },
        else => blk: {
            break :blk "not a linux user";
        },
    };
    _ = os_msg;
    switch (builtin.target.os.tag) {
        .fuchsia => {
            @compileError("fuchsia not supported");
        },
        else => {},
    }
}
export fn _switch_inside_function_zig() void {
    return switch_inside_function() catch unreachable;
}
pub fn switch_on_tagged_union2() anyerror!void {
    const std = @import("std");
    const expect = std.testing.expect;
    var a: Item = .{ .c = .{ .x = 1, .y = 2 } };
    const b = switch (a) {
        Item.a => |item| blk: {
            break :blk item;
        },
        Item.e => |item| blk: {
            break :blk item;
        },
        Item.c => |*item| blk: {
            item.*.x += 1;
            break :blk 6;
        },
        Item.d => blk: {
            break :blk 8;
        },
    };
    try (expect(b == 6));
    try (expect(a.c.x == 2));
}
export fn _switch_on_tagged_union2_zig() void {
    return switch_on_tagged_union2() catch unreachable;
}
pub fn is_field_optional(
    comptime T: type,
    field_index: usize,
) anyerror!bool {
    const fields = @typeInfo(T).Struct.fields;
    const ret = switch (field_index) {
        inline 0 => |idx| blk: {
            break :blk @typeInfo(fields[idx].type) == .Optional;
        },
        else => blk: {
            break :blk error.IndexOutOfBounds;
        },
    };
    return ret;
}
pub fn using_type_info_with_runtime_values() anyerror!void {
    const std = @import("std");
    const expect = std.testing.expect;
    const expect_error = std.testing.expectError;
    var index: usize = 0;
    try (expect((!try (is_field_optional(Struct1, index)))));
    index += 1;
    try (expect(try (is_field_optional(Struct1, index))));
    index += 1;
    try (expect_error(error.IndexOutOfBounds, is_field_optional(Struct1, index)));
}
export fn _using_type_info_with_runtime_values_zig() void {
    return using_type_info_with_runtime_values() catch unreachable;
}
pub fn with_switch(
    any: AnySlice,
) usize {
    const ret = switch (any) {
        inline else => |slice| blk: {
            break :blk slice.len;
        },
    };
    return ret;
}
pub fn with_for(
    any: AnySlice,
) usize {
    const Tag = @typeInfo(AnySlice).Union.tag_type.?;
    inline for (@typeInfo(Tag).Enum.fields) |field| {
        if (field.value == @intFromEnum(any)) {
            return @field(any, field.name).len;
        } else {}
    }
    unreachable;
}
pub fn inline_for_and_else() anyerror!void {
    const std = @import("std");
    const expect = std.testing.expect;
    const any: AnySlice = .{ .c = "hello" };
    try (expect(with_for(any) == 5));
    try (expect(with_switch(any) == 5));
}
export fn _inline_for_and_else_zig() void {
    return inline_for_and_else() catch unreachable;
}
pub fn while_basic() anyerror!void {
    const std = @import("std");
    const expect = std.testing.expect;
    var i: usize = 0;
    while (i < 10) {
        i += 1;
    }
    try (expect(i == 10));
}
export fn _while_basic_zig() void {
    return while_basic() catch unreachable;
}
pub fn while_break() anyerror!void {
    const std = @import("std");
    const expect = std.testing.expect;
    var i: usize = 0;
    while (true) {
        if (i == 10) {
            break;
        } else {}
        i += 1;
    }
    try (expect(i == 10));
}
export fn _while_break_zig() void {
    return while_break() catch unreachable;
}
pub fn while_continue() anyerror!void {
    const std = @import("std");
    const expect = std.testing.expect;
    var i: usize = 0;
    while (true) {
        i += 1;
        if (i < 10) {
            continue;
        } else {}
        break;
    }
    try (expect(i == 10));
}
export fn _while_continue_zig() void {
    return while_continue() catch unreachable;
}
pub fn rangeHasNumber(
    begin: usize,
    end: usize,
    number: usize,
) bool {
    var i: usize = begin;
    while (i < end) {
        if (i == number) {
            return true;
        } else {}
        i += 1;
    } else {
        return false;
    }
}
export fn _rangeHasNumber_zig(
    begin: usize,
    end: usize,
    number: usize,
) bool {
    return rangeHasNumber(
        begin,
        end,
        number,
    );
}
pub fn while_else() anyerror!void {
    const std = @import("std");
    const expect = std.testing.expect;
    try (expect(rangeHasNumber(0, 10, 5)));
    try (expect((!rangeHasNumber(0, 10, 15))));
}
export fn _while_else_zig() void {
    return while_else() catch unreachable;
}
pub fn while_null_capture() anyerror!void {
    const std = @import("std");
    const expect = std.testing.expect;
    var sum1: u32 = 0;
    EventuallyNullSequence.numbers_left = 3;
    while (EventuallyNullSequence.eventuallyNullSequence()) |value| {
        sum1 += value;
    }
    try (expect(sum1 == 3));
    var sum2: u32 = 0;
    EventuallyNullSequence.numbers_left = 3;
    while (EventuallyNullSequence.eventuallyNullSequence()) |value| {
        sum2 += value;
    } else {
        try (expect(sum2 == 3));
    }
    var i: u32 = 0;
    var sum3: u32 = 0;
    EventuallyNullSequence.numbers_left = 3;
    while (EventuallyNullSequence.eventuallyNullSequence()) |value| {
        sum3 += value;
        i += 1;
    }
    try (expect(i == 3));
}
export fn _while_null_capture_zig() void {
    return while_null_capture() catch unreachable;
}
pub fn while_error_union_capture() anyerror!void {
    const std = @import("std");
    const expect = std.testing.expect;
    var sum1: u32 = 0;
    EventuallyErrorSequence.numbers_left = 3;
    while (EventuallyErrorSequence.eventuallyErrorSequence()) |value| {
        sum1 += value;
    } else |err| {
        try (expect(err == error.ReachedZero));
    }
}
export fn _while_error_union_capture_zig() void {
    return while_error_union_capture() catch unreachable;
}
pub fn typeNameLength(
    comptime T: type,
) usize {
    return @typeName(T).len;
}
pub fn inline_while_loop() anyerror!void {
    const std = @import("std");
    const expect = std.testing.expect;
    comptime var i: usize = 0;
    var sum: usize = 0;
    inline while (i < 3) {
        const T = switch (i) {
            0 => blk: {
                break :blk f32;
            },
            1 => blk: {
                break :blk i8;
            },
            2 => blk: {
                break :blk bool;
            },
            else => blk: {
                break :blk i4;
            },
        };
        sum += typeNameLength(T);
        i += 1;
    }
    try (expect(sum == 9));
}
export fn _inline_while_loop_zig() void {
    return inline_while_loop() catch unreachable;
}
pub fn for_basics() anyerror!void {
    const std = @import("std");
    const expect = std.testing.expect;
    const items = [_]u32{ 4, 5, 3, 4, 0 };
    var sum: u32 = 0;
    for (items) |value| {
        if (value == 0) {
            continue;
        } else {}
        sum += value;
    }
    try (expect(sum == 16));
    for (items[0..1]) |value| {
        sum += value;
    }
    try (expect(sum == 20));
    var sum2: i32 = 0;
    for (items, 0..) |_, i| {
        try (expect(@TypeOf(i) == usize));
        sum2 += @as(i32, @intCast(i));
    }
    try (expect(sum2 == 10));
    var sum3: usize = 0;
    for (0..5) |i| {
        sum3 += i;
    }
    try (expect(sum3 == 10));
}
export fn _for_basics_zig() void {
    return for_basics() catch unreachable;
}
pub fn for_multi_object() anyerror!void {
    const std = @import("std");
    const expect = std.testing.expect;
    const items = [_]usize{ 1, 2, 3 };
    const items2 = [_]usize{ 4, 5, 6 };
    var count: usize = 0;
    for (items, items2) |i, j| {
        count += (i + j);
    }
    try (expect(count == 21));
}
export fn _for_multi_object_zig() void {
    return for_multi_object() catch unreachable;
}
pub fn for_reference() anyerror!void {
    const std = @import("std");
    const expect = std.testing.expect;
    var items = [_]i32{ 3, 4, 2 };
    for (&items) |*value| {
        value.* += 1;
    }
    try (expect(items[0] == 4));
    try (expect(items[1] == 5));
    try (expect(items[2] == 3));
}
export fn _for_reference_zig() void {
    return for_reference() catch unreachable;
}
pub fn for_else() anyerror!void {
    const std = @import("std");
    const expect = std.testing.expect;
    const items = [_]?i32{ 3, 4, null, 5 };
    var sum: i32 = 0;
    for (items) |value| {
        if (value != null) {
            sum += value.?;
        } else {}
    } else {
        try (expect(sum == 12));
    }
}
export fn _for_else_zig() void {
    return for_else() catch unreachable;
}
pub fn inline_for_loop() anyerror!void {
    const std = @import("std");
    const expect = std.testing.expect;
    const items = [_]i32{ 2, 4, 6 };
    var sum: usize = 0;
    inline for (items) |i| {
        const T = switch (i) {
            2 => blk: {
                break :blk f32;
            },
            4 => blk: {
                break :blk i8;
            },
            6 => blk: {
                break :blk bool;
            },
            else => blk: {
                break :blk i4;
            },
        };
        sum += typeNameLength(T);
    }
    try (expect(sum == 9));
}
export fn _inline_for_loop_zig() void {
    return inline_for_loop() catch unreachable;
}
pub fn if_expression() anyerror!void {
    const std = @import("std");
    const expect = std.testing.expect;
    const a: u32 = 5;
    const b: u32 = 4;
    const result = if (a != b) 47 else 3089;
    try (expect(result == 47));
}
export fn _if_expression_zig() void {
    return if_expression() catch unreachable;
}
pub fn if_boolean() anyerror!void {
    const std = @import("std");
    const expect = std.testing.expect;
    const a: u32 = 5;
    const b: u32 = 4;
    if (a != b) {
        try (expect(true));
    } else {
        if (a == 9) {
            unreachable;
        } else {
            unreachable;
        }
    }
}
export fn _if_boolean_zig() void {
    return if_boolean() catch unreachable;
}
pub fn if_error_union() anyerror!void {
    const std = @import("std");
    const expect = std.testing.expect;
    const a: anyerror!u32 = 0;
    if (a) |value| {
        try (expect(value == 0));
    } else |err| {
        _ = err;
        unreachable;
    }
    const b: anyerror!u32 = error.BadValue;
    if (b) |value| {
        _ = value;
        unreachable;
    } else |err| {
        try (expect(err == error.BadValue));
    }
    if (a) |value| {
        try (expect(value == 0));
    } else |err| {
        _ = err;
    }
    if (b) |_| {} else |err| {
        try (expect(err == error.BadValue));
    }
    var c: anyerror!u32 = 3;
    if (c) |*value| {
        value.* = 9;
    } else |_| {
        unreachable;
    }
    if (c) |value| {
        try (expect(value == 9));
    } else |_| {
        unreachable;
    }
}
export fn _if_error_union_zig() void {
    return if_error_union() catch unreachable;
}
pub fn if_optional() anyerror!void {
    const std = @import("std");
    const expect = std.testing.expect;
    const a: ?u32 = 0;
    if (a) |value| {
        try (expect(value == 0));
    } else {
        unreachable;
    }
    const b: ?u32 = null;
    if (b) |_| {
        unreachable;
    } else {
        try (expect(true));
    }
    if (a) |value| {
        try (expect(value == 0));
    } else {}
    if (b == null) {
        try (expect(true));
    } else {}
    var c: ?u32 = 3;
    if (c) |*value| {
        value.* = 2;
    } else {}
    if (c) |value| {
        try (expect(value == 2));
    } else {
        unreachable;
    }
}
export fn _if_optional_zig() void {
    return if_optional() catch unreachable;
}
pub fn if_error_union_with_optional() anyerror!void {
    const std = @import("std");
    const expect = std.testing.expect;
    const a: anyerror!?u32 = 0;
    if (a) |optional_value| {
        try (expect(optional_value == 0));
    } else |err| {
        _ = err;
        unreachable;
    }
    const b: anyerror!?u32 = null;
    if (b) |optional_value| {
        try (expect(optional_value == null));
    } else |_| {
        unreachable;
    }
    const c: anyerror!?u32 = error.BadValue;
    if (c) |optional_value| {
        _ = optional_value;
        unreachable;
    } else |err| {
        try (expect(err == error.BadValue));
    }
    var d: anyerror!?u32 = 3;
    if (d) |*optional_value| {
        if (optional_value.*) |*value| {
            value.* = 9;
        } else {}
    } else |_| {
        unreachable;
    }
    if (d) |optional_value| {
        try (expect(optional_value.? == 9));
    } else |_| {
        unreachable;
    }
}
export fn _if_error_union_with_optional_zig() void {
    return if_error_union_with_optional() catch unreachable;
}
pub fn defer_example() anyerror!usize {
    const std = @import("std");
    const expect = std.testing.expect;
    var a: usize = 1;
    {
        defer {
            a = 2;
        }
        a = 1;
    }
    try (expect(a == 2));
    a = 5;
    return a;
}
export fn _defer_example_zig() usize {
    return defer_example() catch unreachable;
}
pub fn defer_unwinding() anyerror!void {
    const std = @import("std");
    const print = std.debug.print;
    defer {
        print("1 ", .{});
    }
    defer {
        print("2 ", .{});
    }
    if (false) {
        defer {
            print("3 ", .{});
        }
    } else {}
}
export fn _defer_unwinding_zig() void {
    return defer_unwinding() catch unreachable;
}
pub fn add(
    a: i8,
    b: i8,
) i8 {
    if (a == 0) {
        return b;
    } else {}
    return (a + b);
}
pub fn sub2(
    a: i8,
    b: i8,
) i8 {
    return (a - b);
}
export fn _sub2_zig(
    a: i8,
    b: i8,
) i8 {
    return sub2(
        a,
        b,
    );
}
pub fn doOp(
    fnCall: Call2Op.fnCall,
    op1: i8,
    op2: i8,
) i8 {
    return fnCall(op1, op2);
}
pub fn function() anyerror!void {
    const std = @import("std");
    const expect = std.testing.expect;
    _ = add(0, 1);
    _ = sub2(0, 1);
    try (expect(doOp(add, 5, 6) == 11));
    try (expect(doOp(sub2, 5, 6) == (-1)));
}
export fn _function_zig() void {
    return function() catch unreachable;
}
pub fn foo2(
    point: Point,
) i32 {
    return (point.x + point.y);
}
export fn _foo2_zig(
    point: Point,
) i32 {
    return foo2(
        point,
    );
}
pub fn pass_struct_to_function() anyerror!void {
    const std = @import("std");
    const expect = std.testing.expect;
    try (expect(foo2(.{ .x = 1, .y = 2 }) == 3));
}
export fn _pass_struct_to_function_zig() void {
    return pass_struct_to_function() catch unreachable;
}
pub fn add_forty_two(
    T: anytype,
) @TypeOf(T) {
    return (T + 42);
}
pub fn fn_type_inference() anyerror!void {
    const std = @import("std");
    const expect = std.testing.expect;
    try (expect(add_forty_two(1) == 43));
    try (expect(@TypeOf(add_forty_two(1)) == comptime_int));
    const y: i64 = 2;
    try (expect(add_forty_two(y) == 44));
    try (expect(@TypeOf(add_forty_two(y)) == i64));
}
export fn _fn_type_inference_zig() void {
    return fn_type_inference() catch unreachable;
}
pub fn fn_reflection() anyerror!void {
    const std = @import("std");
    const math = std.math;
    const testing = std.testing;
    try (testing.expect(@typeInfo(@TypeOf(testing.expect)).Fn.params[0].type.? == bool));
    try (testing.expect(@typeInfo(@TypeOf(testing.tmpDir)).Fn.return_type.? == testing.TmpDir));
    try (testing.expect(@typeInfo(@TypeOf(math.Log2Int)).Fn.is_generic));
}
export fn _fn_reflection_zig() void {
    return fn_reflection() catch unreachable;
}
pub fn char_to_digit(
    c: u8,
) u8 {
    const std = @import("std");
    const math = std.math;
    const ret = switch (c) {
        '0'...'9' => blk: {
            break :blk (c - '0');
        },
        'A'...'Z' => blk: {
            break :blk ((c - 'A') + 10);
        },
        'a'...'z' => blk: {
            break :blk ((c - 'a') + 10);
        },
        else => blk: {
            break :blk math.maxInt(u8);
        },
    };
    return ret;
}
export fn _char_to_digit_zig(
    c: u8,
) u8 {
    return char_to_digit(
        c,
    );
}
pub fn parse_u64(
    buf: []const u8,
    radix: u8,
) anyerror!u64 {
    var x: u64 = 0;
    for (buf) |c| {
        const digit: u8 = char_to_digit(c);
        if (digit >= radix) {
            return error.InvalidChar;
        } else {}
        var ov = @mulWithOverflow(x, radix);
        if (ov[1] != 0) {
            return error.OverFlow;
        } else {}
        ov = @addWithOverflow(ov[0], digit);
        if (ov[1] != 0) {
            return error.OverFlow;
        } else {}
        x = ov[0];
    }
    return x;
}
pub fn parse_u64_test() anyerror!void {
    const std = @import("std");
    const testing = std.testing;
    const result = try (parse_u64("1234", 10));
    try (testing.expect(result == 1234));
}
export fn _parse_u64_test_zig() void {
    return parse_u64_test() catch unreachable;
}
pub fn foo3(
    err: AllocationError,
) FileOpenError {
    return err;
}
pub fn coerce_subset_to_superset() anyerror!void {
    const std = @import("std");
    const testing = std.testing;
    const err = foo3(AllocationError.OutOfMemory);
    try (testing.expect(err == FileOpenError.OutOfMemory));
}
export fn _coerce_subset_to_superset_zig() void {
    return coerce_subset_to_superset() catch unreachable;
}
pub fn do_a_thing2(
    str: []const u8,
) void {
    const number = parse_u64(str, 10) catch blk: {
        break :blk 13;
    };
    _ = number;
}
pub fn do_a_thing(
    str: []const u8,
) void {
    const number = (parse_u64(str, 10) catch 13);
    _ = number;
}
pub fn catch_() anyerror!void {
    do_a_thing("1234");
    do_a_thing2("1234");
}
export fn _catch__zig() void {
    return catch_() catch unreachable;
}
pub fn captureError(
    captured: *?anyerror,
) anyerror!void {
    errdefer |err| {
        captured.* = err;
    }
    return error.GeneralFailure;
}
pub fn errdefer_capture() anyerror!void {
    const std = @import("std");
    const testing = std.testing;
    var captured: ?anyerror = null;
    if (captureError(&captured)) |_| {
        unreachable;
    } else |err| {
        try (testing.expectEqual(error.GeneralFailure, captured.?));
        try (testing.expectEqual(error.GeneralFailure, err));
    }
}
export fn _errdefer_capture_zig() void {
    return errdefer_capture() catch unreachable;
}
pub fn error_union() anyerror!void {
    const std = @import("std");
    const testing = std.testing;
    var foo: anyerror!i32 = undefined;
    foo = 1234;
    foo = error.SomeError;
    try (testing.expectEqual(@typeInfo(@TypeOf(foo)).ErrorUnion.payload, i32));
    try (testing.expectEqual(@typeInfo(@TypeOf(foo)).ErrorUnion.error_set, anyerror));
}
export fn _error_union_zig() void {
    return error_union() catch unreachable;
}
pub fn merge_error_sets() anyerror!void {
    if (MergeErrorSets.foo()) |_| {
        unreachable;
    } else |err| {
        switch (err) {
            error.OutOfMemory => {
                @panic("unexpected");
            },
            error.PathNotFound => {
                @panic("unexpected");
            },
            error.NotDir => {},
        }
    }
}
export fn _merge_error_sets_zig() void {
    return merge_error_sets() catch unreachable;
}
pub fn add_explicit(
    comptime T: type,
    a: T,
    b: T,
) ErrorSet!T {
    const ov = @addWithOverflow(a, b);
    if (ov[1] != 0) {
        return error.Overflow;
    } else {}
    return ov[0];
}
pub fn inferred_error_set() anyerror!void {
    if (add_explicit(u8, 255, 1)) |_| {
        unreachable;
    } else |err| {
        switch (err) {
            error.Overflow => {},
        }
    }
}
export fn _inferred_error_set_zig() void {
    return inferred_error_set() catch unreachable;
}
pub fn optional_type() anyerror!void {
    const std = @import("std");
    const testing = std.testing;
    var foo: ?i32 = null;
    foo = 1234;
    try (testing.expect(@typeInfo(@TypeOf(foo)).Optional.child == i32));
}
export fn _optional_type_zig() void {
    return optional_type() catch unreachable;
}
pub fn optional_pointer() anyerror!void {
    const std = @import("std");
    const testing = std.testing;
    var ptr: ?*i32 = null;
    var x: i32 = 1;
    ptr = &x;
    try (testing.expect(ptr.?.* == 1));
    try (testing.expect(@sizeOf(?*i32) == @sizeOf(*i32)));
}
export fn _optional_pointer_zig() void {
    return optional_pointer() catch unreachable;
}
pub fn type_coercion_variable_declaration() anyerror!void {
    const a: u8 = 1;
    const b: u16 = a;
    _ = b;
}
export fn _type_coercion_variable_declaration_zig() void {
    return type_coercion_variable_declaration() catch unreachable;
}
pub fn foo4(
    b: u16,
) void {
    _ = b;
}
export fn _foo4_zig(
    b: u16,
) void {
    return foo4(
        b,
    );
}
pub fn type_coercion_function_call() anyerror!void {
    const a: u8 = 1;
    foo4(a);
}
export fn _type_coercion_function_call_zig() void {
    return type_coercion_function_call() catch unreachable;
}
pub fn type_coercion_builtin() anyerror!void {
    const a: u8 = 1;
    const b: u16 = @as(u16, a);
    _ = b;
}
export fn _type_coercion_builtin_zig() void {
    return type_coercion_builtin() catch unreachable;
}
pub fn foo5(
    _: *const i32,
) void {}
pub fn type_coercion_const_qualification() anyerror!void {
    var a: i32 = 1;
    const b: *const i32 = &a;
    foo5(b);
}
export fn _type_coercion_const_qualification_zig() void {
    return type_coercion_const_qualification() catch unreachable;
}
pub fn cast_to_array() anyerror!void {
    const std = @import("std");
    const testing = std.testing;
    const mem = std.mem;
    const window_name = [_][*:0]const u8{"window name"};
    const x: []const ?[*:0]const u8 = &window_name;
    try (testing.expect(mem.eql(u8, mem.span(x[0].?), "window name")));
}
export fn _cast_to_array_zig() void {
    return cast_to_array() catch unreachable;
}
pub fn integer_widening() anyerror!void {
    const std = @import("std");
    const testing = std.testing;
    const a: u8 = 250;
    const b: u16 = a;
    const c: u32 = b;
    const d: u64 = c;
    const e: u64 = d;
    const f: u128 = e;
    try (testing.expect(f == a));
}
export fn _integer_widening_zig() void {
    return integer_widening() catch unreachable;
}
pub fn implicit_unsigned_integer_to_signed_integer() anyerror!void {
    const std = @import("std");
    const testing = std.testing;
    const a: u8 = 250;
    const b: i16 = a;
    try (testing.expect(b == 250));
}
export fn _implicit_unsigned_integer_to_signed_integer_zig() void {
    return implicit_unsigned_integer_to_signed_integer() catch unreachable;
}
pub fn float_widening() anyerror!void {
    const std = @import("std");
    const testing = std.testing;
    const a: f16 = 12.34;
    const b: f32 = a;
    const c: f64 = b;
    const d: f128 = c;
    try (testing.expect(d == a));
}
export fn _float_widening_zig() void {
    return float_widening() catch unreachable;
}
pub fn cast_to_slice() anyerror!void {
    const std = @import("std");
    const testing = std.testing;
    const x1: []const u8 = "hello";
    const x2: []const u8 = &[_]u8{ 104, 101, 108, 108, 111 };
    (try testing.expect(std.mem.eql(u8, x1, x2)));
    const y: []const f32 = &[_]f32{ 1.2, 3.4 };
    (try testing.expect(y[0] == 1.2));
}
export fn _cast_to_slice_zig() void {
    return cast_to_slice() catch unreachable;
}
pub fn cast_to_error_union_slice() anyerror!void {
    const std = @import("std");
    const testing = std.testing;
    const x1: anyerror![]const u8 = "hello";
    const x2: anyerror![]const u8 = &[_]u8{ 104, 101, 108, 108, 111 };
    (try testing.expect(std.mem.eql(u8, (try x1), (try x2))));
    const y: anyerror![]const f32 = &[_]f32{ 1.2, 3.4 };
    (try testing.expect((try y)[0] == 1.2));
}
export fn _cast_to_error_union_slice_zig() void {
    return cast_to_error_union_slice() catch unreachable;
}
pub fn cast_to_optional_slice() anyerror!void {
    const std = @import("std");
    const testing = std.testing;
    const x1: ?[]const u8 = "hello";
    const x2: ?[]const u8 = &[_]u8{ 104, 101, 108, 108, 111 };
    (try testing.expect(std.mem.eql(u8, x1.?, x2.?)));
    const y: ?[]const f32 = &[_]f32{ 1.2, 3.4 };
    (try testing.expect(y.?[0] == 1.2));
}
export fn _cast_to_optional_slice_zig() void {
    return cast_to_optional_slice() catch unreachable;
}
pub fn cast_ptr_to_slice() anyerror!void {
    const std = @import("std");
    const testing = std.testing;
    var buf: [5]u8 = "hello".*;
    const x: []const u8 = &buf;
    (try testing.expect(std.mem.eql(u8, x, "hello")));
    const buf2: [2]f32 = [_]f32{ 1.2, 3.4 };
    const x2: []const f32 = &buf2;
    (try testing.expect(std.mem.eql(f32, x2, &[_]f32{ 1.2, 3.4 })));
}
export fn _cast_ptr_to_slice_zig() void {
    return cast_ptr_to_slice() catch unreachable;
}
pub fn cast_single_item_ptr_to_many_item_ptr() anyerror!void {
    const std = @import("std");
    const testing = std.testing;
    var buf: [5]u8 = "hello".*;
    const x: [*]u8 = &buf;
    (try testing.expect(x[4] == 'o'));
    var buf2: [5]u8 = "hello".*;
    const x3: ?[*]u8 = &buf2;
    (try testing.expect(x3.?[4] == 'o'));
    var x2: i32 = 1234;
    const y: *[1]i32 = &x2;
    const z: [*]i32 = y;
    (try testing.expect(z[0] == 1234));
}
export fn _cast_single_item_ptr_to_many_item_ptr_zig() void {
    return cast_single_item_ptr_to_many_item_ptr() catch unreachable;
}
pub fn coerce_to_optionals() anyerror!void {
    const std = @import("std");
    const testing = std.testing;
    const x: ?i32 = 1234;
    const y: ?i32 = null;
    try (testing.expect(x.? == 1234));
    try (testing.expect(y == null));
}
export fn _coerce_to_optionals_zig() void {
    return coerce_to_optionals() catch unreachable;
}
pub fn coerce_to_optionals_wrapped_in_error_union() anyerror!void {
    const std = @import("std");
    const testing = std.testing;
    const x: anyerror!?i32 = 1234;
    const y: anyerror!?i32 = null;
    try (testing.expect((try x).? == 1234));
    try (testing.expect((try y) == null));
}
export fn _coerce_to_optionals_wrapped_in_error_union_zig() void {
    return coerce_to_optionals_wrapped_in_error_union() catch unreachable;
}
pub fn coercion_to_error_unions() anyerror!void {
    const std = @import("std");
    const testing = std.testing;
    const x: anyerror!i32 = 1234;
    const y: anyerror!i32 = error.Failure;
    try (testing.expect((try x) == 1234));
    try (testing.expectError(error.Failure, y));
}
export fn _coercion_to_error_unions_zig() void {
    return coercion_to_error_unions() catch unreachable;
}
pub fn coercion_to_smaller_integer_type() anyerror!void {
    const std = @import("std");
    const testing = std.testing;
    const x: u64 = 255;
    const y: u8 = x;
    try (testing.expect(y == 255));
}
export fn _coercion_to_smaller_integer_type_zig() void {
    return coercion_to_smaller_integer_type() catch unreachable;
}
pub fn coercion_between_unions_and_enums() anyerror!void {
    const std = @import("std");
    const testing = std.testing;
    const u: U = .{ .two = 12.34 };
    const e: E = u;
    try (testing.expect(e == E.two));
    const three_: E = E.three;
    const u_2: U = three_;
    try (testing.expect(u_2 == E.three));
    const u_3: U = .three;
    try (testing.expect(u_3 == E.three));
    const u_4: U2 = .a;
    try (testing.expect(u_4.tag() == 1));
}
export fn _coercion_between_unions_and_enums_zig() void {
    return coercion_between_unions_and_enums() catch unreachable;
}
pub fn peer_resolve_int_widening() anyerror!void {
    const std = @import("std");
    const testing = std.testing;
    const a: i8 = 12;
    const b: i16 = 34;
    const c = (a + b);
    try (testing.expect(c == 46));
    try (testing.expect(@TypeOf(c) == i16));
}
export fn _peer_resolve_int_widening_zig() void {
    return peer_resolve_int_widening() catch unreachable;
}
pub fn boolToStr(
    b: bool,
) []const u8 {
    return if (b) "true" else "false";
}
pub fn peer_resolve_arrays_of_different_size_to_const_slice() anyerror!void {
    const std = @import("std");
    const testing = std.testing;
    try (testing.expect(std.mem.eql(u8, boolToStr(true), "true")));
    try (testing.expect(std.mem.eql(u8, boolToStr(false), "false")));
    comptime {
        (try testing.expect(std.mem.eql(u8, boolToStr(true), "true")));
        (try testing.expect(std.mem.eql(u8, boolToStr(false), "false")));
    }
}
export fn _peer_resolve_arrays_of_different_size_to_const_slice_zig() void {
    return peer_resolve_arrays_of_different_size_to_const_slice() catch unreachable;
}
pub fn peerResolveArrayConstSlice(
    b: bool,
) anyerror!void {
    const value1 = if (b) "aoeu" else "zz";
    const value2 = if (b) "zz" else "aoeu";
    const std = @import("std");
    const testing = std.testing;
    try (testing.expect(std.mem.eql(u8, value1, "aoeu")));
    try (testing.expect(std.mem.eql(u8, value2, "zz")));
}
pub fn peer_resolve_array_and_const_slice() anyerror!void {
    try (peerResolveArrayConstSlice(true));
    comptime {
        try (peerResolveArrayConstSlice(true));
    }
}
export fn _peer_resolve_array_and_const_slice_zig() void {
    return peer_resolve_array_and_const_slice() catch unreachable;
}
pub fn peerTypeEmptyArrayAndSliceAndError(
    a: bool,
    slice: []u8,
) anyerror![]u8 {
    if (a) {
        return &[_]u8{};
    } else {}
    return slice[0..1];
}
pub fn peer_type_resolution_T_and_optional_T() anyerror!void {
    const std = @import("std");
    const expect = std.testing.expect;
    {
        var data = "hi".*;
        const slice = data[0..];
        (try expect((try peerTypeEmptyArrayAndSliceAndError(true, slice)).len == 0));
        (try expect((try peerTypeEmptyArrayAndSliceAndError(false, slice)).len == 1));
    }
    comptime {
        var data = "hi".*;
        const slice = data[0..];
        (try expect((try peerTypeEmptyArrayAndSliceAndError(true, slice)).len == 0));
        (try expect((try peerTypeEmptyArrayAndSliceAndError(false, slice)).len == 1));
    }
}
export fn _peer_type_resolution_T_and_optional_T_zig() void {
    return peer_type_resolution_T_and_optional_T() catch unreachable;
}
pub fn peerTypeEmptyArrayAndSlice(
    a: bool,
    slice: []const u8,
) []const u8 {
    if (a) {
        return &[_]u8{};
    } else {}
    return slice[0..1];
}
pub fn peer_type_resolution_empty_array_and_slice() anyerror!void {
    const std = @import("std");
    const testing = std.testing;
    try (testing.expect(peerTypeEmptyArrayAndSlice(true, "hi").len == 0));
    try (testing.expect(peerTypeEmptyArrayAndSlice(false, "hi").len == 1));
    comptime {
        (try testing.expect(peerTypeEmptyArrayAndSlice(true, "hi").len == 0));
        (try testing.expect(peerTypeEmptyArrayAndSlice(false, "hi").len == 1));
    }
}
export fn _peer_type_resolution_empty_array_and_slice_zig() void {
    return peer_type_resolution_empty_array_and_slice() catch unreachable;
}
pub fn peer_type_resolution_pointer_and_optional_pointer() anyerror!void {
    const std = @import("std");
    const testing = std.testing;
    const a: *const usize = @ptrFromInt(4886718336);
    const b: ?*usize = @ptrFromInt(4886718336);
    try (testing.expect(a == b));
    try (testing.expect(b == a));
}
export fn _peer_type_resolution_pointer_and_optional_pointer_zig() void {
    return peer_type_resolution_pointer_and_optional_pointer() catch unreachable;
}
pub fn turn_hashmap_into_set_with_void() anyerror!void {
    const std = @import("std");
    const expect = std.testing.expect;
    var map = std.AutoHashMap(i32, void).init(std.heap.page_allocator);
    defer {
        map.deinit();
    }
    try (map.put(1, {}));
    try (map.put(2, {}));
    try (expect(map.contains(2)));
    try (expect((!map.contains(3))));
    _ = map.remove(2);
    try (expect((!map.contains(2))));
}
export fn _turn_hashmap_into_set_with_void_zig() void {
    return turn_hashmap_into_set_with_void() catch unreachable;
}
pub fn max(
    comptime T: type,
    a: T,
    b: T,
) T {
    if (T == bool) {
        return a or b;
    } else {
        if (a > b) {
            return a;
        } else {
            return b;
        }
    }
}
pub fn try_to_compare_bools() anyerror!void {
    const std = @import("std");
    const expect = std.testing.expect;
    (try expect(max(bool, false, true) == true));
}
export fn _try_to_compare_bools_zig() void {
    return try_to_compare_bools() catch unreachable;
}
pub fn one(
    value: i32,
) i32 {
    return (value + 1);
}
export fn _one_zig(
    value: i32,
) i32 {
    return one(
        value,
    );
}
pub fn two(
    value: i32,
) i32 {
    return (value + 2);
}
export fn _two_zig(
    value: i32,
) i32 {
    return two(
        value,
    );
}
pub fn three(
    value: i32,
) i32 {
    return (value + 3);
}
export fn _three_zig(
    value: i32,
) i32 {
    return three(
        value,
    );
}
pub fn performFn(
    comptime prefix_char: u8,
    start_value: i32,
) i32 {
    _ = one(0);
    _ = two(0);
    _ = three(0);
    const cmd_fns = [_]CmdFn{ .{ .name = "one", .func = one }, .{ .name = "two", .func = two }, .{ .name = "three", .func = three } };
    var result: i32 = start_value;
    comptime var i = 0;
    inline while (i < cmd_fns.len) {
        if (cmd_fns[i].name[0] == prefix_char) {
            result = cmd_fns[i].func(result);
        } else {}
        i += 1;
    }
    return result;
}
pub fn perform_fn() anyerror!void {
    const std = @import("std");
    const expect = std.testing.expect;
    try (expect(performFn('t', 1) == 6));
    try (expect(performFn('o', 0) == 1));
    try (expect(performFn('w', 99) == 99));
}
export fn _perform_fn_zig() void {
    return perform_fn() catch unreachable;
}
pub fn fibonacci(
    index: u32,
) u32 {
    if (index < 2) {
        return index;
    } else {}
    return (fibonacci((index - 1)) + fibonacci((index - 2)));
}
export fn _fibonacci_zig(
    index: u32,
) u32 {
    return fibonacci(
        index,
    );
}
pub fn fibonacci_test() anyerror!void {
    const std = @import("std");
    const expect = std.testing.expect;
    try (expect(fibonacci(7) == 13));
    comptime {
        (try expect(fibonacci(7) == 13));
    }
}
export fn _fibonacci_test_zig() void {
    return fibonacci_test() catch unreachable;
}
pub fn List(
    comptime T: type,
) type {
    const Temp = struct {
        items: []T,
        len: usize,
    };
    return Temp;
}
pub fn list_test() anyerror!void {
    const std = @import("std");
    const expect = std.testing.expect;
    var buffer: [10]i32 = undefined;
    const list: List(i32) = .{ .items = &buffer, .len = 0 };
    try (expect(list.len == 0));
}
export fn _list_test_zig() void {
    return list_test() catch unreachable;
}
pub fn decl_access_by_string() anyerror!void {
    const std = @import("std");
    const expect = std.testing.expect;
    try (expect(@field(Point4, "z") == 1));
    Point4.z = 2;
    try (expect(@field(Point4, "z") == 2));
}
export fn _decl_access_by_string_zig() void {
    return decl_access_by_string() catch unreachable;
}
pub fn has_decl() anyerror!void {
    const std = @import("std");
    const expect = std.testing.expect;
    try (expect(@hasDecl(Foo5, "blah")));
    try (expect(@hasDecl(Foo5, "hi")));
    try (expect((!@hasDecl(Foo5, "nope"))));
    try (expect((!@hasDecl(Foo5, "nope1234"))));
}
export fn _has_decl_zig() void {
    return has_decl() catch unreachable;
}
pub fn vector_shuffle() anyerror!void {
    const std = @import("std");
    const expect = std.testing.expect;
    const a: @Vector(7, u8) = @Vector(7, u8){ 'o', 'l', 'h', 'e', 'r', 'z', 'w' };
    const b: @Vector(4, u8) = @Vector(4, u8){ 'w', 'd', '!', 'x' };
    const mask1 = @Vector(5, i32){ 2, 3, 1, 1, 0 };
    const res1: @Vector(5, u8) = @shuffle(u8, a, undefined, mask1);
    try (expect(std.mem.eql(u8, &@as([5]u8, res1), "hello")));
    const mask2 = @Vector(6, i32){ (-1), 0, 4, 1, (-2), (-3) };
    const res2: @Vector(6, u8) = @shuffle(u8, a, b, mask2);
    try (expect(std.mem.eql(u8, &@as([6]u8, res2), "world!")));
}
export fn _vector_shuffle_zig() void {
    return vector_shuffle() catch unreachable;
}
pub fn vector_reduce() anyerror!void {
    const std = @import("std");
    const expect = std.testing.expect;
    const V = @Vector(4, i32);
    const value: V = .{ 1, (-1), 1, (-1) };
    const result = value > @as(V, @splat(0));
    comptime {
        try (expect(@TypeOf(result) == @Vector(4, bool)));
    }
    const is_all_true = @reduce(.And, result);
    comptime {
        try (expect(@TypeOf(is_all_true) == bool));
    }
    try (expect(is_all_true == false));
}
export fn _vector_reduce_zig() void {
    return vector_reduce() catch unreachable;
}
pub fn round_test() anyerror!void {
    const std = @import("std");
    const expect = std.testing.expect;
    try (expect(@round(1.4) == 1));
    try (expect(@round(1.5) == 2));
    try (expect(@round((-1.4)) == (-1)));
    try (expect(@round((-2.5)) == (-3)));
}
export fn _round_test_zig() void {
    return round_test() catch unreachable;
}
pub fn List2(
    comptime T: type,
) type {
    const Temp = struct {
        items: []T,
        const Self = @This();
        pub fn length(
            self: Self,
        ) usize {
            return self.items.len;
        }
    };
    return Temp;
}
pub fn this_test() anyerror!void {
    const std = @import("std");
    const expect = std.testing.expect;
    var items = [_]i32{ 1, 2, 3, 4 };
    const list: List2(i32) = .{ .items = items[0..] };
    try (expect(list.length() == 4));
}
export fn _this_test_zig() void {
    return this_test() catch unreachable;
}
pub fn integer_truncation() anyerror!void {
    const std = @import("std");
    const expect = std.testing.expect;
    const a: u16 = 43981;
    const b: u8 = @truncate(a);
    try (expect(b == 205));
}
export fn _integer_truncation_zig() void {
    return integer_truncation() catch unreachable;
}
