from enum import Enum, auto
import sys
import json
from zyg.zyg import *


@zig()
def hello() -> Error[anyerror, void]:
    std: Const[Infer] = Import("std")
    stdout: Const[Infer] = std.io.getStdOut().writer()
    Try(stdout.print("Hello, {s}!\n", ("world",)))


def test_hello(capfd):
    hello()
    captured = capfd.readouterr()
    assert captured.out == "Hello, world!\n"


@zig()
def hello2() -> void:
    std: Const[Infer] = Import("std")
    std.debug.print("Hello, world!\n", ())


def test_hello2(capfd):
    hello2()
    captured = capfd.readouterr()
    assert captured.err == "Hello, world!\n"


@zig(print_generated=True)
def values() -> void:
    std: Const[Infer] = Import("std")
    print: Const[Infer] = std.debug.print
    assert_: Const[Infer] = std.debug.assert_

    one_plus_one: Const[i32] = 1 + 1
    print("1 + 1 = {}\n", (one_plus_one,))

    seven_div_three: Const[f32] = 7.0 / 3.0
    print("7.0 / 3.0 = {}\n", (seven_div_three,))

    print("{}\n{}\n{}\n", (True and False, True or False, not True))

    optional_value: Var[Optional[Slice[Const[u8]]]] = None
    assert_(optional_value == None)

    print("\noptional 1\ntype: {}\nvalue: {?s}\n",
          (TypeOf(optional_value), optional_value,))

    optional_value = "hi"
    assert_(optional_value != None)

    print("\noptional 2\ntype: {}\nvalue: {?s}\n",
          (TypeOf(optional_value), optional_value,))

    number_or_error: Var[Error[anyerror, i32]] = error.ArgNotFound

    print("\nerror union 1\ntype: {}\nvalue: {!}\n",
          (TypeOf(number_or_error), number_or_error))

    number_or_error = 1234

    print("\nerror union 2\ntype: {}\nvalue: {!}\n",
          (TypeOf(number_or_error), number_or_error,))


def test_values(capfd):
    values()
    captured = capfd.readouterr()
    expected_out = """1 + 1 = 2
7.0 / 3.0 = 2.3333333e0
false
true
false

optional 1
type: ?[]const u8
value: null

optional 2
type: ?[]const u8
value: hi

error union 1
type: anyerror!i32
value: error.ArgNotFound

error union 2
type: anyerror!i32
value: 1234
"""
    assert captured.err == expected_out


# TODO: Confirm all zig types are supported

@zig()
def string_literals() -> void:
    std: Const[Infer] = Import("std")
    print: Const[Infer] = std.debug.print
    mem: Const[Infer] = std.mem

    bytes: Const[Slice[Const[u8]]] = "hello"
    print("{s}\n", (TypeOf(bytes),))
    print("{d}\n", (bytes.len,))
    print("{c}\n", (bytes[1],))
    print("{d}\n", (bytes[5],))
    print("{s}\n", ('e' == '\x65',))
    print("{d}\n", (u'1f4a9',))
    print("{d}\n", ('💯',))
    print("{u}\n", ('⚡',))
    print("{s}\n", (mem.eql(u8, "hello", "h\x65llo"),))
    print("{s}\n", (mem.eql(u8, "💯", "\xf0\x9f\x92\xaf"),))

    invalid_utf8: Const[Slice[Const[u8]]] = "\xff\xfe"
    print("0x{x}\n", (invalid_utf8[1],))
    print("0x{x}\n", ("💯"[1],))


# def test_string_literals(capfd):
#     string_literals()
#     captured = capfd.readouterr()
#     expected_out = """[]const u8
# 5
# 101
# 0
# true
# 127169
# 💯
# ⚡
# true
# true
# 0xff
# 0x9f
# """
#     assert captured.err == expected_out

@zig()
def assign_undefined() -> void:
    std: Const[Infer] = Import("std")
    print: Const[Infer] = std.debug.print

    x: Var[i32] = undefined
    x = 1
    print("{d}\n", (x,))


def test_assign_undefined(capfd):
    assign_undefined()
    captured = capfd.readouterr()
    assert captured.err == "1\n"


@zig_struct()
class Point(ZigStruct):
    x: i32
    y: i32


@zig()
def make_point(x: i32) -> Point:
    return {x: x, y: x * 2}


@zig()
def arrays() -> void:
    std: Const[Infer] = Import("std")
    mem: Const[Infer] = std.mem
    assert_: Const[Infer] = std.debug.assert_

    message: Const[Infer] = list(
        [chr('h'), chr('e'), chr('l'), chr('l'), chr('o')], u8)
    alt_message: Const[Array[5, u8]] = (
        chr('h'), chr('e'), chr('l'), chr('l'), chr('o'))
    with comptime:
        assert_(mem.eql(u8, ref(message), ref(alt_message)))
        assert_(message.len == 5)

    same_message: Const[Infer] = "hello"
    with comptime:
        assert_(mem.eql(u8, ref(message), same_message))

    sum: Var[usize] = 0
    for byte in message:
        sum += byte
    assert_(sum == chr('h') + chr('e') + chr('l') * 2 + chr('o'))

    some_integers: Var[Array[100, i32]] = undefined
    for *item, i in (ref(some_integers), range(0, None)):
        item.deref = IntCast(i)
    assert_(some_integers[10] == 10)
    assert_(some_integers[99] == 99)

    part_one: Const[Infer] = list([1, 2, 3, 4], i32)
    part_two: Const[Infer] = list([5, 6, 7, 8], i32)
    all_of_it: Const[Infer] = cat(part_one, part_two)
    assert_(mem.eql(i32, ref(all_of_it), ref(
        list([1, 2, 3, 4, 5, 6, 7, 8], i32))))

    hello_: Const[Infer] = "hello"
    world: Const[Infer] = "world"
    hello_world: Const[Infer] = cat(hello_, " ", world)
    assert_(mem.eql(u8, hello_world, "hello world"))

    pattern: Const[Infer] = repeat("ab", 3)
    assert_(mem.eql(u8, pattern, "ababab"))

    all_zero: Const[Infer] = repeat(list([0], u16), 10)
    assert_(all_zero.len == 10)
    assert_(all_zero[5] == 0)

    more_points: Const[Array[10, Point]] = repeat(
        list([make_point(3)], Point), 10)
    assert_(more_points[4].x == 3)
    assert_(more_points[4].y == 6)
    assert_(more_points.len == 10)


def test_arrays():
    arrays()


@zig()
def multidimensional_arrays() -> void:
    std: Const[Infer] = Import("std")
    assert_: Const[Infer] = std.debug.assert_
    mat4x4: Const[Array[4, Array[4, f32]]] = (
        (1.0, 0.0, 0.0, 0.0),
        (0.0, 1.0, 0.0, 1.0),
        (0.0, 0.0, 1.0, 0.0),
        (0.0, 0.0, 0.0, 1.0),
    )
    assert_(mat4x4[1][1] == 1.0)

    all_zero: Const[Array[4, Array[4, f32]]] = (
        (0.0, 0.0, 0.0, 0.0),
        (0.0, 0.0, 0.0, 0.0),
        (0.0, 0.0, 0.0, 0.0),
        (0.0, 0.0, 0.0, 0.0),
    )
    assert_(all_zero[0][0] == 0.0)


def test_multidimensional_arrays():
    multidimensional_arrays()


@zig()
def zero_terminated_sentinel_array() -> void:
    std: Const[Infer] = Import("std")
    assert_: Const[Infer] = std.debug.assert_

    array: Const[Array[4, 0, u8]] = (1, 2, 3, 4)
    assert_(TypeOf(array) == type(Array[4, 0, u8]))
    assert_(array.len == 4)
    assert_(array[4] == 0)


@zig()
def extra_zeros_in_zero_terminated_sentinel_array() -> void:
    std: Const[Infer] = Import("std")
    assert_: Const[Infer] = std.debug.assert_

    array: Const[Array[4, 0, u8]] = (1, 0, 0, 4)
    assert_(TypeOf(array) == type(Array[4, 0, u8]))
    assert_(array.len == 4)
    assert_(array[4] == 0)


def test_zero_terminated_sentinel_array():
    zero_terminated_sentinel_array()
    extra_zeros_in_zero_terminated_sentinel_array()


