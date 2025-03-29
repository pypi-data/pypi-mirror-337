import collections
import dbm
import hashlib
import logging
import pathlib
import struct
import tempfile
from datetime import UTC, datetime

logger = logging.getLogger(__name__)

struct_formats = {
    0: f"<B{hashlib.sha512().digest_size}sf",
}


class FileStore(collections.abc.MutableMapping):
    root_path = pathlib.Path(tempfile.gettempdir()).resolve() / 'siotls'

    def __init__(self, root_path=None):
        if root_path is not None:
            self.root_path = root_path
        if not self.root_path.is_dir():
            self.root_path.mkdir(0o775)
        self._store = dbm.open(self.root_path / 'store.dbm', 'c', 0o664)  # noqa: SIM115
        logger.info("using filestore at %s (%s entries)", self.root_path, len(self._store))

    def _parse(self, key, entry):
        version = int.from_bytes(entry[0], 'little')
        try:
            return struct_formats[version].unpack(entry)
        except (KeyError, ValueError) as exc:
            raise KeyError(key) from exc

    def __getitem__(self, key):
        match self._parse(key, self._store[key]):
            case (0, checksum, expire_timestamp):
                filepath = self.root_path / checksum.hex()
                try:
                    data = filepath.read_bytes()
                except OSError as exc:
                    exc_ = KeyError(key)
                    exc_.add_note(f"unable to access or read the file at {filepath}")
                    raise exc_ from exc

                return data, datetime.fromtimestamp(expire_timestamp, UTC)

    def __setitem__(self, key, item):
        data, expire = item

        # Using the checkum as filename has two advantages: (1) it makes
        # sure there are no weird characters, (2) it makes so a same
        # file with different keys is only stored once.
        version = 0
        checksum = hashlib.sha512(data).digest()

        filepath = self.root_path / checksum.hex()
        if not filepath.isfile():
            with filepath.open('wb') as file:
                file.chmod(0o664)
                file.write(data)

        self._store[key] = struct.pack(
            struct_formats[version],
            (version, checksum, expire.timestamp())
        )

    def __delitem__(self, key):
        entry = self._store.pop(key)
        match self._parse(key, entry):
            case (0, checksum, _):
                (self.root_path / checksum.hex()).unlink()

    def __len__(self):
        return len(self._store)

    def __iter__(self):
        return iter(self._store)

    def close(self):
        self._store.close()
