"""
# file.py Module Summary

This module provides classes for handling JSON and JSON5 files, offering robust read/write operations, dataclass integration, and configurable formatting. Key components include:

*   **Core Classes:**
    - `SimpleJsonFile`/`SimpleJson5File`: Base classes for basic JSON/JSON5 operations (open, read, write, create, delete).
    - `JsonFile`/`Json5File`: Extended classes with dataclass support for automatic object serialization/deserialization.

*   **Features:**
    - **Dataclass Integration:** Convert JSON data to/from Python dataclass objects using `dacite`.
    - **Format Control:** Customize indentation, ASCII encoding, key sorting, and content type (dict/list).
    - **Validation:** Enforce file extensions (`.json`), content type checks, and error handling for common file operations.
    - **JSON5 Support:** Leverage `json5` library for relaxed JSON syntax parsing.

*   **Constants & Configuration:**
    - `ContentType`: Enforces expected JSON structure (dictionary or list).
    - `FileMode`: Standardizes file opening modes (read/write/append).
    - `Coding`: Defines text encodings (UTF-8, ASCII).
    - Custom encoders/decoders (`JsonEncoder`, `JsonDecoder`) for enhanced serialization.

Designed for reliability and maintainability, with context manager support and explicit error handling via custom exceptions.
"""

# Import modules
from .exceptions import *
from dacite import from_dict
from .encoder import JsonEncoder
from .decoder import JsonDecoder
from dataclasses import is_dataclass, asdict
from typing import TextIO, Union, Optional, Type, TypeVar
from .constants import Constants, FileMode, ContentType, Coding
import os
import json
import json5

# Set TypeVar
T = TypeVar("T")