@zig()
def basic_vector() -> void:
    std: Const[Infer] = Import("std")
    assert_: Const[Infer] = std.debug.assert_

    a: Const[Infer] = Vector(4, i32)(1, 2, 3, 4)
    b: Const[Infer] = Vector(4, i32)(5, 6, 7, 8)
    c: Const[Infer] = a + b

    assert_(c[0] == 6)
    assert_(c[1] == 8)
    assert_(c[2] == 10)
    assert_(c[3] == 12)


@zig()
def vector_conversion() -> Error[anyerror, void]:
    std: Const[Infer] = Import("std")
    testing: Const[Infer] = std.testing

    arr1: Const[Array[4, f32]] = (1.1, 3.2, 4.5, 5.6)
    vec: Const[Vector(4, f32)] = arr1
    arr2: Const[Array[4, f32]] = vec
    Try(testing.expectEqual(arr1, arr2))

    vec2: Const[Vector(2, f32)] = arr1[1:3].deref

    slice: Const[Slice[Const[f32]]] = ref(arr1)
    offset: Var[u32] = 1
    _ = ref(offset)
    vec3: Const[Vector(2, f32)] = slice[offset:][0:2].deref
    Try(testing.expectEqual(slice[offset], vec2[0]))
    Try(testing.expectEqual(slice[offset + 1], vec2[1]))
    Try(testing.expectEqual(vec2, vec3))


def test_vector():
    basic_vector()
    vector_conversion()


@zig()
def address_of_syntax() -> void:
    std: Const[Infer] = Import("std")
    assert_: Const[Infer] = std.debug.assert_

    x: Const[i32] = 1234
    x_ptr: Const[Infer] = ref(x)
    assert_(TypeOf(x_ptr) == type(Ptr[Const[i32]]))
    assert_(x_ptr.deref == 1234)

    y: Var[i32] = 5678
    y_ptr: Const[Infer] = ref(y)
    assert_(TypeOf(y_ptr) == type(Ptr[i32]))
    y_ptr.deref += 1
    assert_(y_ptr.deref == 5679)


@zig()
def pointer_array_access() -> void:
    std: Const[Infer] = Import("std")
    assert_: Const[Infer] = std.debug.assert_

    array: Var[Array[10, u8]] = list([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], u8)
    ptr: Const[Infer] = ref(array[2])
    assert_(TypeOf(ptr) == type(Ptr[u8]))
    assert_(array[2] == 3)
    ptr.deref += 1
    assert_(array[2] == 4)


@ zig()
def slice_syntax() -> void:
    std: Const[Infer] = Import("std")
    assert_: Const[Infer] = std.debug.assert_

    x: Var[i32] = 1234
    x_ptr: Const[Infer] = ref(x)
    x_array_ptr: Const[Infer] = x_ptr[0:1]
    assert_(TypeOf(x_array_ptr) == type(Ptr[Array[1, i32]]))
    x_many_ptr: Const[Array[i32]] = x_array_ptr
    assert_(x_many_ptr[0] == 1234)


def test_single_item_pointer():
    address_of_syntax()
    pointer_array_access()
    slice_syntax()


@zig()
def pointer_arithmetic_with_slices() -> void:
    std: Const[Infer] = Import("std")
    assert_: Const[Infer] = std.debug.assert_

    array: Var[Infer] = list([1, 2, 3, 4], i32)
    length: Var[usize] = 0
    _ = ref(length)
    slice: Var[Infer] = array[length:array.len]

    assert_(slice[0] == 1)
    assert_(slice.len == 4)

    slice.ptr += 1
    assert_(slice[0] == 2)
    assert_(slice.len == 4)


@zig()
def pointer_arithmetic_with_many_item_pointer() -> void:
    std: Const[Infer] = Import("std")
    assert_: Const[Infer] = std.debug.assert_

    array: Const[Infer] = list([1, 2, 3, 4], i32)
    ptr: Var[Array[Const[i32]]] = ref(array)
    assert_(ptr[0] == 1)
    ptr += 1
    assert_(ptr[0] == 2)
    assert_(ptr[1:] == ptr + 1)

    # I don't think this is supported in zig
    # assert_(ref(ptr[1]) - ref(ptr[0]) == 1)


def test_pointer_arithmetic():
    pointer_arithmetic_with_slices()
    pointer_arithmetic_with_many_item_pointer()


@zig()
def comptime_pointers() -> Error[anyerror, void]:
    std: Const[Infer] = Import("std")
    testing: Const[Infer] = std.testing
    with comptime:
        x: Var[i32] = 1
        ptr: Const[Infer] = ref(x)
        ptr.deref += 1
        x += 1
        Try(testing.expect(ptr.deref == 3))


def test_comptime_pointers():
    comptime_pointers()


@zig()
def integer_pointer_conversion() -> Error[anyerror, void]:
    std: Const[Infer] = Import("std")
    testing: Const[Infer] = std.testing
    ptr: Const[Ptr[i32]] = PtrFromInt(0xdeadbee0)
    addr: Const[Infer] = IntFromPtr(ptr)
    Try(testing.expect(TypeOf(addr) == usize))
    Try(testing.expect(addr == 0xdeadbee0))


def test_integer_pointer_conversion():
    integer_pointer_conversion()


@zig()
def comptime_ptr_from_int() -> Error[anyerror, void]:
    std: Const[Infer] = Import("std")
    testing: Const[Infer] = std.testing
    with comptime:
        ptr: Const[Ptr[i32]] = PtrFromInt(0xdeadbee0)
        addr: Const[Infer] = IntFromPtr(ptr)
        Try(testing.expect(TypeOf(addr) == usize))
        Try(testing.expect(addr == 0xdeadbee0))


def test_comptime_ptr_from_int():
    comptime_ptr_from_int()


@zig()
def basic_slices() -> Error[anyerror, void]:
    std: Const[Infer] = Import("std")
    assert_: Const[Infer] = std.debug.assert_
    expectEqualSlices: Const[Infer] = std.testing.expectEqualSlices

    array: Var[Infer] = list([1, 2, 3, 4], i32)
    known_at_runtime_zero: Var[usize] = 0
    _ = ref(known_at_runtime_zero)
    slice: Const[Infer] = array[known_at_runtime_zero:array.len]

    alt_slice: Const[Slice[Const[i32]]] = ref((1, 2, 3, 4))

    Try(expectEqualSlices(i32, slice, alt_slice))
    assert_(TypeOf(slice) == type(Slice[i32]))
    assert_(ref(slice[0]) == ref(array[0]))
    assert_(slice.len == array.len)

    array_ptr: Const[Infer] = array[0:array.len]
    assert_(TypeOf(array_ptr) == type(Ptr[Array[array.len, i32]]))

    runtime_start: Var[usize] = 1
    _ = ref(runtime_start)
    length: Const[Infer] = 2
    array_ptr_len: Const[Infer] = array[runtime_start:][0:length]
    assert_(TypeOf(array_ptr_len) == type(Ptr[Array[length, i32]]))

    assert_(TypeOf(ref(slice[0])) == type(Ptr[i32]))
    assert_(TypeOf(slice.ptr) == type(Array[i32]))
    assert_(IntFromPtr(slice.ptr) == IntFromPtr(ref(slice[0])))

    slice[10] += 1

    empty1: Const[Infer] = ref(list([], u8))
    empty2: Const[Slice[u8]] = ref(())
    assert_(empty1.len == 0)
    assert_(empty2.len == 0)


def test_basic_slices():
    basic_slices()


@zig()
def using_slices_for_strings() -> Error[anyerror, void]:
    std: Const[Infer] = Import("std")
    assert_: Const[Infer] = std.debug.assert_
    fmt: Const[Infer] = std.fmt

    hello_: Const[Slice[Const[u8]]] = "hello"
    world: Const[Slice[Const[u8]]] = "世界"

    all_together: Var[Array[100, u8]] = undefined
    start: Var[usize] = 0
    _ = ref(start)
    all_together_slice: Const[Infer] = all_together[start:]
    hello_world: Const[Infer] = Try(fmt.bufPrint(
        all_together_slice, "{s} {s}", (hello_, world)))

    assert_(std.mem.eql(u8, hello_world, "hello 世界"))


@zig()
def slice_pointer() -> Error[anyerror, void]:
    std: Const[Infer] = Import("std")
    assert_: Const[Infer] = std.debug.assert_

    array: Var[Array[10, u8]] = undefined
    ptr: Const[Infer] = ref(array)
    assert_(TypeOf(ptr) == type(Ptr[Array[10, u8]]))

    start: Var[usize] = 0
    end: Var[usize] = 5
    _ = ref(start)
    _ = ref(end)
    slice: Const[Infer] = ptr[start:end]
    assert_(TypeOf(slice) == type(Slice[u8]))
    slice[2] = 3
    assert_(array[2] == 3)

    ptr2: Const[Infer] = slice[2:3]
    assert_(ptr2.len == 1)
    assert_(ptr2[0] == 3)
    assert_(TypeOf(ptr2) == type(Ptr[Array[1, u8]]))


