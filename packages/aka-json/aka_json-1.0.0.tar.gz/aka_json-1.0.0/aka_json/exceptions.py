"""
# exceptions.py Module Summary

Defines custom exception classes for handling file-related errors.

    Raises:
        FileExtensionError: When an incorrect or missing file extension is encountered.
        FileOpenError: When attempting to open or close a file that is already in that state.
        FileCorruptError: When the file content is detected as corrupted or invalid.
        ContentTypeError: When an attempt is made to write an incompatible content type to a file.
"""


class FileExtensionError(Exception):
    """It is usually raise when an incorrect file extension is passed or missing."""


class FileOpenError(Exception):
    """It is usually raise when a file is already open or already closed."""


class FileCorruptError(Exception):
    """It is usually raise when the file content is corrupted."""


class ContentTypeError(Exception):
    """It is usually raise when writing an incorrect content type to a file."""