# Json classes
class SimpleJsonFile:
    """
    A simple class for reading and writing JSON files.

    Handles basic file operations like opening, closing, reading, writing,
    creating, and removing files. Supports specifying content type (dict or list),
    coding, indentation, and sorting keys.
    """

    _path: str
    _name: str
    _extension: str

    _content_type: str
    _coding: str
    _indent: int
    _ensure_ascii: bool
    _sort_keys: bool

    _file: Optional[TextIO]
    _content: Optional[Union[dict, list]]

    _is_exists: bool
    _is_opened: bool
    _is_empty: bool

    def __init__(self, file_path: str, content_type: str = ContentType.DICT, *,
                 coding: str = Coding.UTF8, auto_load: bool = False, indent: int = 2,
                 ensure_ascii: bool = False, sort_keys: bool = False, create_file: bool = False,
                 default_content: Optional[Union[dict, list]] = None) -> None:
        """
        Initializes a SimpleJsonFile object.

        Args:
            file_path (str): The path to the JSON file.
            content_type (str, optional): The expected content type of the file (dict or list). Defaults to ContentType.DICT.
            coding (str, optional): The file encoding. Defaults to Coding.UTF8.
            auto_load (bool, optional): Whether to automatically load the file content upon initialization. Defaults to False.
            indent (int, optional): The indentation level for JSON formatting. Defaults to 2.
            ensure_ascii (bool, optional): Whether to ensure ASCII characters in the JSON output. Defaults to False.
            sort_keys (bool, optional): Whether to sort the keys in the JSON output. Defaults to False.
            create_file (bool, optional): Whether to create the file if it doesn't exist. Defaults to False.
            default_content (Optional[Union[dict, list]], optional): Default content to write to the file if it's created. Defaults to None.
        """

        self._path = os.path.normpath(file_path)
        self._name = os.path.basename(self._path)
        self._extension = Constants.JSON_EXTENSION
        
        self._content_type = content_type
        self.__check_content_type()

        self._coding = coding
        self.__check_extension()

        self._ensure_ascii = ensure_ascii
        self._indent = indent
        self._sort_keys = sort_keys

        self._file = None
        self._content = None

        self._is_exists = False
        self._is_opened = False
        self._is_empty = True

        if create_file:
            self.new(True, default_content)

        self._is_exists = self.__is_exists()

        if auto_load and self._is_exists:
            self.open()
            self._content = self.read()
            self.close()

        self._is_opened = self.__is_opened()
        self._is_empty = self.__is_empty()

    def __call__(self) -> Optional[Union[dict, list]]:
        return self.read()

    def __str__(self) -> str:
        if self._content is None:
            return "N/A"

        return json.dumps(self._content, cls=JsonEncoder, indent=self._indent, ensure_ascii=self._ensure_ascii, sort_keys=self._sort_keys)

    def __enter__(self) -> "SimpleJsonFile":
        self.open(create_file=True)
        return self
    
    def __exit__(self, *args) -> None:
        self.close()

    def __check_extension(self) -> None:
        """"""

        if not self._name.endswith(Constants.JSON_EXTENSION):
            current_extension = os.path.splitext(self._name)[1]
            expected_extension = Constants.JSON_EXTENSION
            raise FileExtensionError(f"File {self._path} has incorrect extension. Expected: {expected_extension} - Recieved: {current_extension}.")

    def __check_content_type(self) -> None:
        """"""

        content_types = ContentType.__dict__.values()

        if not self._content_type in content_types:
            raise ContentTypeError(f"Invalid content type. Expected: {content_types} - Recieved: {self._content_type}.")

    def __is_exists(self) -> bool:
        """"""

        return os.path.exists(self._path)

    def __is_opened(self) -> bool:
        """"""

        return self._file is not None

    def __is_empty(self) -> bool:
        """"""

        if self._is_exists and self._is_opened and self._content:
            return len(self._content) == 0
        return False

    def set_options(self, content_type: str = ContentType.DICT, *, coding: str = Coding.UTF8, indent: int = 2,
                    ensure_ascii: bool = False, sort_keys: bool = False) -> None:
        """
        Sets the options for the JSON file.

        Args:
            content_type (str, optional): The content type of the file (dict or list). Defaults to ContentType.DICT.
            coding (str, optional): The file encoding. Defaults to Coding.UTF8.
            indent (int, optional): The indentation level for JSON formatting. Defaults to 2.
            ensure_ascii (bool, optional): Whether to ensure ASCII characters in the JSON output. Defaults to False.
            sort_keys (bool, optional): Whether to sort the keys in the JSON output. Defaults to False.
        """

        self._content_type = content_type
        self.__check_content_type()

        self._coding = coding
        self.__check_extension()

        self._ensure_ascii = ensure_ascii
        self._indent = indent
        self._sort_keys = sort_keys

    def open(self, *, create_file: bool = False) -> TextIO:
        """
        Opens the JSON file.

        Args:
            create_file (bool, optional): Whether to create the file if it doesn't exist. Defaults to False.

        Returns:
            TextIO: The file object.

        Raises:
            FileNotFoundError: If the file is not found.
            FileOpenError: If the file is already open.
        """
        
        if create_file:
            self.new()

        if not self._is_exists:
            raise FileNotFoundError(f"File {self._path} is not found.")

        if self._file and self._is_opened:
            raise FileOpenError(f"File {self._path} is already open.")
            
        self._file = open(self._path, FileMode.READ_WRITE, encoding=self._coding)
        self._is_opened = self.__is_opened()

    def close(self, *, remove_file: bool = False) -> None:
        """
        Closes the JSON file.

        Args:
            remove_file (bool, optional): Whether to remove the file after closing. Defaults to False.

        Raises:
            FileOpenError: If the file is already closed.
        """

        if not self._file and not self._is_opened:
            raise FileOpenError(f"File {self._path} is already closed.")

        self._file.close()
        self._file = None
        self._is_opened = self.__is_opened()

        if remove_file:
            self.remove()

    def new(self, replace_file: bool = False,
            default_content: Optional[Union[dict, list]] = None) -> None:
        """
        Creates a new JSON file.

        Args:
            replace_file (bool, optional): Whether to replace the file if it already exists. Defaults to False.
            default_content (Optional[Union[dict, list]], optional): Default content to write to the file. Defaults to None.
        """

        if not self._is_exists or replace_file:
            with open(self._path, FileMode.READ_WRITE_NEW, encoding=self._coding) as new_file:
                new_file.write("{}" if self._content_type == ContentType.DICT else "[]")
                self._is_exists = self.__is_exists()

            if default_content:
                if self._content_type == ContentType.LIST:
                    self.write([default_content])

                elif self._content_type == ContentType.DICT:
                    self.write(default_content)

    def remove(self) -> None:
        """
        Removes the JSON file.

        Raises:
            FileNotFoundError: If the file is not found.
            FileOpenError: If the file is currently open.
        """

        if not self._is_exists:
            raise FileNotFoundError(f"File {self._path} is not found.")
        
        if self._is_opened:
            raise FileOpenError(f"File {self._path} is opened")

        os.remove(self._path)
        self._is_exists = self.__is_exists()

    def read(self) -> Union[dict, list]:
        """
        Reads the content of the JSON file.

        Returns:
            Union[dict, list]: The content of the JSON file as a dictionary or a list.

        Raises:
            FileNotFoundError: If the file is not found.
            FileOpenError: If the file is not opened.
        """

        if not self._is_exists:
            raise FileNotFoundError(f"File {self._path} is not found.")
        
        if not self._is_opened:
            raise FileOpenError(f"File {self._path} is not opened.")

        self._file.seek(0)
        read_data = json.load(self._file, cls=JsonDecoder)
        self._content = read_data
        return read_data         

    def write(self, content: Optional[Union[dict, list]] = None) -> None:
        """
        Writes content to the JSON file.

        Args:
            content (Optional[Union[dict, list]], optional): The content to write to the file. Defaults to None (writes the current content).

        Raises:
            FileNotFoundError: If the file is not found.
            FileOpenError: If the file is not opened or if there is an error writing to the file.
        """

        if not self._is_exists:
            raise FileNotFoundError(f"File {self._path} is not found.")

        if not self._is_opened:
            raise FileOpenError(f"File {self._path} is not opened.")
        
        if content is None:
            content = self._content

        try:
            self._file.seek(0)
            self._file.truncate()
            json.dump(content, self._file, cls=JsonEncoder, indent=self._indent, ensure_ascii=self._ensure_ascii, sort_keys=self._sort_keys)
            self._file.flush()

            self._content = content

            self._is_empty = self.__is_empty()

        except Exception as exception:
             raise FileOpenError(f"Error writing to the {self._path} file: {exception}") from exception

    def clear(self) -> None:
        """
        Clears the content of the JSON file (writes an empty dictionary or list).
        """

        if self._content_type == ContentType.DICT:
            self.write({})
        else:
            self.write([])

    def get_size(self) -> int:
        """
        Gets the size of the JSON file content.

        Returns:
            int: The number of elements in the JSON content (length of the dictionary or list).
        """

        if self._content is None:
            return 0
        return len(self._content)


