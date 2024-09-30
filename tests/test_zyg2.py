from enum import Enum, auto
from zyg.zyg import *


@zig()
def peer_resolve_int_widening() -> Error[anyerror, void]:
    std: Const[Infer] = Import("std")
    testing: Const[Infer] = std.testing

    a: Const[i8] = 12
    b: Const[i16] = 34
    c: Const[Infer] = a + b

    Try(testing.expect(c == 46))
    Try(testing.expect(TypeOf(c) == i16))


@zig(export=False)
def boolToStr(b: bool) -> Slice[Const[u8]]:
    return "true" if b else "false"


@zig()
def peer_resolve_arrays_of_different_size_to_const_slice() -> Error[anyerror, void]:
    std: Const[Infer] = Import("std")
    testing: Const[Infer] = std.testing

    Try(testing.expect(std.mem.eql(u8, boolToStr(True), "true")))
    Try(testing.expect(std.mem.eql(u8, boolToStr(False), "false")))
    with comptime:
        Try @ testing.expect(std.mem.eql(u8, boolToStr(True), "true"))
        Try @ testing.expect(std.mem.eql(u8, boolToStr(False), "false"))


@zig(export=False)
def peerResolveArrayConstSlice(b: bool) -> Error[anyerror, void]:
    value1: Const[Infer] = "aoeu" if b else "zz"
    value2: Const[Infer] = "zz" if b else "aoeu"

    std: Const[Infer] = Import("std")
    testing: Const[Infer] = std.testing

    Try(testing.expect(std.mem.eql(u8, value1, "aoeu")))
    Try(testing.expect(std.mem.eql(u8, value2, "zz")))


@zig()
def peer_resolve_array_and_const_slice() -> Error[anyerror, void]:
    Try(peerResolveArrayConstSlice(True))
    with comptime:
        Try(peerResolveArrayConstSlice(True))


@zig(export=False)
def peerTypeTAndOptionalT(c: bool, b: bool) -> Optional[usize]:
    if c:
        return None if b else As(usize, 0)
    return As(usize, 3)


@zig()
def peer_type_resolution_T_and_optional_T() -> Error[anyerror, void]:
    std: Const[Infer] = Import("std")
    testing: Const[Infer] = std.testing

    Try(testing.expect(peerTypeTAndOptionalT(True, False).unwrap == 0))
    Try(testing.expect(peerTypeTAndOptionalT(False, False).unwrap == 3))

    with comptime:
        Try @ testing.expect(peerTypeTAndOptionalT(True, False).unwrap == 0)
        Try @ testing.expect(peerTypeTAndOptionalT(False, False).unwrap == 3)


@zig(export=False)
def peerTypeEmptyArrayAndSlice(a: bool, slice: Slice[Const[u8]]) -> Slice[Const[u8]]:
    if a:
        return ref(list([], u8))
    return slice[0:1]


@zig()
def peer_type_resolution_empty_array_and_slice() -> Error[anyerror, void]:
    std: Const[Infer] = Import("std")
    testing: Const[Infer] = std.testing

    Try(testing.expect(peerTypeEmptyArrayAndSlice(True, "hi").len == 0))
    Try(testing.expect(peerTypeEmptyArrayAndSlice(False, "hi").len == 1))

    with comptime:
        Try @ testing.expect(peerTypeEmptyArrayAndSlice(True, "hi").len == 0)
        Try @ testing.expect(peerTypeEmptyArrayAndSlice(False, "hi").len == 1)


@zig(export=False)
def peerTypeEmptyArrayAndSliceAndError(a: bool, slice: Slice[u8]) -> Error[anyerror, Slice[u8]]:
    if a:
        return ref(list([], u8))
    return slice[0:1]


@zig()
def peer_type_resolution_T_and_optional_T() -> Error[anyerror, void]:
    std: Const[Infer] = Import("std")
    expect: Const[Infer] = std.testing.expect
    with block:
        data: Var[Infer] = "hi".deref
        slice: Const[Infer] = data[0:]
        Try @ expect((Try @ peerTypeEmptyArrayAndSliceAndError(True, slice)).len == 0)
        Try @ expect((Try @ peerTypeEmptyArrayAndSliceAndError(False, slice)).len == 1)

    with comptime:
        data: Var[Infer] = "hi".deref
        slice: Const[Infer] = data[0:]
        Try @ expect((Try @ peerTypeEmptyArrayAndSliceAndError(True, slice)).len == 0)
        Try @ expect((Try @ peerTypeEmptyArrayAndSliceAndError(False, slice)).len == 1)


