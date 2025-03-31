"""
# encoder.py Module Summary

This module defines a custom JSON encoder (`JsonEncoder`) that extends the standard `JSONEncoder`. Its purpose is to enable the serialization of `datetime`, `date`, `time`, and `bytes` objects into a JSON-compatible format. This is achieved by overriding the `default()` method to detect these specific types. `datetime`, `date`, and `time` objects are converted to ISO format strings. `bytes` objects are converted to base64-encoded strings.  This allows the `json` module to correctly handle these types when writing JSON files. The custom decoder (`decoder.py`) is required to properly read these files back.
"""

from datetime import datetime, date, time
from json import JSONEncoder
from typing import Any
import base64


class JsonEncoder(JSONEncoder):
    """
    Custom JSON encoder to handle datetime, date, time, and bytes objects.

    This encoder extends the standard JSONEncoder to serialize these types
    into a JSON-compatible format. Datetime, date, and time objects are
    serialized into ISO format strings, and bytes objects are serialized
    into base64-encoded strings.
    """

    def default(self, obj):
        """
        Overrides the default method of JSONEncoder to handle specific object types.

        Args:
            obj: The object to be encoded.

        Returns:
            A JSON-serializable representation of the object, or calls the superclass's
            default method if the object type is not handled.
        """

        if isinstance(obj, (datetime, date, time)):
            return {"__datetime__": True, "iso": obj.isoformat()}

        elif isinstance(obj, bytes):
            return {"__bytes__": True, "base64": base64.b64encode(obj).decode('utf-8')}

        return super().default(obj)