class JsonFile(SimpleJsonFile):
    """
    A class for reading and writing JSON files, extending SimpleJsonFile with dataclass support.

    Allows reading the file content directly into dataclass objects and writing
    dataclass objects to the file.
    """

    def __init__(self, file_path: str, content_type: str = ContentType.DICT, *,
                 coding: str = Coding.UTF8, auto_load: bool = False, indent: int = 2,
                 ensure_ascii: bool = False, sort_keys: bool = False, create_file: bool = False,
                 default_content: Optional[Union[dict, list]] = None) -> None:
        """
        Initializes a JsonFile object.

        Args:
            file_path (str): The path to the JSON file.
            content_type (str, optional): The expected content type of the file (dict or list). Defaults to ContentType.DICT.
            coding (str, optional): The file encoding. Defaults to Coding.UTF8.
            auto_load (bool, optional): Whether to automatically load the file content upon initialization. Defaults to False.
            indent (int, optional): The indentation level for JSON formatting. Defaults to 2.
            ensure_ascii (bool, optional): Whether to ensure ASCII characters in the JSON output. Defaults to False.
            sort_keys (bool, optional): Whether to sort the keys in the JSON output. Defaults to False.
            create_file (bool, optional): Whether to create the file if it doesn't exist. Defaults to False.
            default_content (Optional[Union[dict, list]], optional): Default content to write to the file if it's created. Defaults to None.
        """

        super().__init__(file_path, content_type, coding=coding, auto_load=auto_load,
                         indent=indent, ensure_ascii=ensure_ascii, sort_keys=sort_keys,
                         create_file=create_file, default_content=default_content)

    def __enter__(self) -> "JsonFile":
        self.open(create_file=True)
        return self
    
    def __exit__(self, *args) -> None:
        self.close()

    def read_as_dataclass(self, dataclass: Type[T]) -> T | list[T]:
        """
        Reads the JSON file content and converts it into a dataclass object or a list of dataclass objects.

        Args:
            dataclass (Type[T]): The dataclass type to convert the JSON content into.

        Returns:
            T | list[T]: A dataclass object or a list of dataclass objects.
        """

        data = self.read()

        if isinstance(data, list):
            return [from_dict(dataclass, item) for item in data]

        return from_dict(dataclass, data)

    def write(self, content: Optional[Union[dict, list, Type[T]]] = None) -> None:
        """
        Writes content to the JSON file, handling dataclass objects.

        If the content is a dataclass object or a list of dataclass objects, it will be converted to a dictionary before writing.

        Args:
            content (Optional[Union[dict, list, Type[T]]], optional): The content to write to the file. Defaults to None (writes the current content).
        """

        if content is None:
            content = self._content

        if isinstance(content, list):
            items = []
            for item in content:
                if is_dataclass(item):
                    item = asdict(item)
            content = items

        elif is_dataclass(content):
            content = asdict(content)
            json.dump(content, self._file, cls=JsonEncoder, indent=self._indent, ensure_ascii=self._ensure_ascii, sort_keys=self._sort_keys)
            self._content = content


