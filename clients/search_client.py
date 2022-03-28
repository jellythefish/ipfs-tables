from argparse import ArgumentParser
import os
import sys
import psycopg2
import copy
from clients.ipfs_client import IPFSClient

METADATA_DB_HOST = '51.250.13.25'
METADATA_DB_PORT = 5432

TABLE_NAME = 'metadata'


class Object():
    description = None
    hash = None
    format = None
    upload_time = None
    uploader = None
    size = None
    key = None

    def __init__(self, hash, name, type, file_extension, upload_timestamp, uploaded_by, bytesize, tags):
            self.hash = hash
            self.name = name
            self.type = type
            self.file_extension = file_extension
            self.upload_timestamp = upload_timestamp
            self.uploaded_by = uploaded_by
            self.size = bytesize
            self.tags = tags

    def get_formatted_result(self, url):
        return f"Name: {self.name}\nType: {self.type}, link: {url}, uploaded by: {self.uploaded_by}, upload time: {self.upload_timestamp}\n"


class SearchClient():
    def __init__(self):
        self.conn = psycopg2.connect(
            host=METADATA_DB_HOST,
            port=METADATA_DB_PORT,
            database="postgres",
            user="postgres",
            password="postgres")
        self.cursor = self.conn.cursor()
        self.ipfs = IPFSClient()

    def search_in_metadata(self, search_key, search_type=None):
        query_str = f"SELECT hash, name, type, media_format, file_extension, upload_timestamp, uploaded_by, bytesize, tags FROM {TABLE_NAME}"
        if search_key is not None:
            query_str +=  f" WHERE '{search_key}'=ANY(tags)"
            if search_type is not None:
                query_str += f" AND media_format = '{search_type}'"
        elif search_type is not None:
            query_str +=  f" WHERE media_format = '{search_type}'"
        self.cursor.execute(query_str)

        rows = self.cursor.fetchall()
        result = [] 
        for row in rows:
            hash, name, type, media_format, file_extension, upload_timetsamp, uploaded_by, bytesize, tags = row
            object = Object(hash, name, type, file_extension, upload_timetsamp, uploaded_by, bytesize, tags)
            result.append(copy.deepcopy(object))

        return result

    def process_metadata_result(self, object):
        hash = object.hash
        #print(f'hash: {hash}')
        self.ipfs.get_file(hash)
        return 'ipfs.io/ipfs/' + hash

    def search(self, search, type):
        print(f"Using search phrase: {search}, search type: {type}")
        metadata_results = self.search_in_metadata(search, type)
        results = ''
        for result in metadata_results:
            url = self.process_metadata_result(result)
            #print(f'Result url: {url}')
            results = results + result.get_formatted_result(url)

        if search is not None and len(search) > 0:
            additional_search = search.split()
            if len(additional_search) > 1:
                for subsearch in additional_search:
                    metadata_results = self.search_in_metadata(subsearch, type)
                    for result in metadata_results:
                        url = self.process_metadata_result(metadata_result)
                        results  = results + result.get_formatted_result(url)

        if len(results) == 0:
            print('Nothing found')
        else:
            print(results)


if __name__ == '__main__':
    main()
