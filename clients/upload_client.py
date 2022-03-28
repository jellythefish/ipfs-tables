from clients.database_client import DatabaseClient
from clients.ipfs_client import IPFSClient

from typing import List, Tuple

import pathlib
import logging
import time
import socket

class UploadClient(object):
    def __init__(self) -> None:
        self.db_client = DatabaseClient("postgres", "postgres", "postgres", "51.250.13.25", 5432)
        self.ipfs_client = IPFSClient()

        logging.basicConfig()
        logging.getLogger().setLevel(logging.DEBUG)

    def _upload_files(self, files: List[Tuple[pathlib.Path, dict]]) -> None:
        for file, meta in files:
            response = self.ipfs_client.create_file(file)
            meta["hash"] = response["Hash"]
            self.db_client.add(meta)

    def _extract_meta(self, file: pathlib.Path, media_format=None, tags=None):
        meta = {}
        meta["name"] = file.name
        filename_parts = file.name.split('.')
        if len(filename_parts) > 1:
            meta["file_extension"] = ".{}".format(filename_parts[1])
        else:
            meta["file_extension"] = ""

        meta["type"] = "file"
        meta["media_format"] = media_format if media_format else ""
        meta["upload_timestamp"] = int(time.time())
        meta["bytesize"] = file.stat().st_size
        meta["tags"] = tags.split(',') if tags else []
        meta["uploaded_by"] = socket.gethostname()
        return meta

    def upload_to_ipfs(self, path: str, media_format=None, tags=None):
        object = pathlib.Path(path)
        assert object.exists(), "path {} does not exist".format(path)

        result = []

        if object.is_file():
            logging.debug("Uploading file {} to ipfs db".format(object.resolve()))
            metadata = self._extract_meta(object, media_format, tags)
            result = [(object, metadata)]
        if object.is_dir():
            logging.debug("Uploding files in directory {} to ipfs".format(object.resolve()))
            for file in object.rglob("*"):
                if file.is_dir():
                    continue
                result.append((file, self._extract_meta(file, media_format, tags)))

        self._upload_files(result)