def test_slices():
    using_slices_for_strings()
    slice_pointer()


@zig()
def zero_terminated_slice() -> void:
    std: Const[Infer] = Import("std")
    assert_: Const[Infer] = std.debug.assert_

    slice: Const[Slice[0, Const[u8]]] = "hello"
    assert_(slice.len == 5)
    assert_(slice[5] == 0)


@zig()
def zero_terminated_slicing() -> void:
    std: Const[Infer] = Import("std")
    assert_: Const[Infer] = std.debug.assert_

    array: Var[Infer] = list([3, 2, 1, 0, 3, 2, 1, 0], u8)
    runtime_length: Var[usize] = 3
    _ = ref(runtime_length)
    slice: Const[Infer] = array[0:runtime_length:0]
    assert_(TypeOf(slice) == type(Slice[0, u8]))
    assert_(slice.len == 3)


def test_zero_terminated_slice():
    zero_terminated_slice()
    zero_terminated_slicing()


@zig_struct()
class PointF(ZigStruct):
    x: f32
    y: f32


@zig_struct()
class Point2(ZigPackedStruct):
    x: f32
    y: f32


@zig()
def structs() -> Error[anyerror, void]:
    assert_: Const[Infer] = Import("std").debug.assert_
    p: Const[PointF] = {x: 0.12, y: 0.34}
    p2: Const[PointF] = {x: 0.12, y: undefined}
    assert_(p.x == 0.12)
    assert_(p.y == 0.34)
    assert_(p2.x == 0.12)

    class Vec3(ZigStruct):
        x: f32
        y: f32
        z: f32

        Self: Const[Infer] = This()

        def init(x: f32, y: f32, z: f32) -> Self:
            return {x: x, y: y, z: z}

        def dot(self: Self, other: Self) -> f32:
            return self.x * other.x + self.y * other.y + self.z * other.z

    v1: Const[Infer] = Vec3.init(1.0, 0.0, 0.0)
    v2: Const[Infer] = Vec3.init(0.0, 1.0, 0.0)
    assert_(v1.dot(v2) == 0.0)
    assert_(Vec3.dot(v1, v2) == 0.0)

    class Empty(ZigStruct):
        PI: Const[f32] = 3.14

    assert_(Empty.PI == 3.14)
    assert_(SizeOf(Empty) == 0)

    does_nothing: Const[Empty] = {}
    _ = does_nothing


@zig()
def setYBasedOnX(x: Ptr[f32], y: f32) -> void:
    point: Const[Ptr[PointF]] = FieldParentPtr("x", x)
    point.y = y


@zig()
def field_parent_pointer() -> Error[anyerror, void]:
    assert_: Const[Infer] = Import("std").debug.assert_
    point: Var[PointF] = {x: 0.1234, y: 0.5678}
    setYBasedOnX(ref(point.x), 0.9)
    assert_(point.y == 0.9)


def test_structs():
    structs()
    field_parent_pointer()


@zig(export=False)
def LinkedList(T: comptime | type) -> type:
    class temp(ZigStruct):
        first: Optional[Ptr[Node]]
        last: Optional[Ptr[Node]]
        len: usize

        class Node(ZigStruct):
            prev: Optional[Ptr[Node]]
            next: Optional[Ptr[Node]]
            data: T

    return temp


@zig()
def linked_list() -> Error[anyerror, void]:
    std: Const[Infer] = Import("std")
    assert_: Const[Infer] = std.debug.assert_
    expectEqual: Const[Infer] = std.testing.expectEqual

    Try(expectEqual(LinkedList(i32), LinkedList(i32)))

    list: Const[LinkedList(i32)] = {
        first: None,
        last: None,
        len: 0
    }
    assert_(list.len == 0)

    ListOfInts: Const[Infer] = LinkedList(i32)
    assert_(ListOfInts == LinkedList(i32))
    node: Var[ListOfInts.Node] = {
        prev: None,
        next: None,
        data: 1234,
    }
    list2: Const[LinkedList(i32)] = {
        first: ref(node),
        last: ref(node),
        len: 1,
    }

    assert_(list2.first.unwrap.data == 1234)


def test_linked_list():
    linked_list()


@zig_struct()
class Foo(ZigStruct):
    a: i32 = 1234
    b: i32


@zig()
def default_struct_initialization_fields() -> Error[anyerror, void]:

    x: Const[Foo] = {
        b: 5
    }
    if x.a + x.b != 1239:
        with comptime:
            unreachable()


def test_default_struct_initialization_fields():
    default_struct_initialization_fields()


@zig_struct()
class Full(ZigPackedStruct):
    number: u16


class u4(ZigType):
    ...


@zig_struct()
class Divided(ZigPackedStruct):
    half1: u8
    quarter3: u4
    quarter4: u4


@zig()
def struct_bitcast() -> Error[anyerror, void]:
    std: Const[Infer] = Import("std")
    assert_: Const[Infer] = std.debug.assert_
    native_endian: Const[Infer] = Import("builtin").target.cpu.arch.endian()

    full: Const[Full] = {number: 0x1234}
    divided: Const[Divided] = BitCast(full)
    assert_(divided.half1 == 0x34)
    assert_(divided.quarter3 == 0x2)
    assert_(divided.quarter4 == 0x1)

    ordered: Const[Array[2, u8]] = BitCast(full)

    match native_endian:
        case enum(big):
            assert_(ordered[0] == 0x12)
            assert_(ordered[1] == 0x34)
        case enum(little):
            assert_(ordered[0] == 0x34)
            assert_(ordered[1] == 0x12)


@zig()
def struct_bitcast2() -> Error[anyerror, void]:
    Try(struct_bitcast())
    with comptime:
        Try(struct_bitcast())


def test_struct_bitcast():
    struct_bitcast2()


class u3(ZigType):
    ...


class u2(ZigType):
    ...


@zig_struct()
class BitField(ZigPackedStruct):
    a: u3
    b: u3
    c: u2


@zig()
def bit_field_offsets() -> Error[anyerror, void]:
    std: Const[Infer] = Import("std")
    assert_: Const[Infer] = std.debug.assert_

    assert_(BitOffsetOf(BitField, "a") == 0)
    assert_(BitOffsetOf(BitField, "b") == 3)
    assert_(BitOffsetOf(BitField, "c") == 6)

    assert_(OffsetOf(BitField, "a") == 0)
    assert_(OffsetOf(BitField, "b") == 0)
    assert_(OffsetOf(BitField, "c") == 0)


def test_bit_field_offsets():
    bit_field_offsets()


@zig()
def fully_anonymous_struct() -> Error[anyerror, void]:
    std: Const[Infer] = Import("std")
    expect: Const[Infer] = std.testing.expect

    args: Const[Infer] = {
        int: As(u32, 1234),
        float: As(f64, 12.34),
        b: True,
        s: "hi",
    }

    Try(expect(args.int == 1234))
    Try(expect(args.float == 12.34))
    Try(expect(args.b))
    Try(expect(args.s[0] == chr('h')))
    Try(expect(args.s[1] == chr('i')))


def test_fully_anonymous_struct():
    fully_anonymous_struct()


@zig()
def tuples() -> Error[anyerror, void]:
    std: Const[Infer] = Import("std")
    expect: Const[Infer] = std.testing.expect

    values_: Const[Infer] = cat((
        As(u32, 1234),
        As(f64, 12.34),
        True,
        "hi"
    ), repeat((False,), 2))
    Try(expect(values_[0] == 1234))
    Try(expect(values_[4] == False))

    with inline:
        for v, i in (values_, range(0, None)):
            if i != 2:
                continue
            Try(expect(v))

    Try(expect(values_.len == 6))
    Try(expect(values_[3][0] == chr('h')))


def test_tuples():
    tuples()


class u2(ZigType):
    ...


@zig_enum()
class Type(ZigEnum):
    ok = auto()
    not_ok = auto()


@zig_enum()
class Value(ZigEnum, u2):
    zero = auto()
    one = auto()
    two = auto()


@zig_enum()
class Value2(ZigEnum, u32):
    hundred = 100
    thousand = 1000
    million = 1000000