# Json5 classes
class SimpleJson5File:
    """
    A simple class for reading and writing JSON5 files.

    Handles basic file operations like opening, closing, reading, writing,
    creating, and removing files. Supports specifying content type (dict or list),
    coding, indentation, and sorting keys. Uses the `json5` library for JSON5 support.
    """

    _path: str
    _name: str
    _extension: str

    _content_type: str
    _coding: str
    _indent: int
    _ensure_ascii: bool
    _sort_keys: bool

    _file: Optional[TextIO]
    _content: Optional[Union[dict, list]]

    _is_exists: bool
    _is_opened: bool
    _is_empty: bool

    def __init__(self, file_path: str, content_type: str = ContentType.DICT, *,
                 coding: str = Coding.UTF8, auto_load: bool = False, indent: int = 2,
                 ensure_ascii: bool = False, sort_keys: bool = False,
                 create_file: bool = False, default_content: Optional[Union[dict, list]] = None) -> None:
        """
        Initializes a SimpleJson5File object.

        Args:
            file_path (str): The path to the JSON5 file.
            content_type (str, optional): The expected content type of the file (dict or list). Defaults to ContentType.DICT.
            coding (str, optional): The file encoding. Defaults to Coding.UTF8.
            auto_load (bool, optional): Whether to automatically load the file content upon initialization. Defaults to False.
            indent (int, optional): The indentation level for JSON formatting. Defaults to 2.
            ensure_ascii (bool, optional): Whether to ensure ASCII characters in the JSON output. Defaults to False.
            sort_keys (bool, optional): Whether to sort the keys in the JSON output. Defaults to False.
            create_file (bool, optional): Whether to create the file if it doesn't exist. Defaults to False.
            default_content (Optional[Union[dict, list]], optional): Default content to write to the file if it's created. Defaults to None.
        """

        self._path = os.path.normpath(file_path)
        self._name = os.path.basename(self._path)
        self._extension = Constants.JSON_EXTENSION
        
        self._content_type = content_type
        self.__check_content_type()

        self._coding = coding
        self.__check_extension()

        self._ensure_ascii = ensure_ascii
        self._indent = indent
        self._sort_keys = sort_keys

        self._file = None
        self._content = None

        self._is_exists = False
        self._is_opened = False
        self._is_empty = True

        if create_file:
            self.new(True, default_content)

        self._is_exists = self.__is_exists()

        if auto_load and self._is_exists:
            self.open()
            self._content = self.read()
            self.close()

        self._is_opened = self.__is_opened()
        self._is_empty = self.__is_empty()

    def __call__(self) -> Optional[Union[dict, list]]:
        return self.read()

    def __str__(self) -> str:
        if self._content is None:
            return "N/A"

        return json5.dumps(self._content, cls=JsonEncoder, indent=self._indent, ensure_ascii=self._ensure_ascii, sort_keys=self._sort_keys)

    def __enter__(self) -> "SimpleJson5File":
        self.open(create_file=True)
        return self
    
    def __exit__(self, *args) -> None:
        self.close()

    def __check_extension(self) -> None:
        """"""

        if not self._name.endswith(Constants.JSON_EXTENSION):
            current_extension = os.path.splitext(self._name)[1]
            expected_extension = Constants.JSON_EXTENSION
            raise FileExtensionError(f"File {self._path} has incorrect extension. Expected: {expected_extension} - Recieved: {current_extension}.")

    def __check_content_type(self) -> None:
        """"""

        content_types = ContentType.__dict__.values()

        if not self._content_type in content_types:
            raise ContentTypeError(f"Invalid content type. Expected: {content_types} - Recieved: {self._content_type}.")

    def __is_exists(self) -> bool:
        """"""

        return os.path.exists(self._path)

    def __is_opened(self) -> bool:
        """"""

        return self._file is not None

    def __is_empty(self) -> bool:
        """"""

        if self._is_exists and self._is_opened and self._content:
            return len(self._content) == 0
        return False

    def set_options(self, content_type: str = ContentType.DICT, *, coding: str = Coding.UTF8, indent: int = 2,
                    ensure_ascii: bool = False, sort_keys: bool = False) -> None:
        """
        Sets the options for the JSON5 file.

        Args:
            content_type (str, optional): The content type of the file (dict or list). Defaults to ContentType.DICT.
            coding (str, optional): The file encoding. Defaults to Coding.UTF8.
            indent (int, optional): The indentation level for JSON formatting. Defaults to 2.
            ensure_ascii (bool, optional): Whether to ensure ASCII characters in the JSON output. Defaults to False.
            sort_keys (bool, optional): Whether to sort the keys in the JSON output. Defaults to False.
        """

        self._content_type = content_type
        self.__check_content_type()

        self._coding = coding
        self.__check_extension()

        self._ensure_ascii = ensure_ascii
        self._indent = indent
        self._sort_keys = sort_keys

    def open(self, *, create_file: bool = False) -> TextIO:
        """
        Opens the JSON5 file.

        Args:
            create_file (bool, optional): Whether to create the file if it doesn't exist. Defaults to False.

        Returns:
            TextIO: The file object.

        Raises:
            FileNotFoundError: If the file is not found.
            FileOpenError: If the file is already open.
        """
        
        if create_file:
            self.new()

        if not self._is_exists:
            raise FileNotFoundError(f"File {self._path} is not found.")

        if self._file and self._is_opened:
            raise FileOpenError(f"File {self._path} is already open.")
            
        self._file = open(self._path, FileMode.READ_WRITE, encoding=self._coding)
        self._is_opened = self.__is_opened()

    def close(self, *, remove_file: bool = False) -> None:
        """
        Closes the JSON5 file.

        Args:
            remove_file (bool, optional): Whether to remove the file after closing. Defaults to False.

        Raises:
            FileOpenError: If the file is already closed.
        """

        if not self._file and not self._is_opened:
            raise FileOpenError(f"File {self._path} is already closed.")

        self._file.close()
        self._file = None
        self._is_opened = self.__is_opened()

        if remove_file:
            self.remove()

    def new(self, replace_file: bool = False,
            default_content: Optional[Union[dict, list]] = None) -> None:
        """
        Creates a new JSON5 file.

        Args:
            replace_file (bool, optional): Whether to replace the file if it already exists. Defaults to False.
            default_content (Optional[Union[dict, list]], optional): Default content to write to the file. Defaults to None.
        """

        if not self._is_exists or replace_file:
            with open(self._path, FileMode.READ_WRITE_NEW, encoding=self._coding) as new_file:
                new_file.write("{}" if self._content_type == ContentType.DICT else "[]")
                self._is_exists = self.__is_exists()

            if default_content:
                if self._content_type == ContentType.LIST:
                    self.write([default_content])

                elif self._content_type == ContentType.DICT:
                    self.write(default_content)

    def remove(self) -> None:
        """
        Removes the JSON5 file.

        Raises:
            FileNotFoundError: If the file is not found.
            FileOpenError: If the file is currently open.
        """

        if not self._is_exists:
            raise FileNotFoundError(f"File {self._path} is not found.")
        
        if self._is_opened:
            raise FileOpenError(f"File {self._path} is opened")

        os.remove(self._path)
        self._is_exists = self.__is_exists()

    def read(self) -> Union[dict, list]:
        """
        Reads the content of the JSON5 file.

        Returns:
            Union[dict, list]: The content of the JSON5 file as a dictionary or a list.

        Raises:
            FileNotFoundError: If the file is not found.
            FileOpenError: If the file is not opened.
        """

        if not self._is_exists:
            raise FileNotFoundError(f"File {self._path} is not found.")
        
        if not self._is_opened:
            raise FileOpenError(f"File {self._path} is not opened.")

        self._file.seek(0)
        read_data = json5.load(self._file, cls=JsonDecoder)
        self._content = read_data
        return read_data         

    def write(self, content: Optional[Union[dict, list]] = None) -> None:
        """
        Writes content to the JSON5 file.

        Args:
            content (Optional[Union[dict, list]], optional): The content to write to the file. Defaults to None (writes the current content).

        Raises:
            FileNotFoundError: If the file is not found.
            FileOpenError: If the file is not opened or if there is an error writing to the file.
        """

        if not self._is_exists:
            raise FileNotFoundError(f"File {self._path} is not found.")

        if not self._is_opened:
            raise FileOpenError(f"File {self._path} is not opened.")
        
        if content is None:
            content = self._content

        try:
            self._file.seek(0)
            self._file.truncate()
            json5.dump(content, self._file, cls=JsonEncoder, indent=self._indent, ensure_ascii=self._ensure_ascii, sort_keys=self._sort_keys)
            self._file.flush()

            self._content = content

            self._is_empty = self.__is_empty()

        except Exception as exception:
             raise FileOpenError(f"Error writing to the {self._path} file: {exception}") from exception

    def clear(self) -> None:
        """
        Clears the content of the JSON5 file (writes an empty dictionary or list).
        """

        if self._content_type == ContentType.DICT:
            self.write({})
        else:
            self.write([])

    def get_size(self) -> int:
        """
        Gets the size of the JSON5 file content.

        Returns:
            int: The number of elements in the JSON5 content (length of the dictionary or list).
        """
        if self._content is None:
            return 0
        return len(self._content)


