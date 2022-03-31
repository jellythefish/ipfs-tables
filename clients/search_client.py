from argparse import ArgumentParser
import os
import sys
import psycopg2
import copy
from clients.ipfs_client import IPFSClient
import sqlite3

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
        self.postgres_conn = psycopg2.connect(
            host=METADATA_DB_HOST,
            port=METADATA_DB_PORT,
            database="postgres",
            user="postgres",
            password="postgres",
            connect_timeout=10)
        self.postgres_cursor = self.postgres_conn.cursor()
        self.ipfs = IPFSClient()
        self.sqlite_conn = sqlite3.connect('meta.db')
        self.sqlite_cursor = self.sqlite_conn.cursor()

    def search_in_postgres_metadata(self, search_key, search_type=None):
        query_str = f"SELECT hash, name, type, media_format, file_extension, upload_timestamp, uploaded_by, bytesize, tags FROM {TABLE_NAME}"
        if search_key is not None:
            query_str +=  f" WHERE '{search_key}'=ANY(tags)"
            if search_type is not None:
                query_str += f" AND media_format = '{search_type}'"
        elif search_type is not None:
            query_str +=  f" WHERE media_format = '{search_type}'"
        self.postgres_cursor.execute(query_str)

        rows = self.postgres_cursor.fetchall()
        result = [] 
        for row in rows:
            hash, name, type, media_format, file_extension, upload_timetsamp, uploaded_by, bytesize, tags = row
            print(f'postgres returned: {name}')
            object = Object(hash, name, type, file_extension, upload_timetsamp, uploaded_by, bytesize, tags)
            result.append(copy.deepcopy(object))

        return result

    def search_in_sqlite_metadata(self, search_key, search_type=None):
        query_str = f"SELECT hash, name, type, media_format, file_extension, upload_timestamp, uploaded_by, bytesize, tags FROM {TABLE_NAME}"
        if search_key is not None:
            query_str +=  f" WHERE ( tags == '{search_key}' OR tags LIKE '%,{search_key}' OR tags LIKE '{search_key},%' OR tags LIKE '%,{search_key},%')"
            if search_type is not None:
                query_str += f" AND media_format = '{search_type}'"
        elif search_type is not None:
            query_str +=  f" WHERE media_format = '{search_type}'"

        result = [] 
        for row in self.sqlite_cursor.execute(query_str):
            hash, name, type, media_format, file_extension, upload_timetsamp, uploaded_by, bytesize, tags = row
            print(f'sqlute return {name}')
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
        metadata_results = self.search_in_postgres_metadata(search, type)
        metadata_results.extend(self.search_in_sqlite_metadata(search, type))
        results = ''
        keys = []
        for result in metadata_results:
            url = self.process_metadata_result(result)
            if result.name not in keys:
                #print(f'Result url: {url}')
                results = results + result.get_formatted_result(url)
                keys.append(result.name)

        if search is not None and len(search) > 0:
            additional_search = search.split()
            if len(additional_search) > 1:
                for subsearch in additional_search:
                    metadata_results = self.search_in_postgres_metadata(subsearch, type)
                    metadata_results.extend(self.search_in_sqlite_metadata(search, type))
                    for result in metadata_results:
                        url = self.process_metadata_result(metadata_result)
                        if result.name not in keys:
                            results  = results + result.get_formatted_result(url)
                            keys.append(result.name)

        if len(results) == 0:
            print('Nothing found')
        else:
            print(results)


if __name__ == '__main__':
    main()
