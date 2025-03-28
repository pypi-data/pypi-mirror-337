import platform
import struct
import dataclasses
from typing import Any, Type, TypeVar, Tuple

T = TypeVar('T')

# PyPy compatibility layer
if platform.python_implementation() == 'PyPy':
    def serde(cls):
        """Simple decorator for PyPy compatibility that just uses dataclass"""
        return dataclasses.dataclass(cls)

    def to_postcard(obj: Any) -> bytes:
        """Binary serialization for PyPy that matches postcard format"""
        if dataclasses.is_dataclass(obj):
            data = bytearray()
            for field in dataclasses.fields(obj):
                value = getattr(obj, field.name)
                if isinstance(value, int):
                    if field.type.__name__ == 'u8':
                        data.extend(struct.pack('<B', value))
                    elif field.type.__name__ == 'u16':
                        data.extend(struct.pack('<H', value))
                    elif field.type.__name__ == 'u32':
                        data.extend(struct.pack('<I', value))
                    else:
                        data.extend(struct.pack('<I', value))
                elif isinstance(value, float):
                    data.extend(struct.pack('<f', value))
                elif isinstance(value, bool):
                    data.extend(struct.pack('<?', value))
            return bytes(data)
        return bytes(obj)

    def from_postcard(cls: Type[T], data: bytes) -> T:
        """Binary deserialization for PyPy that matches postcard format"""
        if not dataclasses.is_dataclass(cls):
            return cls(data)
            
        values = {}
        offset = 0
        for field in dataclasses.fields(cls):
            if field.type.__name__ == 'u8':
                values[field.name], = struct.unpack('<B', data[offset:offset+1])
                offset += 1
            elif field.type.__name__ == 'u16':
                values[field.name], = struct.unpack('<H', data[offset:offset+2])
                offset += 2
            elif field.type.__name__ == 'u32':
                values[field.name], = struct.unpack('<I', data[offset:offset+4])
                offset += 4
            elif field.type.__name__ == 'f32':
                values[field.name], = struct.unpack('<f', data[offset:offset+4])
                offset += 4
            elif field.type == bool:
                values[field.name], = struct.unpack('<?', data[offset:offset+1])
                offset += 1
        return cls(**values)

    def take_from_postcard(cls: Type[T], data: bytes) -> Tuple[T, int]:
        """Parse partial data and return object with bytes consumed"""
        obj = from_postcard(cls, data)
        size = 0
        for field in dataclasses.fields(cls):
            if field.type.__name__ == 'u8':
                size += 1
            elif field.type.__name__ == 'u16':
                size += 2
            elif field.type.__name__ == 'u32' or field.type.__name__ == 'f32':
                size += 4
            elif field.type == bool:
                size += 1
        return obj, size
else:
    from serde import serde
    from pypostcard.serde import to_postcard, from_postcard, take_from_postcard

# Export for use by other modules
__all__ = ['serde', 'to_postcard', 'from_postcard', 'take_from_postcard']