@zig_enum()
class Value3(ZigEnum, u4):
    a = auto()
    b = 8
    c = auto()
    d = 4
    e = auto()


@zig_enum()
class Suit(ZigEnum):
    clubs = auto()
    spades = auto()
    diamonds = auto()
    hearts = auto()

    Self: Const[Infer] = This()

    def isClubs(self: Self) -> bool:
        return self == Suit.clubs


@zig_enum()
class Foo2(ZigEnum):
    string = auto()
    number = auto()
    none = auto()


@zig_enum()
class Small(ZigEnum):
    one = auto()
    two = auto()
    three = auto()
    four = auto()


@zig()
def enums() -> Error[anyerror, void]:
    std: Const[Infer] = Import("std")
    expect: Const[Infer] = std.testing.expect

    c: Const[Infer] = Type.ok
    Try(expect(c == Type.ok))

    Try(expect(IntFromEnum(Value.zero) == 0))
    Try(expect(IntFromEnum(Value.one) == 1))
    Try(expect(IntFromEnum(Value.two) == 2))

    Try(expect(IntFromEnum(Value2.hundred) == 100))
    Try(expect(IntFromEnum(Value2.thousand) == 1000))
    Try(expect(IntFromEnum(Value2.million) == 1000000))

    Try(expect(IntFromEnum(Value3.a) == 0))
    Try(expect(IntFromEnum(Value3.b) == 8))
    Try(expect(IntFromEnum(Value3.c) == 9))
    Try(expect(IntFromEnum(Value3.d) == 4))
    Try(expect(IntFromEnum(Value3.e) == 5))

    p: Const[Infer] = Suit.spades
    Try(expect(not p.isClubs()))

    q: Const[Foo2] = Foo2.number
    what_is_it: Const[Infer] = _
    match q:
        case Foo2.string:
            break_return("this is a string")
        case Foo2.number:
            break_return("this is a number")
        case Foo2.none:
            break_return("this is a none")
    Try(expect(std.mem.eql(u8, what_is_it, "this is a number")))

    # TODO: Not supported now
    # Try(expect(TypeInfo(Small).enum.tag_type == u2))
    # Try(expect(TypeInfo(Small).enum.fields.len == 4))
    # Try(expect(std.mem.eql(u8, TypeInfo(Small).enum.fields[1].name, "two")))

    Try(expect(std.mem.eql(u8, TagName(Small.three), "three")))


def test_enums():
    enums()


@zig_enum()
class Color(ZigEnum):
    automatic = auto()
    off = auto()
    on = auto()


@zig()
def enum_literals() -> Error[anyerror, void]:
    std: Const[Infer] = Import("std")
    expect: Const[Infer] = std.testing.expect

    color1: Const[Color] = enum(automatic)
    color2: Const[Color] = Color.automatic
    Try(expect(color1 == color2))

    color: Const[Infer] = Color.on
    result: Const[Infer] = _
    match color:
        case enum(automatic):
            break_return(False)
        case enum(on):
            break_return(True)
        case enum(off):
            break_return(False)
    Try(expect(result))


def test_enum_literals():
    enum_literals()


@zig_enum()
class Number(ZigEnum, u8):
    one = auto()
    two = auto()
    three = auto()
    _ = auto()


@zig()
def switch_non_exhaustive() -> Error[anyerror, void]:
    std: Const[Infer] = Import("std")
    expect: Const[Infer] = std.testing.expect

    number: Const[Infer] = Number.one
    result: Const[Infer] = _
    match number:
        case Number.one:
            break_return(True)
        case Number.two | Number.three:
            break_return(False)
        case _:
            break_return(False)
    Try(expect(result))

    is_one: Const[Infer] = _
    match number:
        case Number.one:
            break_return(True)
        case _:
            break_return(False)
    Try(expect(is_one))


def test_switch_non_exhaustive():
    switch_non_exhaustive()


@zig_union()
class Payload(ZigUnion):
    int: i64
    float: f64
    boolean: bool


@zig()
def simple_union() -> Error[anyerror, void]:
    std: Const[Infer] = Import("std")
    expect: Const[Infer] = std.testing.expect

    payload: Var[Payload] = {int: 1234}
    Try(expect(payload.int == 1234))
    payload = {float: 12.34}
    Try(expect(payload.float == 12.34))


def test_simple_union():
    simple_union()


@zig_enum()
class ComplexTypeTag(ZigEnum):
    ok = auto()
    not_ok = auto()


@zig_union(tag='ComplexTypeTag')
class ComplexType(ZigTaggedUnion):
    ok: u8
    not_ok: void


@zig()
def switch_on_tagged_union() -> Error[anyerror, void]:
    std: Const[Infer] = Import("std")
    expect: Const[Infer] = std.testing.expect

    c: Const[ComplexType] = {ok: 42}
    Try(expect(As(ComplexTypeTag, c) == ComplexTypeTag.ok))

    match c:
        case enum(ok) as value:
            Try(expect(value == 42))
        case enum(not_ok):
            unreachable()

    Try(expect(std.meta.Tag(ComplexType) == ComplexTypeTag))


def test_switch_on_tagged_union():
    switch_on_tagged_union()


@zig()
def modify_tagged_union_in_switch() -> Error[anyerror, void]:
    std: Const[Infer] = Import("std")
    expect: Const[Infer] = std.testing.expect

    c: Var[ComplexType] = {ok: 42}
    match c:
        case enum(ok) as _value:  # This is an absolutely stupid hack!!!
            value.deref += 1
        case enum(not_ok):
            unreachable()

    Try(expect(c.ok == 43))


def test_modify_tagged_union_in_switch():
    modify_tagged_union_in_switch()


@zig_union(tag='enum')
class Variant(ZigTaggedUnion):
    int: i32
    boolean: bool
    none: void

    Self: Const[Infer] = This()

    def truthy(self: Self) -> bool:
        ret: Const[Infer] = _
        match self:
            case Variant.int as x_int:
                break_return(x_int != 0)
            case Variant.boolean as x_bool:
                break_return(x_bool)
            case Variant.none:
                break_return(False)
        return ret


@zig()
def union_method() -> Error[anyerror, void]:
    std: Const[Infer] = Import("std")
    expect: Const[Infer] = std.testing.expect

    v1: Var[Variant] = {int: 1}
    v2: Var[Variant] = {boolean: False}
    v3: Var[Variant] = enum(none)

    Try(expect(v1.truthy()))
    Try(expect(not v2.truthy()))
    Try(expect(not v3.truthy()))


def test_union_method():
    union_method()


@zig_union()
class Number2(ZigUnion):
    int: i32
    float: f64


@zig()
def make_number() -> Number2:
    return {float: 12.34}


@zig()
def anonymous_union_literal_syntax() -> Error[anyerror, void]:
    std: Const[Infer] = Import("std")
    expect: Const[Infer] = std.testing.expect

    i: Const[Number2] = {int: 42}
    f: Const[Number2] = {float: 12.34}
    Try(expect(i.int == 42))
    Try(expect(f.float == 12.34))


def test_anonymous_union_literal_syntax():
    anonymous_union_literal_syntax()


@zig()
def access_variable_after_block_scope() -> void:
    with block:
        x: Var[i32] = 1
        _ = ref(x)


def test_access_variable_after_block_scope():
    access_variable_after_block_scope()


@zig()
def labeled_block_expression() -> Error[anyerror, void]:
    std: Const[Infer] = Import("std")
    expect: Const[Infer] = std.testing.expect

    y: Var[i32] = 123
    x: Const[Infer] = _
    with block(blk1):
        y += 1
        break_return(blk1, y)

    Try(expect(x == 124))
    Try(expect(y == 124))


def test_labeled_block_expression():
    labeled_block_expression()


@zig()
def separate_scopes() -> void:
    with block:
        pi: Const[f32] = 3.14
        _ = pi
    with block:
        pi: Var[bool] = True
        _ = ref(pi)


def test_separate_scopes():
    separate_scopes()


@zig()
def switch_simple() -> Error[anyerror, void]:
    std: Const[Infer] = Import("std")
    expect: Const[Infer] = std.testing.expect

    a: Const[u64] = 10
    zz: Const[u64] = 103

    b: Const[Infer] = _
    match a:
        case 1, 2, 3:
            break_return(0)
        case range_incl(5, 100):
            break_return(1)
        case 101:
            c: Const[u64] = 5
            break_return(c * 2 + 1)
        case comptime(zz):
            break_return(zz)
        case _:
            break_return(9)

    Try(expect(b == 1))


def test_switch_simple():
    switch_simple()


