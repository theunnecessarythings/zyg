# Zig-Python Experimental Integration

This repository is an **experimental project** that integrates Python with Zig. It transpiles annotated Python code into Zig, compiles it as a dynamic library, and executes it from Python for performance gains.

## Overview

- **Transpilation:** Use Python decorators (e.g., `@zig`, `@zig_struct`) to mark functions and types for conversion.
- **Dynamic Compilation:** Automatically generate and compile Zig code to a dynamic library, then load it via ctypes.
- **Benchmarks:** Includes examples like matrix multiplication comparing Python vs. Zig performance.

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/theunnecessarythings/zyg
   cd zyg
   ```

2. **Install Dependencies:**
   Only dependency is zig itself. Use `uv` to install it.

## Usage

```python
@zig_struct(extern=False)
class MatrixZig(ZigStruct):
    value: Slice[f64]
    rows: usize
    cols: usize

@zig()
def matmul_zig(C: Ptr[MatrixZig], A: Ptr[MatrixZig], B: Ptr[MatrixZig]) -> void:
    # Zig-style matrix multiplication
```

Calling these functions will automatically transpile, compile, and run the generated Zig code.

## Note

This is an **experimental project**—expect rapid changes and limited error handling. Contributions and feedback are welcome!

## License

MIT License.
