"""
# decoder.py Module Summary

This module defines a custom JSON decoder (`JsonDecoder`) that extends the standard `JSONDecoder`. Its purpose is to correctly deserialize `datetime` and `bytes` objects that were serialized by the corresponding custom encoder (`encoder.py`). It uses an `object_hook` to identify specially-formatted dictionaries representing datetimes (identified by the "__datetime__" key) and bytes (identified by the "__bytes__" key) and convert them back to their original types using `datetime.fromisoformat()` and `base64.b64decode()`, respectively.  This allows proper reading of JSON files that contain these data types.
"""

from typing import Any
from json import JSONDecoder
from datetime import datetime
import base64


class JsonDecoder(JSONDecoder):
    """
    Custom JSON decoder to handle datetime and bytes objects.

    This decoder extends the standard JSONDecoder to deserialize datetime
    objects from ISO format strings and bytes objects from base64-encoded strings.
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes the JsonDecoder with a custom object hook.

        Args:
            *args: Positional arguments passed to the superclass constructor.
            **kwargs: Keyword arguments passed to the superclass constructor.
        """

        kwargs["object_hook"] = self.object_hook
        super().__init__(*args, **kwargs)
    
    def object_hook(self, obj: Any):
        """
        Custom object hook to deserialize datetime and bytes objects.

        Args:
            obj (Any): The object to be deserialized.

        Returns:
            The deserialized object, or the original object if it's not a datetime or bytes type.
        """

        if isinstance(obj, dict):
            if "__datetime__" in obj and obj["__datetime__"]:
                return datetime.fromisoformat(obj["iso"])
            elif "__bytes__" in obj and obj["__bytes__"]:
                return base64.b64decode(obj["base64"])
        return obj