@zig()
def switch_inside_function() -> Error[anyerror, void]:
    builtin: Const[Infer] = Import("builtin")

    os_msg: Const[Infer] = _
    match builtin.target.os.tag:
        case enum(linux):
            break_return("we found a linux user")
        case _:
            break_return("not a linux user")

    _ = os_msg

    match builtin.target.os.tag:
        case enum(fuchsia):
            CompileError("fuchsia not supported")
        case _:
            pass


def test_switch_inside_function():
    switch_inside_function()


@zig_struct()
class Point3(ZigStruct):
    x: u8
    y: u8


@zig_union(tag='enum')
class Item(ZigTaggedUnion):
    a: u32
    c: Point3
    d: void
    e: u32


@zig()
def switch_on_tagged_union2() -> Error[anyerror, void]:
    std: Const[Infer] = Import("std")
    expect: Const[Infer] = std.testing.expect

    a: Var[Item] = {c: {x: 1, y: 2}}
    b: Const[Infer] = _
    match a:
        case Item.a as item:  # Putting it in the same prong is not supported
            break_return(item)
        case Item.e as item:
            break_return(item)
        case Item.c as _item:
            item.deref.x += 1
            break_return(6)
        case Item.d:
            break_return(8)

    Try(expect(b == 6))
    Try(expect(a.c.x == 2))


def test_switch_on_tagged_union2():
    switch_on_tagged_union2()


@zig_struct(extern=False)
class Struct1(ZigStruct):
    a: u32
    b: Optional[u32]


@zig(export=False)
def is_field_optional(T: comptime | type, field_index: usize) -> Error[anyerror, bool]:
    fields: Const[Infer] = TypeInfo(T).Struct.fields
    ret: Const[Infer] = _
    match field_index:
        case inline(0, ) as idx:
            break_return(TypeInfo(fields[idx].type) == enum(Optional))
        case _:
            break_return(error.IndexOutOfBounds)
    return ret


@zig()
def using_type_info_with_runtime_values() -> Error[anyerror, void]:
    std: Const[Infer] = Import("std")
    expect: Const[Infer] = std.testing.expect
    expect_error: Const[Infer] = std.testing.expectError

    index: Var[usize] = 0
    Try(expect(not Try(is_field_optional(Struct1, index))))
    index += 1
    Try(expect(Try(is_field_optional(Struct1, index))))
    index += 1
    Try(expect_error(error.IndexOutOfBounds, is_field_optional(Struct1, index)))


def test_using_type_info_with_runtime_values():
    using_type_info_with_runtime_values()


@zig_struct()
class SliceTypeA(ZigStruct):
    len: usize
    ptr: Array[u32]


@zig_struct()
class SliceTypeB(ZigStruct):
    ptr: Array[SliceTypeA]
    len: usize


@zig_union(tag='enum')
class AnySlice(ZigTaggedUnion):
    a: SliceTypeA
    b: SliceTypeB
    c: Slice[Const[u8]]
    d: Slice['AnySlice']  # To avoid circular reference error


@ zig(export=False)
def with_for(any: AnySlice) -> usize:
    Tag: Const[Infer] = TypeInfo(AnySlice).Union.tag_type.unwrap
    with inline:
        for field in TypeInfo(Tag).Enum.fields:
            if field.value == IntFromEnum(any):
                return Field(any, field.name).len
    unreachable()


@ zig(export=False)
def with_switch(any: AnySlice) -> usize:
    ret: Const[Infer] = _
    match any:
        case inline(_) as slice:
            break_return(slice.len)
    return ret


@ zig()
def inline_for_and_else() -> Error[anyerror, void]:
    std: Const[Infer] = Import("std")
    expect: Const[Infer] = std.testing.expect

    any: Const[AnySlice] = {c: "hello"}
    Try(expect(with_for(any) == 5))
    Try(expect(with_switch(any) == 5))


def test_inline_for_and_else():
    inline_for_and_else()


@zig()
def while_basic() -> Error[anyerror, void]:
    std: Const[Infer] = Import("std")
    expect: Const[Infer] = std.testing.expect

    i: Var[usize] = 0
    while i < 10:
        i += 1
    Try(expect(i == 10))


@zig()
def while_break() -> Error[anyerror, void]:
    std: Const[Infer] = Import("std")
    expect: Const[Infer] = std.testing.expect

    i: Var[usize] = 0
    while True:
        if i == 10:
            break
        i += 1
    Try(expect(i == 10))


@zig()
def while_continue() -> Error[anyerror, void]:
    std: Const[Infer] = Import("std")
    expect: Const[Infer] = std.testing.expect

    i: Var[usize] = 0
    while True:
        i += 1
        if i < 10:
            continue
        break
    Try(expect(i == 10))


@zig()
def while_else() -> Error[anyerror, void]:
    std: Const[Infer] = Import("std")
    expect: Const[Infer] = std.testing.expect

    Try(expect(rangeHasNumber(0, 10, 5)))
    Try(expect(not rangeHasNumber(0, 10, 15)))


@zig()
def rangeHasNumber(begin: usize, end: usize, number: usize) -> bool:
    i: Var[usize] = begin
    while i < end:
        if i == number:
            return True
        i += 1
    else:
        return False


def test_while():
    while_basic()
    while_break()
    while_continue()
    while_else()


# Not strictly needed, but sure why not
@zig()
def while_null_capture() -> Error[anyerror, void]:
    std: Const[Infer] = Import("std")
    expect: Const[Infer] = std.testing.expect

    sum1: Var[u32] = 0
    EventuallyNullSequence.numbers_left = 3
    while capture(EventuallyNullSequence.eventuallyNullSequence(), value):
        sum1 += value
    Try(expect(sum1 == 3))

    sum2: Var[u32] = 0
    EventuallyNullSequence.numbers_left = 3
    while capture(EventuallyNullSequence.eventuallyNullSequence(), value):
        sum2 += value
    else:
        Try(expect(sum2 == 3))

    i: Var[u32] = 0
    sum3: Var[u32] = 0
    EventuallyNullSequence.numbers_left = 3
    while capture(EventuallyNullSequence.eventuallyNullSequence(), value):
        sum3 += value
        i += 1

    Try(expect(i == 3))


@zig_struct()
class EventuallyNullSequence(ZigStruct):
    numbers_left: Var[u32] = undefined

    def eventuallyNullSequence() -> Optional[u32]:
        if numbers_left == 0:
            return None
        numbers_left -= 1
        return numbers_left


def test_while_null_capture():
    while_null_capture()


@zig()
def while_error_union_capture() -> Error[anyerror, void]:
    std: Const[Infer] = Import("std")
    expect: Const[Infer] = std.testing.expect

    sum1: Var[u32] = 0
    EventuallyErrorSequence.numbers_left = 3
    while capture_err(EventuallyErrorSequence.eventuallyErrorSequence(), value):
        sum1 += value
    else:  # Default error capture in else is 'err'
        Try(expect(err == error.ReachedZero))


@zig_struct()
class EventuallyErrorSequence(ZigStruct):
    numbers_left: Var[u32] = undefined

    def eventuallyErrorSequence() -> Error[anyerror, u32]:
        if numbers_left == 0:
            return error.ReachedZero
        numbers_left -= 1
        return numbers_left


def test_while_error_union_capture():
    while_error_union_capture()


@zig()
def inline_while_loop() -> Error[anyerror, void]:
    std: Const[Infer] = Import("std")
    expect: Const[Infer] = std.testing.expect

    i: comptime | Var[usize] = 0
    sum: Var[usize] = 0
    with inline:
        while i < 3:
            T: Const[Infer] = _
            match i:
                case 0:
                    break_return(f32)
                case 1:
                    break_return(i8)
                case 2:
                    break_return(bool)
                case _:
                    # unreachable() # TODO: Bug => unreachable() cause the unused blk label error
                    break_return(i4)  # Dummy value
            sum += typeNameLength(T)
            i += 1

    Try(expect(sum == 9))


@zig(export=False)
def typeNameLength(T: comptime | type) -> usize:
    return TypeName(T).len


def test_inline_while_loop():
    inline_while_loop()


@zig()
def for_basics() -> Error[anyerror, void]:
    std: Const[Infer] = Import("std")
    expect: Const[Infer] = std.testing.expect

    items: Const[Infer] = list([4, 5, 3, 4, 0], u32)
    sum: Var[u32] = 0

    for value in items:
        if value == 0:
            continue
        sum += value
    Try(expect(sum == 16))

    for value in items[0:1]:
        sum += value
    Try(expect(sum == 20))

    sum2: Var[i32] = 0
    for (_, i) in items, range(0, None):
        Try(expect(TypeOf(i) == usize))
        sum2 += As(i32, IntCast(i))

    Try(expect(sum2 == 10))

    sum3: Var[usize] = 0
    for i in range(0, 5):
        sum3 += i
    Try(expect(sum3 == 10))


