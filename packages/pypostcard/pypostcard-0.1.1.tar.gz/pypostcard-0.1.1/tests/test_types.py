import enum
from pypostcard.types import (
    Enum,
    List,
    deserialize,
    f32,
    f64,
    i16,
    i8,
    serialize,
    u16,
    u8,
)
import pytest


class EnumType(enum.Enum):
    A = 1
    B = 2
    C = 3


@pytest.mark.parametrize(
    "postcard_type,raw,postcard",
    [
        (u8, 0, [0x00]),
        (u8, 127, [0x7F]),
        (u8, 254, [0xFE]),
        (u8, 255, [0xFF]),
        (i8, 0, [0x00]),
        (i8, -1, [0xFF]),
        (i8, 1, [0x01]),
        (i8, 63, [0x3F]),
        (i8, -64, [0xC0]),
        (i8, 64, [0x40]),
        (i8, -65, [0xBF]),
        (u16, 0, [0x00]),
        (u16, 127, [0x7F]),
        (u16, 128, [0x80, 0x01]),
        (u16, 16383, [0xFF, 0x7F]),
        (u16, 16384, [0x80, 0x80, 0x01]),
        (u16, 16385, [0x81, 0x80, 0x01]),
        (u16, 65535, [0xFF, 0xFF, 0x03]),
        (i16, 0, [0x00]),
        (i16, -1, [0x01]),
        (i16, 1, [0x02]),
        (i16, 63, [0x7E]),
        (i16, -64, [0x7F]),
        (i16, 64, [0x80, 0x01]),
        (i16, -65, [0x81, 0x01]),
        (i16, 32767, [0xFE, 0xFF, 0x03]),
        (i16, -32768, [0xFF, 0xFF, 0x03]),
        (bool, False, [0x00]),
        (bool, True, [0x01]),
        (List[u8, 3], [1, 2, 3], [0x01, 0x02, 0x03]),
        (List[u16, 3], [1, 128, 3], [0x01, 0x80, 0x01, 0x03]),
        (f32, 0.0, [0x00, 0x00, 0x00, 0x00]),
        (f32, -32.005859375, [0x00, 0x06, 0x00, 0xC2]),
        (f64, 0.0, [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]),
        (f64, -32.005859375, [0x00, 0x00, 0x00, 0x00, 0xC0, 0x00, 0x40, 0xC0]),
        (Enum[u8, EnumType], EnumType.A, [0x01]),
        (Enum[u8, EnumType], EnumType.B, [0x02]),
        (Enum[u8, EnumType], EnumType.C, [0x03]),
    ],
)
class TestClass:
    def test_serialize(self, postcard_type, raw, postcard):
        serialized = serialize(postcard_type, postcard_type(raw))
        assert [x for x in serialized] == postcard

    def test_deserialize(self, postcard_type, raw, postcard):
        deserialized, bytes_used = deserialize(postcard_type, bytes(postcard))
        assert deserialized == raw
        assert len(postcard) == bytes_used
