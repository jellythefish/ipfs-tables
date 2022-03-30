from clients.ipfs_client import IPFSClient
from clients.sqlite_client import LocalSQLiteDatabaseClient

import base64
import json

class UpdateClient:
    def __init__(self) -> None:
        self.db_client = LocalSQLiteDatabaseClient()
        self.ipfs_client = IPFSClient()

    def run(self) -> None:
        self.ipfs_client.sub("updates")
        with self.ipfs_client.client.pubsub.subscribe('updates') as sub:
            for message in sub:
                meta = json.loads(json.loads(base64.b64decode(message["data"]).decode('utf-8')))
                meta["tags"] = ','.join(meta['tags'])
                self.db_client.add(meta)

if __name__ == '__main__':
    client = UpdateClient()
    client.run()