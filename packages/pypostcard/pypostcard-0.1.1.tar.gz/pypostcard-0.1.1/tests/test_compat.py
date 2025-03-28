import platform
import pytest
from dataclasses import dataclass
from pypostcard.compat import serde, to_postcard, from_postcard, take_from_postcard
from pypostcard.types import u8, u16, u32, f32

def get_impl():
    return platform.python_implementation()

@serde
@dataclass
class SimpleMessage:
    value: u8
    flag: bool

@serde
@dataclass
class ComplexMessage:
    small: u8
    medium: u16
    large: u32
    float_val: f32

def test_simple_message_encoding():
    """Test encoding/decoding of a simple message with u8 and bool"""
    msg = SimpleMessage(value=u8(42), flag=True)
    encoded = to_postcard(msg)
    decoded = from_postcard(SimpleMessage, encoded)
    assert decoded.value == 42
    assert decoded.flag == True

def test_complex_message_encoding():
    """Test encoding/decoding of a message with different numeric types"""
    msg = ComplexMessage(
        small=u8(42),
        medium=u16(1000),
        large=u32(100000),
        float_val=f32(3.14159)
    )
    encoded = to_postcard(msg)
    decoded = from_postcard(ComplexMessage, encoded)
    assert decoded.small == 42
    assert decoded.medium == 1000
    assert decoded.large == 100000
    assert abs(decoded.float_val - 3.14159) < 0.00001

def test_partial_message_parsing():
    """Test parsing part of a message and getting size"""
    msg = SimpleMessage(value=u8(42), flag=True)
    encoded = to_postcard(msg)
    decoded, size = take_from_postcard(SimpleMessage, encoded)
    assert decoded.value == 42
    assert decoded.flag == True
    assert size == 2  # 1 byte for u8, 1 byte for bool

def test_implementation_specific():
    """Test that the implementation matches the Python version"""
    impl = get_impl()
    if impl == 'PyPy':
        # Verify we're using our custom implementation
        assert serde.__module__ == 'pypostcard.compat'
    else:
        # Verify we're using pyserde
        assert serde.__module__ == 'serde' 