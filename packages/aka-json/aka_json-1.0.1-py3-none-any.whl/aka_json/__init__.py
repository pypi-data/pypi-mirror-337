"""
# json_file_handler Module Summary

This module provides a comprehensive set of tools for reading and writing JSON and JSON5 files.  It's designed to simplify file handling and offers features like:

*   **Custom Encoders and Decoders:**  Provides custom JSON encoders and decoders (`JsonEncoder`, `JsonDecoder`) to handle datetime objects (serializing to and deserializing from ISO format strings) and bytes objects (serializing to and deserializing from base64-encoded strings).
*   **Core File Handling Classes:** Offers base classes (`SimpleJsonFile`, `SimpleJson5File`) to handle fundamental file operations (open, close, read, write, create, remove) for both standard JSON and JSON5 formats.
*   **Dataclass Support:**  Includes derived classes (`JsonFile`, `Json5File`) that extend the base classes and provide seamless integration with Python dataclasses. This allows users to read and write complex data structures directly to and from JSON/JSON5 files using dataclass definitions.
*   **JSON5 Support:** Implements support for the JSON5 data format using the `json5` library via `SimpleJson5File` and `Json5File` classes.
*   **Flexible Configuration:** Allows users to specify content type (dictionary or list), encoding (UTF-8, ASCII, etc.), indentation, and other formatting options.
*   **Error Handling:** Leverages custom exception classes (defined in `.exceptions`) to provide more informative error messages.
*   **Constants:** Defines various constants (content types, file modes, codings, and file extensions) in the `.constants` module for improved code clarity, maintainability, and to reduce errors.

**Module Structure:**

*   **`exceptions.py`:**  Defines custom exception classes for specific error scenarios (e.g., `FileExtensionError`, `ContentTypeError`, `FileNotFoundError`, `FileOpenError`).  These provide more detailed error handling.
*   **`encoder.py`:**  Contains the `JsonEncoder` class, which extends `json.JSONEncoder` to handle `datetime`, `date`, `time`, and `bytes` objects during serialization, allowing their proper encoding to JSON.
*   **`decoder.py`:** Contains the `JsonDecoder` class, which extends `json.JSONDecoder` and uses an `object_hook` to deserialize datetime and bytes objects during deserialization.
*   **`constants.py`:**  Defines the `ContentType`, `FileMode`, `Coding`, and `Constants` classes to hold all constants used by the library.
*   **`file.py`:**  This assumed file defines the core file handling classes, including:
    *   `SimpleJsonFile`:  Base class for general JSON file handling.
    *   `JsonFile`:  Extends `SimpleJsonFile` with dataclass support.
    *   `SimpleJson5File`: Base class for general JSON5 file handling.
    *   `Json5File`: Extends `SimpleJson5File` with dataclass support.
*   **`__init__.py`:** (This file) Imports the required parts for easy use via a single `import` statement. This is an example of this. `from .exceptions import *`, `from .constants import ContentType, FileMode, Coding, Constants`, `from .file import SimpleJsonFile, JsonFile, SimpleJson5File, Json5File`.

**Overall, this module provides a robust and convenient way to manage JSON and JSON5 files, with a focus on ease of use, type safety, and extensibility.**
"""

# Import module parts
from .exceptions import *
from .constants import ContentType, FileMode, Coding, Constants
from .file import SimpleJsonFile, JsonFile, SimpleJson5File, Json5File