class Json5File(SimpleJson5File):
    """
    A class for reading and writing JSON5 files, extending SimpleJson5File with dataclass support.

    Allows reading the file content directly into dataclass objects and writing
    dataclass objects to the file. Uses the `json5` library for JSON5 support.
    """

    def __init__(self, file_path: str, content_type: str = ContentType.DICT, *,
                 coding: str = Coding.UTF8, auto_load: bool = False, indent: int = 2,
                 ensure_ascii: bool = False, sort_keys: bool = False, create_file: bool = False,
                 default_content: Optional[Union[dict, list]] = None) -> None:
        """
        Initializes a Json5File object.

        Args:
            file_path (str): The path to the JSON5 file.
            content_type (str, optional): The expected content type of the file (dict or list). Defaults to ContentType.DICT.
            coding (str, optional): The file encoding. Defaults to Coding.UTF8.
            auto_load (bool, optional): Whether to automatically load the file content upon initialization. Defaults to False.
            indent (int, optional): The indentation level for JSON formatting. Defaults to 2.
            ensure_ascii (bool, optional): Whether to ensure ASCII characters in the JSON output. Defaults to False.
            sort_keys (bool, optional): Whether to sort the keys in the JSON output. Defaults to False.
            create_file (bool, optional): Whether to create the file if it doesn't exist. Defaults to False.
            default_content (Optional[Union[dict, list]], optional): Default content to write to the file if it's created. Defaults to None.
        """

        super().__init__(file_path, content_type, coding=coding, auto_load=auto_load,
                         indent=indent, ensure_ascii=ensure_ascii, sort_keys=sort_keys,
                         create_file=create_file, default_content=default_content)

    def __enter__(self) -> "Json5File":
        self.open(create_file=True)
        return self
    
    def __exit__(self, *args) -> None:
        self.close()

    def read_as_dataclass(self, dataclass: Type[T]) -> T | list[T]:
        """
        Reads the JSON5 file content and converts it into a dataclass object or a list of dataclass objects.

        Args:
            dataclass (Type[T]): The dataclass type to convert the JSON5 content into.

        Returns:
            T | list[T]: A dataclass object or a list of dataclass objects.
        """

        data = self.read()

        if isinstance(data, list):
            return [from_dict(dataclass, item) for item in data]

        return from_dict(dataclass, data)

    def write(self, content: Optional[Union[dict, list, Type[T]]] = None) -> None:
        """
        Writes content to the JSON5 file, handling dataclass objects.

        If the content is a dataclass object or a list of dataclass objects, it will be converted to a dictionary before writing.

        Args:
            content (Optional[Union[dict, list, Type[T]]], optional): The content to write to the file. Defaults to None (writes the current content).
        """

        if content is None:
            content = self._content

        if isinstance(content, list):
            items = []
            for item in content:
                if is_dataclass(item):
                    item = asdict(item)
            content = items

        elif is_dataclass(content):
            content = asdict(content)
            json5.dump(content, self._file, cls=JsonEncoder, indent=self._indent, ensure_ascii=self._ensure_ascii, sort_keys=self._sort_keys)
            self._content = content
