# PyPostcard

Python implementation of the postcard serialization format.

## Installation

### Using uv (recommended)

```bash
uv pip install .
```

The package automatically detects your Python implementation and installs the appropriate dependencies:
- On CPython: Installs with pyserde for efficient serialization
- On PyPy: Uses a custom optimized implementation

### Development Installation

Install in editable mode:
```bash
uv pip install -e .
```

## Implementation Details

The library automatically detects whether you're using CPython or PyPy and uses the appropriate implementation:
- On CPython: Uses `pyserde` for efficient serialization/deserialization
- On PyPy: Uses a custom implementation optimized for PyPy