@zig()
def peer_type_resolution_pointer_and_optional_pointer() -> Error[anyerror, void]:
    std: Const[Infer] = Import("std")
    testing: Const[Infer] = std.testing

    a: Const[Ptr[Const[usize]]] = PtrFromInt(0x123456780)
    b: Const[Optional[Ptr[usize]]] = PtrFromInt(0x123456780)

    Try(testing.expect(a == b))
    Try(testing.expect(b == a))


@zig_error()
class Err(ZigError):
    A = auto()
    B = auto()
    C = auto()


def test_peer_resolve_array():
    peer_resolve_int_widening()
    peer_resolve_arrays_of_different_size_to_const_slice()
    peer_resolve_array_and_const_slice()
    peer_type_resolution_T_and_optional_T()
    peer_type_resolution_empty_array_and_slice()
    peer_type_resolution_pointer_and_optional_pointer()


@zig()
def turn_hashmap_into_set_with_void() -> Error[anyerror, void]:
    std: Const[Infer] = Import("std")
    expect: Const[Infer] = std.testing.expect

    map: Var[Infer] = std.AutoHashMap(i32, void).init(std.heap.page_allocator)
    with defer:
        map.deinit()

    Try(map.put(1, []))
    Try(map.put(2, []))

    Try(expect(map.contains(2)))
    Try(expect(not map.contains(3)))

    _ = map.remove(2)
    Try(expect(not map.contains(2)))


def test_turn_hashmap_into_set_with_void():
    turn_hashmap_into_set_with_void()


@zig(export=False)
def max(T: comptime | type, a: T, b: T) -> T:
    if T == bool:
        return a or b
    elif a > b:
        return a
    else:
        return b


@zig()
def try_to_compare_bools() -> Error[anyerror, void]:
    std: Const[Infer] = Import("std")
    expect: Const[Infer] = std.testing.expect

    Try @ expect(max(bool, False, True) == True)


def test_try_to_compare_bools():
    try_to_compare_bools()


@zig()
def one(value: i32) -> i32:
    return value + 1


@zig()
def two(value: i32) -> i32:
    return value + 2


@zig()
def three(value: i32) -> i32:
    return value + 3


@zig_struct(extern=False)
class CmdFn(ZigStruct):
    name: Slice[Const[u8]]
    func: Callable[[i32], i32]


@zig(export=False)
def performFn(prefix_char: comptime | u8, start_value: i32) -> i32:
    _ = one(0)
    _ = two(0)
    _ = three(0)  # Workaround for function ptrs not being resolved
    cmd_fns: Const[Infer] = list([{name: "one", func: one}, {name: "two", func: two}, {
                                  name: "three", func: three},], CmdFn)

    result: Var[i32] = start_value
    i: comptime | Var[Infer] = 0
    with inline:
        while i < cmd_fns.len:
            if cmd_fns[i].name[0] == prefix_char:
                result = cmd_fns[i].func(result)
            i += 1
    return result


@zig()
def perform_fn() -> Error[anyerror, void]:
    std: Const[Infer] = Import("std")
    expect: Const[Infer] = std.testing.expect

    Try(expect(performFn(chr('t'), 1) == 6))
    Try(expect(performFn(chr('o'), 0) == 1))
    Try(expect(performFn(chr('w'), 99) == 99))


def test_perform_fn():
    perform_fn()


@zig()
def fibonacci(index: u32) -> u32:
    if index < 2:
        return index
    return fibonacci(index - 1) + fibonacci(index - 2)


@zig()
def fibonacci_test() -> Error[anyerror, void]:
    std: Const[Infer] = Import("std")
    expect: Const[Infer] = std.testing.expect

    Try(expect(fibonacci(7) == 13))

    with comptime:
        Try @ expect(fibonacci(7) == 13)


def test_fibonacci():
    fibonacci_test()


@zig(export=False)
def List(T: comptime | type) -> type:
    class Temp(ZigStruct):
        items: Slice[T]
        len: usize

    return Temp


@zig()
def list_test() -> Error[anyerror, void]:
    std: Const[Infer] = Import("std")
    expect: Const[Infer] = std.testing.expect

    buffer: Var[Array[10, i32]] = undefined
    list: Const[List(i32)] = {items: ref(buffer), len: 0}

    Try(expect(list.len == 0))