@zig()
def for_multi_object() -> Error[anyerror, void]:
    std: Const[Infer] = Import("std")
    expect: Const[Infer] = std.testing.expect

    items: Const[Infer] = list([1, 2, 3], usize)
    items2: Const[Infer] = list([4, 5, 6], usize)
    count: Var[usize] = 0

    for i, j in items, items2:
        count += i + j

    Try(expect(count == 21))


@zig()
def for_reference() -> Error[anyerror, void]:
    std: Const[Infer] = Import("std")
    expect: Const[Infer] = std.testing.expect

    items: Var[Infer] = list([3, 4, 2], i32)

    for (*value,) in ref(items):  # Pointer only works when passed as a tuple
        value.deref += 1

    Try(expect(items[0] == 4))
    Try(expect(items[1] == 5))
    Try(expect(items[2] == 3))


@zig()
def for_else() -> Error[anyerror, void]:
    std: Const[Infer] = Import("std")
    expect: Const[Infer] = std.testing.expect

    items: Const[Infer] = list([3, 4, None, 5], type(Optional[i32]))

    sum: Var[i32] = 0
    for value in items:
        if value != None:
            sum += value.unwrap
    else:
        Try(expect(sum == 12))


def test_for():
    for_basics()
    for_multi_object()
    for_reference()
    for_else()


@zig()
def inline_for_loop() -> Error[anyerror, void]:
    std: Const[Infer] = Import("std")
    expect: Const[Infer] = std.testing.expect

    items: Const[Infer] = list([2, 4, 6], i32)
    sum: Var[usize] = 0

    with inline:
        for i in items:
            T: Const[Infer] = _
            match i:
                case 2:
                    break_return(f32)
                case 4:
                    break_return(i8)
                case 6:
                    break_return(bool)
                case _:
                    # unreachable() # TODO: Bug => unreachable() cause the unused blk label error
                    break_return(i4)
            sum += typeNameLength(T)

    Try(expect(sum == 9))


def test_inline_for_loop():
    inline_for_loop()


@zig()
def if_expression() -> Error[anyerror, void]:
    std: Const[Infer] = Import("std")
    expect: Const[Infer] = std.testing.expect

    a: Const[u32] = 5
    b: Const[u32] = 4
    result: Const[Infer] = 47 if a != b else 3089
    Try(expect(result == 47))


@zig()
def if_boolean() -> Error[anyerror, void]:
    std: Const[Infer] = Import("std")
    expect: Const[Infer] = std.testing.expect

    a: Const[u32] = 5
    b: Const[u32] = 4
    if a != b:
        Try(expect(True))
    elif a == 9:
        unreachable()
    else:
        unreachable()


@zig()
def if_error_union() -> Error[anyerror, void]:
    std: Const[Infer] = Import("std")
    expect: Const[Infer] = std.testing.expect

    a: Const[Error[anyerror, u32]] = 0
    if capture_err(a, value, err):
        Try(expect(value == 0))
    else:
        _ = err
        unreachable()

    b: Const[Error[anyerror, u32]] = error.BadValue
    if capture_err(b, value, err):
        _ = value
        unreachable()
    else:
        Try(expect(err == error.BadValue))

    if capture_err(a, value, err):
        Try(expect(value == 0))
    else:
        _ = err

    if capture_err(b, _, err):
        pass
    else:
        Try(expect(err == error.BadValue))

    c: Var[Error[anyerror, u32]] = 3
    if capture_err(c, *value, _):
        value.deref = 9
    else:
        unreachable()

    if capture_err(c, value, _):
        Try(expect(value == 9))
    else:
        unreachable()


def test_if():
    if_expression()
    if_boolean()
    if_error_union()


@zig()
def if_optional() -> Error[anyerror, void]:
    std: Const[Infer] = Import("std")
    expect: Const[Infer] = std.testing.expect

    a: Const[Optional[u32]] = 0
    if capture(a, value):
        Try(expect(value == 0))
    else:
        unreachable()

    b: Const[Optional[u32]] = None
    if capture(b, _):
        unreachable()
    else:
        Try(expect(True))

    if capture(a, value):
        Try(expect(value == 0))

    if b == None:
        Try(expect(True))

    c: Var[Optional[u32]] = 3
    if capture(c, *value):
        value.deref = 2

    if capture(c, value):
        Try(expect(value == 2))
    else:
        unreachable()


@zig()
def if_error_union_with_optional() -> Error[anyerror, void]:
    std: Const[Infer] = Import("std")
    expect: Const[Infer] = std.testing.expect

    a: Const[Error[anyerror, Optional[u32]]] = 0
    if capture_err(a, optional_value, err):
        Try(expect(optional_value == 0))
    else:
        _ = err
        unreachable()

    b: Const[Error[anyerror, Optional[u32]]] = None
    if capture_err(b, optional_value, _):
        Try(expect(optional_value == None))
    else:
        unreachable()

    c: Const[Error[anyerror, Optional[u32]]] = error.BadValue
    if capture_err(c, optional_value, err):
        _ = optional_value
        unreachable()
    else:
        Try(expect(err == error.BadValue))

    d: Var[Error[anyerror, Optional[u32]]] = 3
    if capture_err(d, *optional_value, _):
        if capture(optional_value.deref, *value):
            value.deref = 9
    else:
        unreachable()

    if capture_err(d, optional_value, _):
        Try(expect(optional_value.unwrap == 9))
    else:
        unreachable()


def test_if_optional():
    if_optional()
    if_error_union_with_optional()


@zig()
def defer_example() -> Error[anyerror, usize]:
    std: Const[Infer] = Import("std")
    expect: Const[Infer] = std.testing.expect

    a: Var[usize] = 1

    with block:
        with defer:
            a = 2
        a = 1

    Try(expect(a == 2))

    a = 5
    return a


def test_defer_example():
    defer_example()


@zig()
def defer_unwinding() -> Error[anyerror, void]:
    std: Const[Infer] = Import("std")
    print: Const[Infer] = std.debug.print

    with defer:
        print("1 ", ())
    with defer:
        print("2 ", ())
    if False:
        with defer:
            print("3 ", ())


def test_defer_unwinding(capfd):
    defer_unwinding()
    out, err = capfd.readouterr()
    assert err == "2 1 "


@zig(export=False)
def add(a: i8, b: i8) -> i8:
    if a == 0:
        return b
    return a + b


@zig(export=True)
def sub(a: i8, b: i8) -> i8:
    return a - b


@zig(export=False)
def abort() -> noreturn:
    BranchHint(enum(cold))
    while True:
        pass


# TODO: Not supported now inline
@zig()
def shiftLeftOne(a: u32) -> u32:
    return a << 1


@zig()
def sub2(a: i8, b: i8) -> i8:
    return a - b


@zig_struct()
class Call2Op(ZigStruct):
    fnCall: Const[Infer] = type(Ptr[Const[Callable[[i8, i8], i8]]])


@ zig(export=False)
def doOp(fnCall: Call2Op.fnCall, op1: i8, op2: i8) -> i8:
    return fnCall(op1, op2)


@ zig()
def function() -> Error[anyerror, void]:
    std: Const[Infer] = Import("std")
    expect: Const[Infer] = std.testing.expect
    # Force the function to be compiled, (workaround for function ptrs)
    _ = add(0, 1)
    _ = sub2(0, 1)

    Try(expect(doOp(add, 5, 6) == 11))
    Try(expect(doOp(sub2, 5, 6) == -1))


def test_function():
    function()


@zig()
def foo2(point: Point) -> i32:
    return point.x + point.y


@zig()
def pass_struct_to_function() -> Error[anyerror, void]:
    std: Const[Infer] = Import("std")
    expect: Const[Infer] = std.testing.expect

    Try(expect(foo2({x: 1, y: 2}) == 3))


def test_struct_to_function():
    pass_struct_to_function()

# @zig(export=False)
# def add_forty_two(x: anytype) -> TypeOf(x): #NOTE: This will throw 'x' not defined error
#     return x + 42
# NOTE: We can fix it by making x a TypeVar for example
# x = TypeVar('x')
# T is a default typevar you can use


