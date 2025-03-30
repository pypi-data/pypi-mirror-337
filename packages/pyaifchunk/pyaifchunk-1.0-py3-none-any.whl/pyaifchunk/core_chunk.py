class Chunk:
    """
    A class to read IFF chunked data from a file-like object.

    An IFF chunk has the following structure:
        Offset 0-3: 4-byte chunk ID (string)
        Offset 4-7: 4-byte size field (big-endian by default) indicating the size of the chunk's data,
                    not including the header (unless inclheader is True).
        Offset 8-(8+n-1): n bytes of data, where n is the size field (or size-8 if inclheader is True)
        (Optional) Pad byte: If align is True and n is odd, a pad byte is present.

    Attributes:
        _file: The underlying file-like object.
        _align: Boolean indicating whether 2-byte alignment is assumed.
        _bigendian: Boolean indicating whether the size field is big-endian.
        _inclheader: If True, the size includes the header (8 bytes).
        _name: The 4-byte chunk ID.
        _data_size: The size of the chunk data (excluding header, unless inclheader is True).
        _data_start: File position where the data starts.
        _data_end: File position marking the end of the chunk data.
        _closed: Boolean flag that becomes True after skip() or close() is called.
    """

    def __init__(self, file, align: bool = True, bigendian: bool = True, inclheader: bool = False):
        self._file = file
        self._align = align
        self._bigendian = bigendian
        self._inclheader = inclheader
        self._closed = False

        # Read the 8-byte header
        header = self._file.read(8)
        if len(header) < 8:
            raise EOFError("Not enough bytes to read a complete chunk header")

        # First 4 bytes: chunk ID
        self._name = header[:4]

        # Next 4 bytes: size field
        size_field = header[4:8]
        byteorder = 'big' if self._bigendian else 'little'
        size_value = int.from_bytes(size_field, byteorder=byteorder)

        # If inclheader is True, then the size includes the header; adjust accordingly.
        if self._inclheader:
            if size_value < 8:
                raise ValueError("Size field is smaller than header size")
            self._data_size = size_value - 8
        else:
            self._data_size = size_value

        # Record current file pointer as the start of the chunk data.
        self._data_start = self._file.tell()
        self._data_end = self._data_start + self._data_size

        # If alignment is enabled and the data size is odd, a pad byte follows.
        if self._align and (self._data_size % 2 != 0):
            self._pad = 1
            self._data_end += 1  # account for pad byte
        else:
            self._pad = 0

    def getname(self):
        """
        Returns the 4-byte chunk ID.
        """
        return self._name

    def getsize(self):
        """
        Returns the size of the chunk data (not including the header, unless inclheader was True).
        """
        return self._data_size

    def read(self, size=-1):
        """
        Reads up to 'size' bytes from the chunk's data.

        If size is negative or omitted, read all remaining data from the chunk.
        Reading does not go past the end of the chunk (including the pad byte).
        """
        if self._closed:
            raise OSError("Chunk is closed")

        current_pos = self._file.tell()
        # Calculate how many bytes remain in the chunk (data plus pad, if applicable)
        remaining = self._data_end - current_pos
        if remaining <= 0:
            return b''

        if size < 0 or size > remaining:
            size = remaining
        return self._file.read(size)

    def seek(self, pos, whence=0):
        """
        Seek to a position within the chunk data.

        whence: 0 (absolute within chunk), 1 (relative to current position), 2 (relative to chunk's end).
        """
        if self._closed:
            raise OSError("Chunk is closed")

        # Determine absolute target position relative to _data_start
        if whence == 0:
            target = self._data_start + pos
        elif whence == 1:
            target = self._file.tell() + pos
        elif whence == 2:
            target = self._data_end + pos
        else:
            raise ValueError("Invalid value for whence")

        # Clamp target within chunk boundaries
        if target < self._data_start:
            target = self._data_start
        if target > self._data_end:
            target = self._data_end
        self._file.seek(target)
        return target - self._data_start

    def tell(self):
        """
        Returns the current position within the chunk data.
        """
        if self._closed:
            raise OSError("Chunk is closed")
        return self._file.tell() - self._data_start

    def skip(self):
        """
        Skip to the end of the chunk (including any pad byte).
        Subsequent calls to read() will return an empty bytes object.
        """
        if not self._closed:
            self._file.seek(self._data_end)
            self._closed = True

    def close(self):
        """
        Convenience method to skip to the end of the chunk.
        Does not close the underlying file.
        """
        self.skip()

    def isatty(self):
        """
        Returns False as the chunk is not associated with a terminal.
        """
        return False