def test_list():
    list_test()


@zig_struct()
class Point4(ZigStruct):
    x: u32
    y: u32

    z: Var[u32] = 1


@zig()
def decl_access_by_string() -> Error[anyerror, void]:
    std: Const[Infer] = Import("std")
    expect: Const[Infer] = std.testing.expect

    Try(expect(Field(Point4, "z") == 1))
    Point4.z = 2
    Try(expect(Field(Point4, "z") == 2))


def test_decl_access_by_string():
    decl_access_by_string()


@zig_struct()
class Foo5(ZigStruct):
    nope: i32

    blah: Var[Infer] = "xxx"
    hi: Const[Infer] = 1


@zig()
def has_decl() -> Error[anyerror, void]:
    std: Const[Infer] = Import("std")
    expect: Const[Infer] = std.testing.expect

    Try(expect(HasDecl(Foo5, "blah")))
    Try(expect(HasDecl(Foo5, "hi")))
    Try(expect(not HasDecl(Foo5, "nope")))
    Try(expect(not HasDecl(Foo5, "nope1234")))


def test_has_decl():
    has_decl()


@zig()
def vector_shuffle() -> Error[anyerror, void]:
    std: Const[Infer] = Import("std")
    expect: Const[Infer] = std.testing.expect

    a: Const[Vector(7, u8)] = Vector(7, u8)(chr('o'), chr(
        'l'), chr('h'), chr('e'), chr('r'), chr('z'), chr('w'))
    b: Const[Vector(4, u8)] = Vector(4, u8)(
        chr('w'), chr('d'), chr('!'), chr('x'))

    mask1: Const[Infer] = Vector(5, i32)(2, 3, 1, 1, 0)
    res1: Const[Vector(5, u8)] = Shuffle(u8, a, undefined, mask1)
    Try(expect(std.mem.eql(u8, ref(As(type(Array[5, u8]), res1)), "hello")))

    mask2: Const[Infer] = Vector(6, i32)(-1, 0, 4, 1, -2, -3)
    res2: Const[Vector(6, u8)] = Shuffle(u8, a, b, mask2)
    Try(expect(std.mem.eql(u8, ref(As(type(Array[6, u8]), res2)), "world!")))


def test_vector_shuffle():
    vector_shuffle()


@zig()
def vector_reduce() -> Error[anyerror, void]:
    std: Const[Infer] = Import("std")
    expect: Const[Infer] = std.testing.expect

    V: Const[Infer] = Vector(4, i32)
    value: Const[V] = (1, -1, 1, -1)
    result: Const[Infer] = value > As(V, Splat(0))
    with comptime:
        Try(expect(TypeOf(result) == Vector(4, bool)))
    is_all_true: Const[Infer] = Reduce(enum(And), result)
    with comptime:
        Try(expect(TypeOf(is_all_true) == bool))
    Try(expect(is_all_true == False))


def test_vector_reduce():
    vector_reduce()


@zig()
def round_test() -> Error[anyerror, void]:
    std: Const[Infer] = Import("std")
    expect: Const[Infer] = std.testing.expect

    Try(expect(Round(1.4) == 1))
    Try(expect(Round(1.5) == 2))
    Try(expect(Round(-1.4) == -1))
    Try(expect(Round(-2.5) == -3))


def test_round():
    round_test()


@zig(export=False)
def List2(T: comptime | type) -> type:
    class Temp(ZigStruct):
        items: Slice[T]

        Self: Const[Infer] = This()

        def length(self: Self) -> usize:
            return self.items.len

    return Temp


@zig()
def this_test() -> Error[anyerror, void]:
    std: Const[Infer] = Import("std")
    expect: Const[Infer] = std.testing.expect

    items: Var[Infer] = list([1, 2, 3, 4], i32)
    list: Const[List2(i32)] = {items: items[0:]}

    Try(expect(list.length() == 4))


def test_this():
    this_test()


@zig()
def integer_truncation() -> Error[anyerror, void]:
    std: Const[Infer] = Import("std")
    expect: Const[Infer] = std.testing.expect

    a: Const[u16] = 0xabcd
    b: Const[u8] = Truncate(a)
    Try(expect(b == 0xcd))


def test_integer_truncation():
    integer_truncation()
