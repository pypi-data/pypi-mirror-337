import hashlib
from pathlib import Path
import json


def mkdir_full(path):
    """
    Create a directory at the specified path, including any
    necessary parent directories if they do not already exist.

    This function ensures that the directory structure for the given
    path is created fully without raising an exception if a directory
    already exists. The operation is idempotent.

    :param path: The path of the directory to be created.
                 This can include nested directories.
    :type path: str
    :return: None
    """
    Path(path).mkdir(parents=True, exist_ok=True)


def file_get_length(file_path, chunk_size=5):
    """
    Calculates the total size of a file in bytes based on specified chunk size. The file is read in
    chunks to avoid high memory usage for large files. This function opens the file in binary mode
    and reads its contents iteratively, summing up the size of each chunk. This provides an efficient
    way to determine file size without loading the whole file into memory.

    :param file_path: The path to the file whose size needs to be calculated
    :type file_path: str
    :param chunk_size: Size of the chunks to read from the file in megabytes, default is 5MB
    :type chunk_size: int
    :return: Total size of the file in bytes
    :rtype: int
    """
    chunk_size = chunk_size * 1024 * 1024
    total_length = 0
    with open(file_path, 'rb') as file:
        while chunk := file.read(chunk_size):
            total_length += len(chunk)

    return total_length


def file_get_sha256(file_path, chunk_size=5, _object=False):
    """
    Calculates the SHA-256 checksum of a file in chunks or returns the hashlib object when specified. The function reads
    the file in configurable chunk sizes to handle large files efficiently. Optionally, the hashlib object can be returned
    instead of its hexadecimal digest.

    :param file_path: The path to the file whose SHA-256 checksum is to be calculated.
    :type file_path: str
    :param chunk_size: The size of each chunk (in MB) to read from the file during processing. Default is 5 MB.
    :type chunk_size: int
    :param _object: If True, the function returns the hashlib object instead of the hexadecimal checksum digest.
    :type _object: bool
    :return: The SHA-256 checksum in hexadecimal format or the hashlib object if `_object` is True.
    :rtype: str or hashlib._hashlib.HASH
    """
    chunk_size = chunk_size * 1024 * 1024
    sha256 = hashlib.sha256()

    with open(file_path, 'rb') as file:
        while chunk := file.read(chunk_size):
            sha256.update(chunk)

    if _object:
        return sha256

    return sha256.hexdigest()

def touch(path, content=''):
    """
    Creates or overwrites a file at the specified path and writes the provided content
    into it. This method opens the file in write mode, writes the content, and then
    closes the file.

    :param path: The file path where the file will be created or overwritten.
    :type path: str
    :param content: The content to be written into the file.
    :type content: str
    :return: None
    """
    f = open(path, 'w')
    f.write(content)
    f.close()

def has_json_content(file_path):
    """
    Checks if the file at the provided path contains valid JSON content.

    This function attempts to open a file in read mode with UTF-8 encoding
    and parses its content as JSON. If the parsing succeeds, the function
    returns True, indicating that the file contains valid JSON content.
    Otherwise, it handles JSON decoding or Unicode decoding errors and
    returns False.

    :param file_path: Path of the file to be checked.
    :type file_path: str
    :return: A boolean indicating whether the file contains valid JSON content.
    :rtype: bool
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            json.load(f)
        return True
    except (json.JSONDecodeError, UnicodeDecodeError):
        return False