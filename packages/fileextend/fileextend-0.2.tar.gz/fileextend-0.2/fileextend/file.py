import fileextend
import hashlib
import os

class File:
    def __init__(self, filepath):
        self.filepath = filepath
        self.type = 'string'
        self.encoding = 'utf-8'
        self.length = 0
        self.hash = {
            'sha256': hashlib.sha256()
        }

        if os.path.exists(filepath):
            self.length = fileextend.file_get_length(filepath)
            self.hash['sha256'] = fileextend.file_get_sha256(filepath, _object=True)

    def set_type(self, type):
        if not type in ['byte', 'string']:
            raise ValueError("Unexcepted type!")

        self.type = type

    def set_encoding(self, encoding):
        self.encoding = encoding

    def get_length(self):
        return self.length

    def get_hash_sha256(self):
        return self.hash['sha256'].hexdigest()

    def touch(self, content=""):
        if os.path.exists(self.filepath):
            return

        fileextend.mkdir_full(os.path.dirname(self.filepath))

        mode = 'w'

        if self.type == 'byte':
            mode = 'wb'
            content = bytes(content, encoding=self.encoding)

        self.length = len(content)
        self.hash['sha256'].update(content)

        with open(self.filepath, mode) as f:
            f.write(content)

    def append(self, content):
        if not os.path.exists(self.filepath):
            return

        mode = 'a'

        if self.type == 'byte':
            mode = 'ab'
            content = bytes(content, encoding=self.encoding)

        self.length += len(content)
        self.hash['sha256'].update(content)

        with open(self.filepath, mode) as f:
            f.write(content)
