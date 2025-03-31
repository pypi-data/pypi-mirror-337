"""
# constants.py Module Summary

This module defines a set of constants used throughout the `json_file_handler` library to promote code readability, maintainability, and prevent errors caused by inconsistent string literals. It defines constants for:

*   **Content Types:** (`ContentType`) Defines the expected structure of JSON files (dictionary or list).
*   **File Modes:** (`FileMode`) Defines file opening modes for reading, writing, appending, and binary operations.
*   **Text Encodings:** (`Coding`) Specifies common text encodings (UTF-8, ASCII, etc.) for reading and writing JSON files.
*   **File Extensions:** Defines the file extensions for JSON and JSON5 files.

The `Constants` class aggregates these constants for easier access and organization.
"""


class ContentType:
    """
    Defines constants for content types supported by the JSON file handler.

    These constants represent the expected structure of the JSON file,
    either as a dictionary (`DICT`) or a list (`LIST`).
    """

    DICT = "DictMode"
    LIST = "ListMode"


class FileMode:
    """
    Defines constants for file modes used when opening JSON files.

    These constants map to standard file mode strings used in Python's `open()` function.
    Includes read, write, append, and combinations thereof, for both text and binary modes.
    """

    READ = "r"
    WRITE = "w"
    READ_BINARY = "rb"
    WRITE_BINARY = "wb"
    READ_WRITE = "r+"
    READ_WRITE_BINARY = "rb+"
    READ_WRITE_NEW = "w+"
    READ_WRITE_BINARY_NEW = "wb+"
    APPEND = "a"
    READ_WRITE_APPEND = "a+"
    APPEND_BINARY = "ab"
    READ_WRITE_APPEND_BINARY = "ab+"


class Coding:
    """
    Defines constants for various text encodings supported by the JSON file handler.

    These constants represent common text encodings that can be used when
    reading and writing JSON files.  Allows specifying different character sets
    to handle files with different encoding schemes.
    """

    UTF8: str = "utf-8"
    UTF16: str = "utf-16"
    ASCII: str = "ascii"
    ISO8859_1: str = "latin-1"
    WINDOWS1252: str = "windows-1252"
    GBK: str = "gbk"
    GB2312: str = "gb2312"
    BIG5: str = "big5"
    SHIFT_JIS: str = "shift_jis"
    KOI8: str = "koi8"
    CP866: str = "cp866"
    ANSI: str = "ansi"


class Constants:
    """
    Groups all constants used in the JSON file handler.

    This class serves as a central repository for all constant values used
    throughout the library.  It includes nested classes for `ContentType`,
    `FileMode`, and `Coding`, as well as constants for file extensions (`JSON_EXTENSION` and `JSON5_EXTENSION`).
    """

    CONTENT_TYPE: ContentType = ContentType
    FILE_MODE: FileMode = FileMode
    CODING: Coding = Coding

    JSON_EXTENSION: str = ".json"
    JSON5_EXTENSION: str = ".json5"