@zig(export=False)
def add_forty_two(T: anytype) -> TypeOf(T):
    return T + 42


@zig()
def fn_type_inference() -> Error[anyerror, void]:
    std: Const[Infer] = Import("std")
    expect: Const[Infer] = std.testing.expect

    Try(expect(add_forty_two(1) == 43))
    Try(expect(TypeOf(add_forty_two(1)) == comptime_int))
    y: Const[i64] = 2
    Try(expect(add_forty_two(y) == 44))
    Try(expect(TypeOf(add_forty_two(y)) == i64))


def test_fn_type_inference():
    fn_type_inference()


@zig()
def fn_reflection() -> Error[anyerror, void]:
    std: Const[Infer] = Import("std")
    math: Const[Infer] = std.math
    testing: Const[Infer] = std.testing

    Try(testing.expect(TypeInfo(TypeOf(testing.expect)
                                ).Fn.params[0].type.unwrap == bool))
    Try(testing.expect(TypeInfo(TypeOf(testing.tmpDir)
                                ).Fn.return_type.unwrap == testing.TmpDir))

    Try(testing.expect(TypeInfo(TypeOf(math.Log2Int)).Fn.is_generic))


def test_fn_reflection():
    fn_reflection()


@zig_error()
class FileOpenError(ZigError):
    # NOTE: We have to use auto() to satisfy 🐍 (    # Snake emoji ->     AccessDenied = auto()
    FileNotFound = auto()
    AccessDenied = auto()
    OutOfMemory = auto()


@zig_error()
class AllocationError(ZigError):
    OutOfMemory = auto()


@zig(export=False)
def foo3(err: AllocationError) -> FileOpenError:
    return err


@zig()
def coerce_subset_to_superset() -> Error[anyerror, void]:
    std: Const[Infer] = Import("std")
    testing: Const[Infer] = std.testing

    err: Const[Infer] = foo3(AllocationError.OutOfMemory)
    Try(testing.expect(err == FileOpenError.OutOfMemory))


@zig(export=False)
def parse_u64(buf: Slice[Const[u8]], radix: u8) -> Error[anyerror, u64]:
    x: Var[u64] = 0

    for c in buf:
        digit: Const[u8] = char_to_digit(c)

        if digit >= radix:
            return error.InvalidChar

        ov: Var[Infer] = MulWithOverflow(x, radix)
        if ov[1] != 0:
            return error.OverFlow

        ov = AddWithOverflow(ov[0], digit)
        if ov[1] != 0:
            return error.OverFlow
        x = ov[0]

    return x


@zig()
def char_to_digit(c: u8) -> u8:
    std: Const[Infer] = Import("std")
    math: Const[Infer] = std.math

    ret: Const[Infer] = _
    match c:
        case range_incl(chr('0'), chr('9')):
            break_return(c - chr('0'))
        case range_incl(chr('A'), chr('Z')):
            break_return(c - chr('A') + 10)
        case range_incl(chr('a'), chr('z')):
            break_return(c - chr('a') + 10)
        case _:
            break_return(math.maxInt(u8))
    return ret


@zig()
def parse_u64_test() -> Error[anyerror, void]:
    std: Const[Infer] = Import("std")
    testing: Const[Infer] = std.testing

    result: Const[Infer] = Try(parse_u64("1234", 10))
    Try(testing.expect(result == 1234))


def test_error_union():
    parse_u64_test()
    coerce_subset_to_superset()


@zig(export=False)
def do_a_thing(str: Slice[Const[u8]]) -> void:
    number: Const[Infer] = parse_u64(str, 10) @ catch(13)
    _ = number


@zig(export=False)
def do_a_thing2(str: Slice[Const[u8]]) -> void:
    number: Const[Infer] = parse_u64(str, 10) @ catch(_)
    with block(blk):
        break_return(blk, 13)
    _ = number


@zig()
def catch_() -> Error[anyerror, void]:
    do_a_thing("1234")
    do_a_thing2("1234")


def test_catch():
    catch_()


@zig(export=False)
def captureError(captured: Ptr[Optional[anyerror]]) -> Error[anyerror, void]:

    with errdefer(err):
        captured.deref = err
    return error.GeneralFailure


@zig()
def errdefer_capture() -> Error[anyerror, void]:
    std: Const[Infer] = Import("std")
    testing: Const[Infer] = std.testing

    captured: Var[Optional[anyerror]] = None

    if capture_err(captureError(ref(captured)), _, err):
        unreachable()
    else:
        Try(testing.expectEqual(error.GeneralFailure, captured.unwrap))
        Try(testing.expectEqual(error.GeneralFailure, err))


def test_errdefer_capture():
    errdefer_capture()


@zig()
def error_union() -> Error[anyerror, void]:
    std: Const[Infer] = Import("std")
    testing: Const[Infer] = std.testing

    foo: Var[Error[anyerror, i32]] = undefined

    foo = 1234
    foo = error.SomeError

    Try(testing.expectEqual(TypeInfo(TypeOf(foo)).ErrorUnion.payload, i32))
    Try(testing.expectEqual(TypeInfo(TypeOf(foo)).ErrorUnion.error_set, anyerror))


def test_error_union2():
    error_union()


@zig_error()
class A(ZigError):
    NotDir = auto()
    PathNotFound = auto()


@zig_error()
class B(ZigError):
    OutOfMemory = auto()
    PathNotFound = auto()


@zig_struct()
class MergeErrorSets(ZigStruct):
    C: Const[Infer] = Union[A, B]

    def foo() -> Error[C, void]:
        return error.NotDir


@zig()
def merge_error_sets() -> Error[anyerror, void]:

    if capture_err(MergeErrorSets.foo(), _, err):
        unreachable()
    else:
        match err:
            case error.OutOfMemory:
                Panic("unexpected")
            case error.PathNotFound:
                Panic("unexpected")
            case error.NotDir:
                pass


def test_merge_error_sets():
    merge_error_sets()


@zig_error()
class ErrorSet(ZigError):
    Overflow = auto()


@zig(export=False)
def add_inferred(T: comptime | type, a: T, b: T) -> Error[anyerror, T]:
    ov: Const[Infer] = AddWithOverflow(a, b)
    if ov[1] != 0:
        return error.Overflow
    return ov[0]


@zig(export=False)
def add_explicit(T: comptime | type, a: T, b: T) -> Error[ErrorSet, T]:
    ov: Const[Infer] = AddWithOverflow(a, b)
    if ov[1] != 0:
        return error.Overflow
    return ov[0]


@zig()
def inferred_error_set() -> Error[anyerror, void]:
    if capture_err(add_explicit(u8, 255, 1), _, err):
        unreachable()
    else:
        match err:
            case error.Overflow:
                pass


def test_inferred_error_set():
    inferred_error_set()


@zig()
def optional_type() -> Error[anyerror, void]:
    std: Const[Infer] = Import("std")
    testing: Const[Infer] = std.testing

    foo: Var[Optional[i32]] = None

    foo = 1234

    Try(testing.expect(TypeInfo(TypeOf(foo)).Optional.child == i32))


def test_optional_type():
    optional_type()


@zig()
def optional_pointer() -> Error[anyerror, void]:
    std: Const[Infer] = Import("std")
    testing: Const[Infer] = std.testing

    ptr: Var[Optional[Ptr[i32]]] = None

    x: Var[i32] = 1
    ptr = ref(x)

    Try(testing.expect(ptr.unwrap.deref == 1))
    Try(testing.expect(SizeOf(type(Optional[Ptr[i32]])) == SizeOf(*i32)))


def test_optional_pointer():
    optional_pointer()


@zig()
def type_coercion_variable_declaration() -> Error[anyerror, void]:
    a: Const[u8] = 1
    b: Const[u16] = a

    _ = b


@zig()
def type_coercion_function_call() -> Error[anyerror, void]:
    a: Const[u8] = 1
    foo4(a)


@zig()
def foo4(b: u16) -> void:
    _ = b


@zig()
def type_coercion_builtin() -> Error[anyerror, void]:
    a: Const[u8] = 1
    b: Const[u16] = As(u16, a)

    _ = b


def test_type_coercion():
    type_coercion_variable_declaration()
    type_coercion_function_call()
    type_coercion_builtin()


@zig(export=False)
def foo5(_: Ptr[Const[i32]]) -> void:
    pass


@zig()
def type_coercion_const_qualification() -> Error[anyerror, void]:
    a: Var[i32] = 1
    b: Const[Ptr[Const[i32]]] = ref(a)
    foo5(b)


