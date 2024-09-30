import ast
import json
import io
import inspect
import os
import sys
import subprocess
import ctypes
from typing import Any, Tuple, Type, TypeVar, TextIO, Generic, get_origin, Callable, Union

compiled_fns = {}
compiled_classes = {}
lib = None
fn_return_type = {}
fn_arg_types = {}
current_union_tag = None
current_struct_extern = True
zig_decorated_fns = {}
semicolon_required = False
state = 'Function'


# Zig base class for Structs
class ZigStruct:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


# Zig base class for Errors
class ZigError:
    ...

# Zig base class for Structs


class ZigPackedStruct:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


# Zig base class for Enums
class ZigEnum:
    def __init__(self, value: Any):
        self.value = value

    @classmethod
    def members(cls):
        return {key: value for key, value in cls.__annotations__.items()}


# Zig base class for Unions
class ZigUnion:
    def __init__(self, **kwargs):
        if len(kwargs) != 1:
            raise ValueError(
                "ZigUnion can only hold one active member at a time")
        for key, value in kwargs.items():
            setattr(self, key, value)


class ZigTaggedUnion:
    def __init__(self,  **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class ZigType:
    def __init__(self, value):
        self.value = value

# TODO: Maybe C ABI types, + type type


class void(ZigType):
    ...


class anyerror(ZigType):
    ...


class anytype(ZigType):
    ...


class anyopaque(ZigType):
    ...


class comptime_int(ZigType):
    ...


class comptime_float(ZigType):
    ...


class noreturn(ZigType):
    ...


class i64(ZigType):
    ...


class i32(ZigType):
    ...


class i16(ZigType):
    ...


class i8(ZigType):
    ...


class u64(ZigType):
    ...


class u32(ZigType):
    ...


class u16(ZigType):
    ...


class u8(ZigType):
    ...


class i128(ZigType):
    ...


class u128(ZigType):
    ...


class isize(ZigType):
    ...


class usize(ZigType):
    ...


class f16(ZigType):
    ...


class f32(ZigType):
    ...


class f64(ZigType):
    ...


class f80(ZigType):
    ...


class f128(ZigType):
    ...


# Generic named Error to indicate that a function can raise an exception
# TODO: Add Error type to this
E = TypeVar('E')
T = TypeVar('T')
Error = Tuple[E, T]
Error.__name__ = 'Error'

Const = Type[T]
Const.__name__ = 'const'
Var = Type[T]
Var.__name__ = 'var'


# function ref (basically returns the refernce of the data)
def ref(value: T) -> T:
    return value


# class Array(Generic[T]):
#     def __class_getitem__(cls, params):
#         size, typ = params
#         return f'Array[{size}, {typ}]'

class Slice(Generic[T]):
    def __init__(self, value: T):
        self.value = value

    def get_value(self) -> T:
        return self.value


Array = Type[T]
Array.__name__ = 'Array'

CArray = Type[T]
CArray.__name__ = 'CArray'
# Slice = Type[T]
Slice.__name__ = 'Slice'
Optional = Type[T]
Optional.__name__ = 'Optional'

Ptr = Type[T]
Ptr.__name__ = 'Ptr'

Infer = TypeVar('Infer')

comptime = TypeVar('comptime')
defer = TypeVar('defer')
errdefer = TypeVar('errdefer')
undefined = TypeVar('undefined')
block = TypeVar('block')


allowed_types = {
    'i64': i64,
    'f64': f64,
    'void': void,
}

builtin_fns = {
    'AddrSpaceCast': '@addrSpaceCast',
    'AddWithOverflow': '@addWithOverflow',
    'AlignCast': '@alignCast',
    'AlignOf': '@alignOf',
    'As': '@as',
    'AtomicLoad': '@atomicLoad',
    'AtomicRmw': '@atomicRmw',
    'AtomicStore': '@atomicStore',
    'BitCast': '@bitCast',
    'BitOffsetOf': '@bitOffsetOf',
    'BitSizeOf': '@bitSizeOf',
    'BranchHint': '@branchHint',
    'Breakpoint': '@breakpoint',
    'MulAdd': '@mulAdd',
    'ByteSwap': '@byteSwap',
    'BitReverse': '@bitReverse',
    'OffsetOf': '@offsetOf',
    'Call': '@call',
    'CDefine': '@cDefine',
    'CImport': '@cImport',
    'CInclude': '@cInclude',
    'Clz': '@clz',
    'CmpxchgStrong': '@cmpxchgStrong',
    'CmpxchgWeak': '@cmpxchgWeak',
    'CompileError': '@compileError',
    'CompileLog': '@compileLog',
    'ConstCast': '@constCast',
    'Ctz': '@ctz',
    'CUndef': '@cUndef',
    'CVaArg': '@cVaArg',
    'CVaCopy': '@cVaCopy',
    'CVaEnd': '@cVaEnd',
    'CVaStart': '@cVaStart',
    'DivExact': '@divExact',
    'DivFloor': '@divFloor',
    'DivTrunc': '@divTrunc',
    'EmbedFile': '@embedFile',
    'EnumFromInt': '@enumFromInt',
    'ErrorFromInt': '@errorFromInt',
    'ErrorName': '@errorName',
    'ErrorReturnTrace': '@errorReturnTrace',
    'ErrorCast': '@errorCast',
    'Export': '@export',
    'Extern': '@extern',
    'Fence': '@fence',
    'Field': '@field',
    'FieldParentPtr': '@fieldParentPtr',
    'FloatCast': '@floatCast',
    'FloatFromInt': '@floatFromInt',
    'FrameAddress': '@frameAddress',
    'HasDecl': '@hasDecl',
    'HasField': '@hasField',
    'Import': '@import',
    'InComptime': '@inComptime',
    'IntCast': '@intCast',
    'IntFromBool': '@intFromBool',
    'IntFromEnum': '@intFromEnum',
    'IntFromError': '@intFromError',
    'IntFromFloat': '@intFromFloat',
    'IntFromPtr': '@intFromPtr',
    'Max': '@max',
    'Memcpy': '@memcpy',
    'Memset': '@memset',
    'Min': '@min',
    'WasmMemorySize': '@wasmMemorySize',
    'WasmMemoryGrow': '@wasmMemoryGrow',
    'Mod': '@mod',
    'MulWithOverflow': '@mulWithOverflow',
    'Panic': '@panic',
    'PopCount': '@popCount',
    'Prefetch': '@prefetch',
    'PtrCast': '@ptrCast',
    'PtrFromInt': '@ptrFromInt',
    'Rem': '@rem',
    'ReturnAddress': '@returnAddress',
    'Select': '@select',
    'SetAlignStack': '@setAlignStack',
    'SetEvalBranchQuota': '@setEvalBranchQuota',
    'SetFloatMode': '@setFloatMode',
    'SetRuntimeSafety': '@setRuntimeSafety',
    'ShlExact': '@shlExact',
    'ShlWithOverflow': '@shlWithOverflow',
    'ShrExact': '@shrExact',
    'Shuffle': '@shuffle',
    'SizeOf': '@sizeOf',
    'Splat': '@splat',
    'Reduce': '@reduce',
    'Src': '@src',
    'Sqrt': '@sqrt',
    'Sin': '@sin',
    'Cos': '@cos',
    'Tan': '@tan',
    'Exp': '@exp',
    'Exp2': '@exp2',
    'Log': '@log',
    'Log2': '@log2',
    'Log10': '@log10',
    'Abs': '@abs',
    'Floor': '@floor',
    'Ceil': '@ceil',
    'Trunc': '@trunc',
    'Round': '@round',
    'SubWithOverflow': '@subWithOverflow',
    'TagName': '@tagName',
    'This': '@This',
    'Trap': '@trap',
    'Truncate': '@truncate',
    'Type': '@Type',
    'TypeInfo': '@typeInfo',
    'TypeName': '@typeName',
    'TypeOf': '@TypeOf',
    'UnionInit': '@unionInit',
    'Vector': '@Vector',
    'VolatileCast': '@volatileCast',
    'WorkGroupId': '@workGroupId',
    'WorkGroupSize': '@workGroupSize',
    'WorkItemId': '@workItemId',
}

# Add the builtin functions to python namespace, Workaround!!
for fn_name in builtin_fns:
    globals()[fn_name] = lambda *args: (fn_name, args)


def check_annotations(annotations: dict[str, Type]):
    for arg, type_ in annotations.items():
        # Check if the type is Error
        if get_origin(type_) is tuple:
            continue
        if type_ not in allowed_types.values():
            raise TypeError(f'Invalid type {type_} for argument {arg}')

    # Return type is required
    if 'return' not in annotations:
        raise TypeError('Return type is required')


def is_array_type(annotation):
    if isinstance(annotation, ast.Subscript):
        if annotation.value.id in ['Array', 'CArray', 'Slice']:
            return True
        if annotation.value.id in ['Const', 'Error', 'Optional']:
            return is_array_type(annotation.slice)
    elif isinstance(annotation, ast.Tuple):
        return is_array_type(annotation.elts[1])
    return False


def parse_return_type_annotation(annotation):
    """
    Parse Python function return type annotations and
    convert them to ctypes return types
    """
    if isinstance(annotation, ast.Name):
        # Handle basic types
        return _map_basic_type(annotation.id)
    elif isinstance(annotation, ast.Tuple):
        # Handle tuple types
        return tuple(parse_return_type_annotation(elt) for elt in annotation.elts)
    elif isinstance(annotation, ast.Subscript):
        # Handle subscripted types like Array, Const, etc.
        base = annotation.value.id
        if base in ['Array', 'CArray', 'Slice', 'Ptr']:
            inner_type = parse_return_type_annotation(annotation.slice)
            return ctypes.POINTER(inner_type)
        elif base in ['Const', "Optional"]:
            return parse_return_type_annotation(annotation.slice)
        elif base == "Error":
            _, inner_type = parse_return_type_annotation(
                annotation.slice)
            return inner_type
        else:
            raise NotImplementedError(f'Unsupported subscript base {base}')
    elif isinstance(annotation, ast.BinOp):
        return parse_return_type_annotation(annotation.right)
    else:
        raise NotImplementedError(
            f'Unsupported return type annotation {annotation}')


def _map_basic_type(type_name):
    """
    Map basic Python types to ctypes types
    """
    type_map = {
        'int': ctypes.c_int,
        'float': ctypes.c_float,
        'str': ctypes.c_char_p,
        'bytes': ctypes.c_char_p,  # ctypes uses c_char_p for strings and bytes
        'bool': ctypes.c_bool,
        'None': None,  # void return type
        # Add more types as needed, e.g., u8, i64, etc.
        'u8': ctypes.c_uint8,
        'i8': ctypes.c_int8,
        'u16': ctypes.c_uint16,
        'i16': ctypes.c_int16,
        'u32': ctypes.c_uint32,
        'i32': ctypes.c_int32,
        'i64': ctypes.c_int64,
        'u64': ctypes.c_uint64,
        'f32': ctypes.c_float,
        'f64': ctypes.c_double,
        'void': None,
        'anyerror': None,
        'anytype': None,
        'noreturn': None,
        'type': None,
        'isize': ctypes.c_int,
        'usize': ctypes.c_uint,
    }
    if type_name in type_map:
        return type_map[type_name]
    elif type_name in compiled_classes:
        return ctypes.POINTER(type_name)
    else:
        raise NotImplementedError(f'Unsupported basic type {type_name}')


def parse_function_def(node: ast.FunctionDef, writer: TextIO):
    global state, current_struct_extern
    current_struct_extern = False
    prev_state = state
    state = 'Function'
    writer.write(f'pub fn {node.name} (')
    for arg in node.args.args:
        if isinstance(arg.annotation, ast.BinOp):
            parse_ast(arg.annotation.left, writer)
            writer.write(' ')
            writer.write(f'{arg.arg}: ')
            parse_type_annotation(arg.annotation.right, writer)
        else:
            writer.write(f'{arg.arg}: ')
            parse_type_annotation(arg.annotation, writer)
        writer.write(', ')
    writer.write(') ')
    if isinstance(node.returns, ast.Subscript):
        if node.returns.value.id == 'Error':
            parse_type_annotation(node.returns.slice.elts[0], writer)
            writer.write('!')
        # elif node.returns.value.id == 'Optional':
        #     writer.write('?')
    parse_type_annotation(node.returns, writer)
    writer.write(' {\n')
    for stmt in node.body:
        parse_ast(stmt, writer)
    writer.write('}\n')
    state = prev_state


def parse_return(node: ast.Return, writer: TextIO):
    writer.write('return ')
    parse_ast(node.value, writer)
    writer.write(';\n')


def parse_binop(node: ast.BinOp, writer: TextIO):
    if not (isinstance(node.op, ast.MatMult) and isinstance(node.right, ast.Call) and isinstance(node.right.func, ast.Name) and node.right.func.id == 'catch' and len(node.right.args) == 1 and isinstance(node.right.args[0], ast.Name) and node.right.args[0].id == '_'):
        writer.write('(')
    if isinstance(node.op, ast.MatMult) and isinstance(node.left, ast.Name) and node.left.id == 'Try':
        writer.write('try ')
    else:
        parse_ast(node.left, writer)
    if isinstance(node.op, ast.Add):
        writer.write(' + ')
    elif isinstance(node.op, ast.Mult):
        writer.write(' * ')
    elif isinstance(node.op, ast.Sub):
        writer.write(' - ')
    elif isinstance(node.op, ast.Div):
        writer.write(' / ')
    elif isinstance(node.op, ast.Mod):
        writer.write(' % ')
    elif isinstance(node.op, ast.LShift):
        writer.write(' << ')
    elif isinstance(node.op, ast.RShift):
        writer.write(' >> ')
    elif isinstance(node.op, ast.BitAnd):
        writer.write(' & ')
    elif isinstance(node.op, ast.BitOr):
        writer.write(' | ')
    elif isinstance(node.op, ast.BitXor):
        writer.write(' ^ ')
    elif isinstance(node.op, ast.MatMult):
        writer.write(' ')
    elif isinstance(node.op, ast.Pow):
        writer.write(' ** ')
    else:
        raise NotImplementedError(
            f'Unsupported binary operator {type(node.op)}')

    parse_ast(node.right, writer)
    if not (isinstance(node.op, ast.MatMult) and isinstance(node.right, ast.Call) and isinstance(node.right.func, ast.Name) and node.right.func.id == 'catch' and len(node.right.args) == 1 and isinstance(node.right.args[0], ast.Name) and node.right.args[0].id == '_'):
        writer.write(')')


def parse_constant(node: ast.Constant, writer: TextIO):
    if type(node.value) is str:
        writer.write(json.dumps(node.value, ensure_ascii=False))
    elif type(node.value) is bool:
        writer.write('true' if node.value else 'false')
    elif node.value is None:
        writer.write('null')
    else:
        writer.write(str(node.value))


def parse_name(node: ast.Name, writer: TextIO):
    if node.id == "assert_":
        writer.write('assert')
    else:
        writer.write(str(node.id))


def parse_subscript(node: ast.Subscript, writer: TextIO):
    if isinstance(node.value, ast.Name) and node.value.id == 'Union':
        for elt in node.slice.elts:
            parse_ast(elt, writer)
            if elt != node.slice.elts[-1]:
                writer.write(' || ')
        return
    parse_ast(node.value, writer)
    if isinstance(node.slice, ast.Constant) and isinstance(node.slice.value, str):
        writer.write('.@')
        parse_ast(node.slice, writer)
    else:
        writer.write('[')
        parse_ast(node.slice, writer)
        writer.write(']')


def parse_type_annotation(annotation, writer, only_type=False):
    if isinstance(annotation, ast.Name):
        writer.write(annotation.id)  # Basic types like u8, i64
    elif isinstance(annotation, ast.Subscript):
        # Handle subscripted types like Array[u8], Const[StructType]
        base = annotation.value.id
        if base == 'Array':
            if not only_type:
                writer.write('[')
                if isinstance(annotation.slice, ast.Tuple):
                    # Check only 2 args
                    if len(annotation.slice.elts) > 3:
                        raise NotImplementedError(
                            'Unsupported number of arguments for Array, expected <= 3')
                    if isinstance(annotation.slice.elts[0], ast.Constant) and annotation.slice.elts[0].value == '*':
                        writer.write('*')
                    else:
                        parse_ast(annotation.slice.elts[0], writer)
                    if len(annotation.slice.elts) == 3:
                        writer.write(':')
                        parse_ast(annotation.slice.elts[1], writer)
                else:
                    writer.write('*')
                writer.write(']')
            parse_type_annotation(annotation.slice, writer, only_type)
        elif base == "Slice":
            if not only_type:
                if isinstance(annotation.slice, ast.Tuple) and len(annotation.slice.elts) == 2:
                    writer.write('[:')
                    parse_ast(annotation.slice.elts[0], writer)
                    writer.write(']')
                else:
                    writer.write('[]')
            parse_type_annotation(annotation.slice, writer, only_type)
        elif base == 'CArray':
            if not only_type:
                writer.write('[*c]')
            # Parse the inner type
            parse_type_annotation(annotation.slice, writer, only_type)
        elif base == 'Const':
            writer.write('const ')
            # Parse the inner type
            parse_type_annotation(annotation.slice, writer, only_type)
        elif base == 'Error':
            # writer.write('!')
            parse_type_annotation(annotation.slice, writer, only_type)
        elif base == 'Optional':
            writer.write('?')
            parse_type_annotation(annotation.slice, writer, only_type)
        elif base == 'Ptr':
            writer.write('*')
            parse_type_annotation(annotation.slice, writer, only_type)
        elif base == 'Callable':
            writer.write('fn(')
            if isinstance(annotation.slice, ast.Tuple):
                assert len(annotation.slice.elts) == 2
                for i, arg in enumerate(annotation.slice.elts[0].elts):
                    parse_type_annotation(arg, writer)
                    if i < len(annotation.slice.elts[0].elts) - 1:
                        writer.write(', ')
                writer.write(')  ')
                parse_type_annotation(annotation.slice.elts[1], writer)
        else:
            raise NotImplementedError(f'Unsupported subscript base {base}')
    elif isinstance(annotation, ast.Tuple):
        if len(annotation.elts) == 2:  # Error type, big assumption here, fix later
            # parse_type_annotation(annotation.elts[0], writer, only_type)
            # writer.write('!')
            parse_type_annotation(annotation.elts[1], writer, only_type)
        elif len(annotation.elts) == 3:
            parse_type_annotation(annotation.elts[2], writer, only_type)
    elif isinstance(annotation, ast.Attribute):
        parse_type_annotation(annotation.value, writer, only_type)
        writer.write('.')
        writer.write(annotation.attr)
    elif isinstance(annotation, ast.Constant):
        writer.write(str(annotation.value))
    elif isinstance(annotation, ast.Call):
        parse_ast(annotation, writer)
    else:
        raise NotImplementedError(
            f'Unsupported type annotation {annotation}')


def parse_ann_assign(node: ast.AnnAssign, writer: TextIO):
    # Determine if it's a constant or variable declaration
    if isinstance(node.annotation, ast.BinOp):
        parse_ast(node.annotation.left, writer)
        writer.write(' ')
        value = node.annotation.right.value
        slice = node.annotation.right.slice
    elif isinstance(node.annotation, ast.Name):
        value = node.annotation
        slice = node.annotation
    else:
        value = node.annotation.value
        slice = node.annotation.slice
    # if state == 'Function':
    if not isinstance(node.annotation, ast.Name):
        if value.id == 'Const':
            writer.write('const ')
        elif value.id == 'Var':
            writer.write('var ')
        else:
            value = node.annotation
            slice = node.annotation

    # Write the target variable name
    parse_ast(node.target, writer)
    # If there's a type annotation, handle it
    if isinstance(slice, ast.Subscript):
        writer.write(': ')
        if slice.value.id == "Error":
            parse_type_annotation(slice.slice.elts[0], writer)
            writer.write('!')
        parse_type_annotation(slice, writer)
    elif isinstance(slice, ast.Name):
        if slice.id != 'Infer':
            writer.write(': ')
            writer.write(slice.id)
    elif isinstance(slice, ast.Call):
        # if slice.func.id == 'Vector':
        writer.write(': ')
        parse_call(slice, writer)

    elif isinstance(slice, ast.Attribute):
        writer.write(': ')
        parse_type_annotation(slice, writer)
    else:
        raise NotImplementedError(
            f'Unsupported annotation slice {slice}')

    # Write the assignment value
    if node.value:
        writer.write(' = ')
        if isinstance(node.value, ast.Name) and node.value.id == '_':
            global semicolon_required
            semicolon_required = True
            return
        parse_ast(node.value, writer)
    if state == 'Function' or getattr(value, 'id', None) in ['Const', 'Var']:
        writer.write(';\n')
    else:
        writer.write(',\n')


def parse_assign(node: ast.Assign, writer: TextIO):
    parse_ast(node.targets[0], writer)
    writer.write(' = ')
    parse_ast(node.value, writer)
    writer.write(';\n')


def parse_aug_assign(node: ast.AugAssign, writer: TextIO):
    parse_ast(node.target, writer)
    if isinstance(node.op, ast.Add):
        writer.write(' += ')
    elif isinstance(node.op, ast.Mult):
        writer.write(' *= ')
    elif isinstance(node.op, ast.Sub):
        writer.write(' -= ')
    elif isinstance(node.op, ast.Div):
        writer.write(' /= ')
    elif isinstance(node.op, ast.Mod):
        writer.write(' %= ')
    else:
        raise NotImplementedError(
            f'Unsupported binary operator {type(node.op)}')
    parse_ast(node.value, writer)
    writer.write(';\n')


def parse_tuple(node: ast.Tuple, writer: TextIO):
    writer.write('.{')
    for i, elt in enumerate(node.elts):
        parse_ast(elt, writer)
        if i < len(node.elts) - 1:
            writer.write(', ')
    writer.write('}')


def parse_call(node: ast.Call, writer: TextIO):
    if isinstance(node.func, ast.Name) and node.func.id == 'list':
        # Handle list call explicitly
        writer.write('[_]')
        # The second argument is the type (e.g., i64)
        parse_ast(node.args[1], writer)
        # The first argument is the actual list (e.g., [1, 2, 3])
        parse_ast(node.args[0], writer)
        return
    if isinstance(node.func, ast.Name) and node.func.id == 'ref':
        # Check only 1 arg
        if len(node.args) != 1:
            raise NotImplementedError(
                f'Unsupported number of arguments for ref, expected 1')
        writer.write('&')
        parse_ast(node.args[0], writer)
        return

    if isinstance(node.func, ast.Name) and node.func.id == 'range':
        # Converting to zig slicing syntax 0..10
        parse_ast(node.args[0], writer)
        writer.write('..')
        # if second arg is None, then it's an infinite range
        if isinstance(node.args[1], ast.Constant) and node.args[1].value is None:
            return
        parse_ast(node.args[1], writer)
        return
    if isinstance(node.func, ast.Name) and node.func.id == 'cat':
        if len(node.args) < 2:
            raise NotImplementedError(
                f'Unsupported number of arguments for cat, expected >= 2')
        for i, arg in enumerate(node.args):
            parse_ast(arg, writer)
            if i < len(node.args) - 1:
                writer.write(' ++ ')
        return
    if isinstance(node.func, ast.Name) and node.func.id == 'repeat':
        if len(node.args) != 2:
            raise NotImplementedError(
                f'Unsupported number of arguments for repeat, expected 2')
        parse_ast(node.args[0], writer)
        writer.write(' ** ')
        parse_ast(node.args[1], writer)
        return
    if isinstance(node.func, ast.Name) and node.func.id == 'type':
        if len(node.args) != 1:
            raise NotImplementedError(
                f'Unsupported number of arguments for type, expected 1')
        parse_type_annotation(node.args[0], writer)
        return
    if isinstance(node.func, ast.Name) and node.func.id == 'unreachable':
        writer.write('unreachable')
        return
    if isinstance(node.func, ast.Name) and node.func.id == 'break_return':
        assert len(node.args) <= 2
        if len(node.args) == 1:
            writer.write('break :blk ')
            parse_ast(node.args[0], writer)
        elif len(node.args) == 2:
            block_name = node.args[0].id
            writer.write(f'break :{block_name} ')
            parse_ast(node.args[1], writer)
        return
    if isinstance(node.func, ast.Name) and node.func.id == 'enum':
        assert len(node.args) == 1
        writer.write('.')
        parse_ast(node.args[0], writer)
        return
    if isinstance(node.func, ast.Name) and node.func.id == 'catch':
        assert len(node.args) == 1
        writer.write('catch ')
        if isinstance(node.args[0], ast.Name) and node.args[0].id == '_':
            return
        parse_ast(node.args[0], writer)
        return
    elif isinstance(node.func, ast.Name) and node.func.id in builtin_fns:
        writer.write(builtin_fns[node.func.id])
    elif isinstance(node.func, ast.Name) and node.func.id == 'Try':
        writer.write('try ')
    elif isinstance(node.func, ast.Name) and node.func.id == 'chr':
        # Check only one arg and its a str of len 1
        if isinstance(node.args[0], ast.Constant) and isinstance(node.args[0].value, str) and len(node.args[0].value) == 1:
            writer.write(f"'{node.args[0].value}'")
            return
        else:
            raise NotImplementedError(
                f'Unsupported argument for chr, expected a single character string')
    else:
        parse_ast(node.func, writer)
    if isinstance(node.func, ast.Call) and node.func.func.id == 'Vector':
        writer.write('{')
    else:
        writer.write('(')
    for i, arg in enumerate(node.args):
        parse_ast(arg, writer)
        if i < len(node.args) - 1:
            writer.write(', ')
    if isinstance(node.func, ast.Call) and node.func.func.id == 'Vector':
        writer.write('}')
    else:
        writer.write(')')


def parse_attribute(node: ast.Attribute, writer: TextIO):
    parse_ast(node.value, writer)
    writer.write('.')
    if node.attr == 'assert_':  # Not the greatest solution, blah
        writer.write('assert')
    elif node.attr == 'deref':
        writer.write('*')
    elif node.attr == 'unwrap':
        writer.write('?')
    else:
        writer.write(node.attr)


def parse_expr(node: ast.Expr, writer: TextIO):
    parse_ast(node, writer)
    writer.write(';\n')


def parse_if(node: ast.If, writer: TextIO):
    if isinstance(node.test, ast.Call) and node.test.func.id in ['capture', 'capture_err']:
        assert len(node.test.args) in [2, 3]
        writer.write('if (')
        parse_ast(node.test.args[0], writer)
        writer.write(') |')
        parse_ast(node.test.args[1], writer)
        writer.write('| {\n')
    else:
        writer.write('if (')
        parse_ast(node.test, writer)
        writer.write(') {\n')
    for stmt in node.body:
        parse_ast(stmt, writer)
    if isinstance(node.test, ast.Call) and node.test.func.id == 'capture_err':
        assert len(node.test.args) == 3
        err_name = node.test.args[2].id
        writer.write('} else |')
        writer.write(err_name)
        writer.write('| {\n')
    else:
        writer.write('} else {\n')
    for stmt in node.orelse:
        parse_ast(stmt, writer)
    writer.write('}\n')


def parse_compare(node: ast.Compare, writer: TextIO):
    parse_ast(node.left, writer)
    for i, op in enumerate(node.ops):
        if isinstance(op, ast.Eq):
            writer.write(' == ')
        elif isinstance(op, ast.NotEq):
            writer.write(' != ')
        elif isinstance(op, ast.Lt):
            writer.write(' < ')
        elif isinstance(op, ast.LtE):
            writer.write(' <= ')
        elif isinstance(op, ast.Gt):
            writer.write(' > ')
        elif isinstance(op, ast.GtE):
            writer.write(' >= ')
        else:
            raise NotImplementedError(
                f'Unsupported comparison operator {type(op)}')
        parse_ast(node.comparators[i], writer)


def parse_if_exp(node: ast.IfExp, writer: TextIO):
    writer.write('if (')
    parse_ast(node.test, writer)
    writer.write(') ')
    parse_ast(node.body, writer)
    writer.write(' else ')
    parse_ast(node.orelse, writer)


def parse_for(node: ast.For, writer: TextIO):
    writer.write('for (')
    if isinstance(node.iter, ast.Tuple):
        for i, target in enumerate(node.iter.elts):
            parse_ast(target, writer)
            if i < len(node.iter.elts) - 1:
                writer.write(', ')
    else:
        parse_ast(node.iter, writer)
    writer.write(') |')
    if isinstance(node.target, ast.Tuple):
        for i, target in enumerate(node.target.elts):
            parse_ast(target, writer)
            if i < len(node.target.elts) - 1:
                writer.write(', ')
    else:
        parse_ast(node.target, writer)
    writer.write('| {\n')
    for stmt in node.body:
        parse_ast(stmt, writer)
    writer.write('}\n')

    if node.orelse:
        writer.write('else {\n')
        for stmt in node.orelse:
            parse_ast(stmt, writer)
        writer.write('}\n')


def parse_list(node: ast.List, writer: TextIO):
    writer.write('{')
    for i, elt in enumerate(node.elts):
        parse_ast(elt, writer)
        if i < len(node.elts) - 1:
            writer.write(', ')
    writer.write('}')


def parse_with(node: ast.With, writer: TextIO):
    global semicolon_required
    # Handle comptime block, everything else is ignored
    if isinstance(node.items[0].context_expr, ast.Name):
        if node.items[0].context_expr.id in ['comptime', 'defer', 'errdefer']:
            writer.write(f'{node.items[0].context_expr.id}{{\n')
            for stmt in node.body:
                parse_ast(stmt, writer)
            writer.write('}\n')
        elif node.items[0].context_expr.id == 'block':
            if writer.getvalue().strip().endswith('catch ;'):  # NOTE: Hacky way to check if catch block is open
                writer.seek(writer.tell() - 2)
                writer.truncate()
                semicolon_required = True
            writer.write('{\n')
            for stmt in node.body:
                parse_ast(stmt, writer)
            writer.write('}\n')
            if semicolon_required:
                writer.write(';\n')
                semicolon_required = False
        elif node.items[0].context_expr.id == 'inline':
            assert len(node.items) == 1, 'Only one inline block is supported'
            writer.write('inline ')
            for stmt in node.body:
                parse_ast(stmt, writer)
        else:
            raise NotImplementedError(
                f'Unsupported with context {node.items[0].context_expr.id}')
    elif isinstance(node.items[0].context_expr, ast.Call):
        if node.items[0].context_expr.func.id == 'block':
            assert len(node.items[0].context_expr.args) == 1
            if writer.getvalue().strip().endswith('catch ;'):  # NOTE: Hacky way to check if catch block is open
                writer.seek(writer.tell() - 2)
                writer.truncate()
                semicolon_required = True
            parse_ast(node.items[0].context_expr.args[0], writer)
            writer.write(': {\n')
            for stmt in node.body:
                parse_ast(stmt, writer)
            writer.write('}\n')
            if semicolon_required:
                writer.write(';\n')
                semicolon_required = False
        if node.items[0].context_expr.func.id == 'errdefer':
            assert len(node.items[0].context_expr.args) == 1
            writer.write('errdefer |')
            parse_ast(node.items[0].context_expr.args[0], writer)
            writer.write('| {\n')
            for stmt in node.body:
                parse_ast(stmt, writer)
            writer.write('}\n')

    else:
        raise NotImplementedError(
            f'Unsupported with context {node.items[0].context_expr}')


def parse_starred(node: ast.With, writer: TextIO):
    writer.write('*')
    parse_ast(node.value, writer)


def parse_unary_op(node: ast.UnaryOp, writer: TextIO):
    writer.write('(')
    if isinstance(node.op, ast.USub):
        writer.write('-')
    elif isinstance(node.op, ast.UAdd):
        writer.write('+')
    elif isinstance(node.op, ast.Invert):
        writer.write('~')
    elif isinstance(node.op, ast.Not):
        writer.write('!')
    else:
        raise NotImplementedError(
            f'Unsupported unary operator {type(node.op)}')
    parse_ast(node.operand, writer)
    writer.write(')')


def parse_bool_op(node: ast.BoolOp, writer: TextIO):
    for i, value in enumerate(node.values):
        parse_ast(value, writer)
        if i < len(node.values) - 1:
            if isinstance(node.op, ast.And):
                writer.write(' and ')
            elif isinstance(node.op, ast.Or):
                writer.write(' or ')
            else:
                raise NotImplementedError(
                    f'Unsupported boolean operator {type(node.op)}')


def parse_enum(body, writer: TextIO):
    for stmt in body:
        if isinstance(stmt, ast.Assign):
            assert len(stmt.targets) == 1
            if isinstance(stmt.value, ast.Call) and stmt.value.func.id == 'auto':
                writer.write(f'{stmt.targets[0].id},\n')
            else:
                writer.write(f'{stmt.targets[0].id} = ')
                parse_ast(stmt.value, writer)
                writer.write(',\n')
        else:
            parse_ast(stmt, writer)


def parse_error_union(body, writer: TextIO):
    for stmt in body:
        if isinstance(stmt, ast.Assign):
            assert len(stmt.targets) == 1
            if isinstance(stmt.value, ast.Call) and stmt.value.func.id == 'auto':
                writer.write(f'{stmt.targets[0].id},\n')
            else:
                raise NotImplementedError(
                    f'Unsupported statement {stmt} in error union')
        else:
            raise NotImplementedError(
                f'Unsupported statement {stmt} in error union')


def parse_class_def(node: ast.ClassDef, writer: TextIO):
    global state, current_struct_extern
    prev_state = state
    state = 'Class'
    if node.bases[0].id == 'ZigStruct':
        assert len(node.bases) == 1
        writer.write(
            f'const {node.name} = {"extern" if current_struct_extern else ""} struct {{\n')
    elif node.bases[0].id == 'ZigPackedStruct':
        assert len(node.bases) == 1
        writer.write(f'const {node.name} = packed struct {{\n')
    elif node.bases[0].id == 'ZigEnum':
        writer.write(f'const {node.name} = enum \n')
        if len(node.bases) == 2:
            writer.write('(')
            parse_ast(node.bases[1], writer)
            writer.write(') ')
        writer.write('{\n')
        parse_enum(node.body, writer)
        writer.write('};\n')
        state = prev_state
        return
    elif node.bases[0].id == 'ZigUnion':
        writer.write(f'const {node.name} = union {{\n')
    elif node.bases[0].id == 'ZigTaggedUnion':
        writer.write(f'const {node.name} = union ({current_union_tag}) {{\n')
    elif node.bases[0].id == 'ZigError':
        writer.write(f'const {node.name} = error {{\n')
        parse_error_union(node.body, writer)
        writer.write('};\n')
        state = prev_state
        return
    else:
        raise NotImplementedError(
            f'Unsupported class base {node.bases[0].id}')

    for stmt in node.body:
        parse_ast(stmt, writer)
    writer.write('};\n')
    state = prev_state


def parse_dict(node: ast.Dict, writer: TextIO):
    writer.write('.{')
    for i, key in enumerate(node.keys):
        writer.write('.')
        parse_ast(key, writer)
        writer.write(' = ')
        parse_ast(node.values[i], writer)
        if i < len(node.keys) - 1:
            writer.write(', ')
    writer.write('}')


def parse_slice(node: ast.Slice, writer: TextIO):
    if node.lower:
        parse_ast(node.lower, writer)
    writer.write('..')
    if node.upper:
        parse_ast(node.upper, writer)
    if node.step:
        writer.write(':')
        parse_ast(node.step, writer)


# item => |item| blk: { ... }
def parse_match(node: ast.Match, writer: TextIO):
    writer.write('switch (')
    parse_ast(node.subject, writer)
    writer.write(') {\n')
    expr = False
    for case in node.cases:
        match_as = False
        parse_ast(case.pattern, writer)
        for n in ast.walk(case.pattern):
            if isinstance(n, ast.MatchAs) and n.pattern:
                match_as = True
                break
        # Walk through the body of the case and check whether any call to break_return is made
        for stmt in case.body:
            for n in ast.walk(stmt):
                if isinstance(n, ast.Call) and n.func.id == 'break_return':
                    expr = True
                    break
        if not match_as:
            writer.write(' => ')
        if expr:
            writer.write(' blk: {\n')
        else:
            writer.write(' {\n')
        for stmt in case.body:
            parse_ast(stmt, writer)
        writer.write('},\n')
    writer.write('}')
    if expr:
        global semicolon_required
        semicolon_required = False
        writer.write(';')


def parse_match_sequence(node: ast.MatchSequence, writer: TextIO):
    for pattern in node.patterns:
        parse_ast(pattern, writer)
        writer.write(', ')


def parse_match_class(node: ast.MatchClass, writer: TextIO):
    if isinstance(node.cls, ast.Name) and node.cls.id == 'enum':
        writer.write('.')
        assert len(node.patterns) == 1
        parse_ast(node.patterns[0], writer)
    if isinstance(node.cls, ast.Name) and node.cls.id == 'range_incl':
        assert len(node.patterns) == 2
        parse_ast(ast.parse(ast.unparse(
            node.patterns[0])).body[0].value, writer)
        # parse_ast(node.patterns[0], writer)
        writer.write('...')
        # parse_ast(node.patterns[1], writer)
        parse_ast(ast.parse(ast.unparse(
            node.patterns[1])).body[0].value, writer)
    if isinstance(node.cls, ast.Name) and node.cls.id == 'comptime':
        assert len(node.patterns) == 1
        parse_ast(node.patterns[0], writer)
    if isinstance(node.cls, ast.Name) and node.cls.id == 'inline':
        writer.write('inline ')
        for pattern in node.patterns:
            parse_ast(pattern, writer)
            if pattern != node.patterns[-1]:
                writer.write(', ')


def parse_match_value(node: ast.MatchValue, writer: TextIO):
    parse_ast(node.value, writer)


def parse_match_as(node: ast.MatchAs, writer: TextIO):
    if node.pattern:
        parse_ast(node.pattern, writer)
        writer.write(' => ')
        writer.write(' |')
        if node.name.startswith('_'):
            writer.write(f'*{node.name[1:]}')
        else:
            writer.write(node.name)
        writer.write('| \n')
    elif node.name:
        writer.write(node.name)
    else:
        writer.write('else')


def parse_match_or(node: ast.MatchOr, writer: TextIO):
    for pattern in node.patterns:
        parse_ast(pattern, writer)
        if pattern != node.patterns[-1]:
            writer.write(', ')


def parse_continue(node: ast.Continue, writer: TextIO):
    writer.write('continue;\n')


def parse_break(node: ast.Break, writer: TextIO):
    writer.write('break;\n')


def parse_while(node: ast.While, writer: TextIO):
    writer.write('while (')
    if isinstance(node.test, ast.Call) and node.test.func.id in ['capture', 'capture_err']:
        assert len(node.test.args) == 2
        parse_ast(node.test.args[0], writer)
        writer.write(') |')
        parse_ast(node.test.args[1], writer)
        writer.write('| {\n')
    else:
        parse_ast(node.test, writer)
        writer.write(') {\n')
    for stmt in node.body:
        parse_ast(stmt, writer)
    writer.write('}\n')
    if node.orelse:
        if isinstance(node.test, ast.Call) and node.test.func.id == 'capture_err':
            writer.write('else |err| {\n')
        else:
            writer.write('else {\n')
        for stmt in node.orelse:
            parse_ast(stmt, writer)
        writer.write('}\n')


def parse_ast(node, writer=sys.stdout):
    match type(node):
        case ast.FunctionDef:
            parse_function_def(node, writer)
        case ast.Return:
            parse_return(node, writer)
        case ast.BinOp:
            parse_binop(node, writer)
        case ast.Constant:
            parse_constant(node, writer)
        case ast.Name:
            parse_name(node, writer)
        case ast.Subscript:
            parse_subscript(node, writer)
        case ast.AnnAssign:
            parse_ann_assign(node, writer)
        case ast.Assign:
            parse_assign(node, writer)
        case ast.AugAssign:
            parse_aug_assign(node, writer)
        case ast.Tuple:
            parse_tuple(node, writer)
        case ast.List:
            parse_list(node, writer)
        case ast.Call:
            parse_call(node, writer)
        case ast.Attribute:
            parse_attribute(node, writer)
        case ast.Expr:
            parse_expr(node.value, writer)
        case ast.If:
            parse_if(node, writer)
        case ast.Compare:
            parse_compare(node, writer)
        case ast.IfExp:
            parse_if_exp(node, writer)
        case ast.For:
            parse_for(node, writer)
        case ast.UnaryOp:
            parse_unary_op(node, writer)
        case ast.BoolOp:
            parse_bool_op(node, writer)
        case ast.With:
            parse_with(node, writer)
        case ast.Starred:
            parse_starred(node, writer)
        case ast.Pass:
            pass
        case ast.ClassDef:
            parse_class_def(node, writer)
        case ast.Dict:
            parse_dict(node, writer)
        case ast.Slice:
            parse_slice(node, writer)
        case ast.Match:
            parse_match(node, writer)
        case ast.MatchClass:
            parse_match_class(node, writer)
        case ast.MatchValue:
            parse_match_value(node, writer)
        case ast.MatchAs:
            parse_match_as(node, writer)
        case ast.MatchSequence:
            parse_match_sequence(node, writer)
        case ast.MatchOr:
            parse_match_or(node, writer)
        case ast.Continue:
            parse_continue(node, writer)
        case ast.Break:
            parse_break(node, writer)
        case ast.While:
            parse_while(node, writer)
        case _:
            raise NotImplementedError(f'Unsupported node type {type(node)}')


def gen_exported_defn(node, writer=sys.stdout):
    global fn_return_type, fn_arg_types
    if isinstance(node, ast.FunctionDef):
        array_type = is_array_type(node.returns)
        if array_type:
            # Create a custom struct for the array type
            writer.write(
                f'pub const {node.name}_ret_type = extern struct {{\n')
            writer.write('    ptr: [*c]')
            parse_type_annotation(node.returns, writer, True)
            writer.write(',\n')
            writer.write('    len: usize,\n')
            writer.write('};\n')

        writer.write(f'export fn _{node.name}_zig (')
        arg_types = []
        for arg in node.args.args:
            writer.write(f'{arg.arg}: ')
            parse_type_annotation(arg.annotation, writer)
            arg_types.append(parse_return_type_annotation(arg.annotation))
            writer.write(', ')
        writer.write(') ')
        fn_arg_types[node.name] = arg_types
        if array_type:
            writer.write(f'{node.name}_ret_type')
        else:
            parse_type_annotation(node.returns, writer)

        fn_return_type[node.name] = parse_return_type_annotation(node.returns)
        if array_type:
            class array_type(ctypes.Structure):
                _fields_ = [("ptr", fn_return_type[node.name]),
                            ("len", ctypes.c_uint64)]
            fn_return_type[node.name] = array_type

        writer.write('{\n')
        if array_type:
            # const ret_value = call_fn() catch unreachable;
            # return .{.ptr= ret_value.ptr, .len= ret_value.len};
            writer.write('    const ret_value = ')
            writer.write(f'{node.name} (')
            for arg in node.args.args:
                writer.write(f'{arg.arg}, ')
            if isinstance(node.returns, ast.Subscript):
                writer.write(') catch unreachable;\n')
                # writer.write(
                # ') catch @import("std").debug.dumpCurrentStackTrace(10);\n')
            else:
                writer.write(');\n')
            writer.write(
                '    return .{.ptr= ret_value.ptr, .len= ret_value.len};\n')
        else:
            # return call_fn() catch unreachable;
            writer.write('    return ')
            writer.write(f'{node.name} (')
            for arg in node.args.args:
                writer.write(f'{arg.arg}, ')
            if isinstance(node.returns, ast.Subscript):
                writer.write(') catch unreachable;\n')
                # writer.write(
                # ') catch @import("std").debug.dumpCurrentStackTrace(10);\n')
            else:
                writer.write(');\n')
        writer.write('}\n')
    else:
        raise NotImplementedError(f'Unsupported node type {type(node)}')


def clean():
    if len(compiled_fns) == 0 and len(compiled_classes) == 0:
        # Delete the compiled library
        if os.path.exists('libgenerated.so'):
            os.remove('libgenerated.so')
        if os.path.exists('libgenerated.so.o'):
            os.remove('libgenerated.so.o')
        if os.path.exists('generated.zig'):
            os.remove('generated.zig')


def reload():
    global lib
    if lib:
        dlclose_func = ctypes.cdll.LoadLibrary('').dlclose
        dlclose_func.argtypes = [ctypes.c_void_p]
        handle = lib._handle
        del lib
        dlclose_func(handle)


def compile_lib(output, print_generated=False):
    # Write the generated Zig code to a file
    with open('generated.zig', 'a') as f:
        f.write(output.getvalue())

    # Format the generated Zig code
    result = subprocess.run([sys.executable, '-m', 'ziglang', 'fmt', 'generated.zig'],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Read and print the formatted Zig code
    if print_generated:
        print(result.stdout.decode('utf-8'))
        print(result.stderr.decode('utf-8'))
        with open('generated.zig', 'r') as f:
            print(f.read())

    # Build the generated Zig code using Zig compiler
    subprocess.run([sys.executable, '-m', 'ziglang', 'build-lib',
                    'generated.zig', '-dynamic', '-O', 'ReleaseFast'])


def extract_functions(source):
    tree = ast.parse(source)
    called_funcs = [node.func.id for node in ast.walk(tree) if isinstance(
        node, ast.Call) and isinstance(node.func, ast.Name)]
    return set(called_funcs)


def parse_fn(func, print_generated, export):
    global lib
    clean()
    # If already compiled, return the compiled function
    if func.__name__ in compiled_fns:
        return compiled_fns[func.__name__]

    source_code = inspect.getsource(func)
    called_fns = extract_functions(source_code)
    for called_fn in called_fns:
        if called_fn not in compiled_fns and called_fn in zig_decorated_fns:
            # avoid infinite recursion
            if called_fn == func.__name__:
                continue
            fn_props = zig_decorated_fns[called_fn]
            parse_fn(fn_props[0], fn_props[1], fn_props[2])

    reload()
    tree = ast.parse(source_code)
    funcdef = tree.body[0]
    output = io.StringIO()
    parse_ast(funcdef, output)
    if export:
        gen_exported_defn(funcdef, output)

    compile_lib(output, print_generated)
    # Load the generated Zig static library
    lib = ctypes.CDLL(os.path.join(os.getcwd(), 'libgenerated.so'))
    if export:
        lib_fn = lib[f'_{func.__name__}_zig']

        lib_fn.restype = fn_return_type[func.__name__]
        lib_fn.argtypes = fn_arg_types[func.__name__]

        # Save the compiled function
        compiled_fns[func.__name__] = lib_fn

        # Call the generated Zig function
        return lib_fn
    else:
        compiled_fns[func.__name__] = None
        return None


def zig(print_generated=False, export=True):
    def decorator(func):
        zig_decorated_fns[func.__name__] = (func, print_generated, export)

        def wrapper(*args, **kwargs):
            # check_annotations(func.__annotations__)
            zig_func = parse_fn(func, print_generated, export)
            return zig_func(*args, **kwargs)
        return wrapper
    return decorator


# Zig Struct Decorator
def zig_struct(extern=True):
    def decorator(cls):
        global lib, current_struct_extern
        current_struct_extern = extern
        clean()
        reload()

        source_code = inspect.getsource(cls)
        tree = ast.parse(source_code)
        clsdef = tree.body[0]
        output = io.StringIO()
        parse_ast(clsdef, output)

        compile_lib(output, print_generated=False)

        compiled_classes[cls.__name__] = cls
        return cls
    return decorator


# Zig Enum Decorator
def zig_enum():
    def decorator(cls):
        global current_class_type
        zig_struct(extern=False)(cls)
    return decorator


# Zig Enum Decorator
def zig_error():
    def decorator(cls):
        zig_struct(extern=False)(cls)
    return decorator


# Zig Union Decorator
def zig_union(tag=False):
    def decorator(cls):
        global current_union_tag
        if tag:
            current_union_tag = tag
        zig_struct(extern=False)(cls)
    return decorator
