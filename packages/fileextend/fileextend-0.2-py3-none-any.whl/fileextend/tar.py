import tarfile


def list_files_from_tar(tgz_path):
    """
    Summarizes a method for listing file names contained in a tar.gz archive.

    This static method utilizes the tarfile module to open a tar.gz file in read
    mode and extracts all the file and directory names present within the archive.
    The names retrieved are returned as a list of strings.

    @param tgz_path: The file path to the tar.gz archive from which to list file
    names.
    @type tgz_path: str

    @return: List of file and directory names contained within the tar.gz archive.
    @rtype: list[str]
    """
    with tarfile.open(tgz_path, "r:gz") as tar:
        return tar.getnames()


def extract_tar_file(tgz_path, filename):
    """
    Extracts a file with the specified filename from a given gzip-compressed tar archive
    and reads its content as a string. If the specified file is not found in the archive,
    it returns None.

    Parameters:
        tgz_path (str): The path to the gzip-compressed tar archive.
        filename (str): The name of the file to be extracted from the archive.

    Returns:
        str: The content of the extracted file as a UTF-8 decoded string if the file
            is found in the archive.
        None: If the specified file does not exist in the archive.
    """
    with tarfile.open(tgz_path, "r:gz") as tar:
        for member in tar.getmembers():
            if member.name == filename:
                file = tar.extractfile(member)
                content = file.read().decode("utf-8")
                return content
    return None


def is_valid_tar(tar_path):
    """
    Checks if the provided tar file path points to a valid tar archive.

    This function attempts to open the provided file path as a tar archive in
    read mode. It verifies the validity by attempting to fetch archive members.
    If any `TarError` is raised during this process, it concludes that the tar
    file is not valid and returns False.

    :param tar_path: The path to the tar file that needs validation. Expected to
        be a string containing a valid file path.
    :type tar_path: str
    :return: Boolean flag indicating if the file is a valid tar archive. Returns
        True if valid, otherwise returns False.
    :rtype: bool
    """
    try:
        with tarfile.open(tar_path, "r") as tar:
            tar.getmembers()
        return True
    except tarfile.TarError:
        return False