def test_type_coercion_const_qualification():
    type_coercion_const_qualification()


@zig()
def cast_to_array() -> Error[anyerror, void]:
    std: Const[Infer] = Import("std")
    testing: Const[Infer] = std.testing
    mem: Const[Infer] = std.mem

    window_name: Const[Infer] = list(
        ["window name"], type(Array['*', 0, Const[u8]]))
    x: Const[Slice[Const[Optional[Array['*', 0, Const[u8]]]]]
             ] = ref(window_name)
    Try(testing.expect(mem.eql(u8, mem.span(x[0].unwrap), "window name")))


def test_cast_to_array():
    cast_to_array()


@zig()
def integer_widening() -> Error[anyerror, void]:
    std: Const[Infer] = Import("std")
    testing: Const[Infer] = std.testing

    a: Const[u8] = 250
    b: Const[u16] = a
    c: Const[u32] = b
    d: Const[u64] = c
    e: Const[u64] = d
    f: Const[u128] = e

    Try(testing.expect(f == a))


@zig()
def implicit_unsigned_integer_to_signed_integer() -> Error[anyerror, void]:
    std: Const[Infer] = Import("std")
    testing: Const[Infer] = std.testing

    a: Const[u8] = 250
    b: Const[i16] = a

    Try(testing.expect(b == 250))


@zig()
def float_widening() -> Error[anyerror, void]:
    std: Const[Infer] = Import("std")
    testing: Const[Infer] = std.testing

    a: Const[f16] = 12.34
    b: Const[f32] = a
    c: Const[f64] = b
    d: Const[f128] = c

    Try(testing.expect(d == a))


def test_widening():
    integer_widening()
    implicit_unsigned_integer_to_signed_integer()
    float_widening()


@zig()
def cast_to_slice() -> Error[anyerror, void]:
    std: Const[Infer] = Import("std")
    testing: Const[Infer] = std.testing

    x1: Const[Slice[Const[u8]]] = "hello"
    x2: Const[Slice[Const[u8]]] = ref(list([104, 101, 108, 108, 111], u8))
    Try @ testing.expect(std.mem.eql(u8, x1, x2))

    y: Const[Slice[Const[f32]]] = ref(list([1.2, 3.4], f32))
    Try @ testing.expect(y[0] == 1.2)


@zig()
def cast_to_error_union_slice() -> Error[anyerror, void]:
    std: Const[Infer] = Import("std")
    testing: Const[Infer] = std.testing

    x1: Const[Error[anyerror, Slice[Const[u8]]]] = "hello"
    x2: Const[Error[anyerror, Slice[Const[u8]]]] = ref(
        list([104, 101, 108, 108, 111], u8))
    Try @ testing.expect(std.mem.eql(u8, Try @ x1, Try @ x2))

    y: Const[Error[anyerror, Slice[Const[f32]]]] = ref(list([1.2, 3.4], f32))
    Try @ testing.expect((Try @ y)[0] == 1.2)


@zig()
def cast_to_optional_slice() -> Error[anyerror, void]:
    std: Const[Infer] = Import("std")
    testing: Const[Infer] = std.testing

    x1: Const[Optional[Slice[Const[u8]]]] = "hello"
    x2: Const[Optional[Slice[Const[u8]]]] = ref(
        list([104, 101, 108, 108, 111], u8))
    Try @ testing.expect(std.mem.eql(u8, x1.unwrap, x2.unwrap))

    y: Const[Optional[Slice[Const[f32]]]] = ref(list([1.2, 3.4], f32))
    Try @ testing.expect(y.unwrap[0] == 1.2)


@zig()
def cast_ptr_to_slice() -> Error[anyerror, void]:
    std: Const[Infer] = Import("std")
    testing: Const[Infer] = std.testing

    buf: Var[Array[5, u8]] = "hello".deref
    x: Const[Slice[Const[u8]]] = ref(buf)
    Try @ testing.expect(std.mem.eql(u8, x, "hello"))

    buf2: Const[Array[2, f32]] = list([1.2, 3.4], f32)
    x2: Const[Slice[Const[f32]]] = ref(buf2)
    Try @ testing.expect(std.mem.eql(f32, x2, ref(list([1.2, 3.4], f32))))


@zig()
def cast_single_item_ptr_to_many_item_ptr() -> Error[anyerror, void]:
    std: Const[Infer] = Import("std")
    testing: Const[Infer] = std.testing

    buf: Var[Array[5, u8]] = "hello".deref
    x: Const[Array[u8]] = ref(buf)
    Try @ testing.expect(x[4] == chr('o'))

    buf2: Var[Array[5, u8]] = "hello".deref
    x3: Const[Optional[Array[u8]]] = ref(buf2)
    Try @ testing.expect(x3.unwrap[4] == chr('o'))

    x2: Var[i32] = 1234
    y: Const[Ptr[Array[1, i32]]] = ref(x2)
    z: Const[Array[i32]] = y
    Try @ testing.expect(z[0] == 1234)


def test_type_coercion_slices_arrs_ptrs():
    cast_to_slice()
    cast_to_error_union_slice()
    cast_to_optional_slice()
    cast_ptr_to_slice()
    cast_single_item_ptr_to_many_item_ptr()


@zig()
def coerce_to_optionals() -> Error[anyerror, void]:
    std: Const[Infer] = Import("std")
    testing: Const[Infer] = std.testing

    x: Const[Optional[i32]] = 1234
    y: Const[Optional[i32]] = None

    Try(testing.expect(x.unwrap == 1234))
    Try(testing.expect(y == None))


@zig()
def coerce_to_optionals_wrapped_in_error_union() -> Error[anyerror, void]:
    std: Const[Infer] = Import("std")
    testing: Const[Infer] = std.testing

    x: Const[Error[anyerror, Optional[i32]]] = 1234
    y: Const[Error[anyerror, Optional[i32]]] = None

    Try(testing.expect((Try @ x).unwrap == 1234))
    Try(testing.expect(Try @ y == None))


@zig()
def coercion_to_error_unions() -> Error[anyerror, void]:
    std: Const[Infer] = Import("std")
    testing: Const[Infer] = std.testing

    x: Const[Error[anyerror, i32]] = 1234
    y: Const[Error[anyerror, i32]] = error.Failure

    Try(testing.expect(Try @ x == 1234))
    Try(testing.expectError(error.Failure, y))


def test_coercion_to_optionals_error_unions():
    coerce_to_optionals()
    coerce_to_optionals_wrapped_in_error_union()
    coercion_to_error_unions()


@zig()
def coercion_to_smaller_integer_type() -> Error[anyerror, void]:
    std: Const[Infer] = Import("std")
    testing: Const[Infer] = std.testing

    x: Const[u64] = 255
    y: Const[u8] = x

    Try(testing.expect(y == 255))


def test_coercion_to_smaller_integer_type():
    coercion_to_smaller_integer_type()


@zig_enum()
class E(ZigEnum):
    one = auto()
    two = auto()
    three = auto()


@zig_union(tag='E')
class U(ZigTaggedUnion):
    one: i32
    two: f32
    three: void


@zig_union(tag='enum')
class U2(ZigTaggedUnion):
    a: void
    b: f32

    def tag(self: This()) -> usize:
        match self:
            case enum(a):
                return 1
            case enum(b):
                return 2


@zig()
def coercion_between_unions_and_enums() -> Error[anyerror, void]:
    std: Const[Infer] = Import("std")
    testing: Const[Infer] = std.testing

    u: Const[U] = {two: 12.34}
    e: Const[E] = u
    Try(testing.expect(e == E.two))

    three_: Const[E] = E.three
    u_2: Const[U] = three_
    Try(testing.expect(u_2 == E.three))

    u_3: Const[U] = enum(three)
    Try(testing.expect(u_3 == E.three))

    u_4: Const[U2] = enum(a)
    Try(testing.expect(u_4.tag() == 1))


def test_coercion_between_unions_and_enums():
    coercion_between_unions_and_enums()


# TODO: Fix this
#
# @zig()
# def coercion_from_homogeneous_tuple_to_array() -> Error[anyerror, void]:
#     std: Const[Infer] = Import("std")
#     testing: Const[Infer] = std.testing
#
#     Tuple: Const[Infer] = struct(u8, u8)
#     tuple: Const[Tuple] = [5, 6]
#     array: Const[Array[2, u8]] = tuple
#
#     _ = array
#
#
# def test_coercion_from_homogeneous_tuple_to_array():
#     coercion_from_homogeneous_tuple_to_array()
