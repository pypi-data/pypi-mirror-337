import platform
import pytest
from pypostcard.serde import from_postcard, to_postcard
from pypostcard.types import List, i16, i8, u16, u8

pytestmark = pytest.mark.skipif(
    platform.python_implementation() == "PyPy",
    reason="serde tests only run on CPython"
)

if platform.python_implementation() != "PyPy":
    from serde import serde

    @serde
    class Foo:
        a: u8
        b: i8
        c: u16
        d: i16
        e: List[u8, 3]
else:
    Foo = None  # Placeholder for PyPy

@pytest.mark.skipif(platform.python_implementation() == "PyPy", reason="serde tests only run on CPython")
def test_serde_serialize():
    test = Foo(a=u8(1), b=i8(2), c=u16(3), d=i16(4), e=List(5, 6, 7))
    postcard = to_postcard(test)
    assert postcard == b"\x01\x02\x03\x08\x05\x06\x07"

@pytest.mark.skipif(platform.python_implementation() == "PyPy", reason="serde tests only run on CPython")
def test_serde_deserialize():
    postcard = b"\x01\x02\x03\x08\x05\x06\x07"
    test = Foo(a=u8(1), b=i8(2), c=u16(3), d=i16(4), e=List(5, 6, 7))
    assert from_postcard(Foo, postcard) == test
