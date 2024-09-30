import ctypes


class MyStruct(ctypes.Structure):
    _fields_ = [("a", ctypes.c_int),  # Map Zig's i32 to ctypes.c_int
                ("b", ctypes.c_int)]


def main():
    lib = ctypes.CDLL("./libtest.so")
    returning_list = lib.returning_list
    returning_list.restype = ctypes.POINTER(ctypes.c_long)
    returning_list.argtypes = []
    lis = returning_list()

    for i in range(3):
        print(lis[i])

    returning_structs = lib.returning_structs
    returning_structs.restype = ctypes.POINTER(MyStruct)
    returning_structs.argtypes = []
    structs = returning_structs()

    for i in range(3):
        print(structs[i].a, structs[i].b)


if __name__ == "__main__":
    main()
