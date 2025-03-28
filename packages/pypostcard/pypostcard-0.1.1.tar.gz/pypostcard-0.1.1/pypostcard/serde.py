import platform
from dataclasses import fields
from typing import Any, Tuple

if platform.python_implementation() == 'PyPy':
    from .compat import serde, to_postcard, from_postcard, take_from_postcard
else:
    from serde import serde
    from serde.se import Serializer
    from serde.de import Deserializer
    from .types import serialize, deserialize

    class PostcardSerializer(Serializer[str]):
        @classmethod
        def serialize(cls, obj: Any, **opts: Any) -> str:
            serdata = bytearray()
            for field in fields(obj):
                value = getattr(obj, field.name)
                # Ensure the value is of the correct type
                if value is not None:
                    typed_value = field.type(value)
                    data = serialize(field.type, typed_value)
                    if data:
                        serdata.extend(data)
            return bytes(serdata)  # Convert to immutable bytes for consistency

    class PostcardDeserializer(Deserializer[str]):
        @classmethod
        def deserialize(cls, obj: Any, data: bytes, **opts: Any) -> Tuple[Any, int]:
            retval = {}
            index = 0
            for field in fields(obj):
                val, bytes_used = deserialize(field.type, data[index:])
                index += bytes_used
                if val is not None:
                    retval[field.name] = val
            return retval, index

    def to_postcard(
        obj: Any,
        se: type[Serializer[str]] = PostcardSerializer,
        **opts: Any,
    ) -> str:
        """Serialize the object into Postcard."""
        return se.serialize(obj, **opts)

    def from_postcard(
        c: Any, s: bytes, de: type[Deserializer[bytes]] = PostcardDeserializer, **opts: Any
    ) -> Any:
        """Deserialize from Postcard into the object."""
        dict, bytes_used = de.deserialize(c, s, **opts)
        return c(**dict)

    def take_from_postcard(
        c: Any, s: bytes, de: type[Deserializer[bytes]] = PostcardDeserializer, **opts: Any
    ) -> Any:
        """Deserialize from Postcard into the object, return the object and number of bytes used."""
        dict, bytes_used = de.deserialize(c, s, **opts)
        return c(**dict), bytes_used

__all__ = ['serde', 'to_postcard', 'from_postcard', 'take_from_postcard']
