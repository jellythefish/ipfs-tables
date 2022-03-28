from argparse import ArgumentParser
import io
import os
import sys
from setuptools import find_packages, setup, Command
import requests
import psycopg2
from ipfs_client import IPFSClient

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

    def __init__(self, hash, name, type, file_extension, upload_timetsamp, uploaded_by, bytesize, tags):
            self.hash = hash
            self.name = name
            self.type = type
            self.format = foramt
            self.file_extension = file_extension
            self.upload_timestamp = upload_timestamp
            self.uploaded_by = uploaded_by
            self.size = size
            self.tags = tags

    def get_formatted_result(url):
        return f"Name: {self.name}\nType: {self.type}, link: {url}\n"


class SearchCommand():
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
        query_str = f"SELECT hash, name, type, media_format, file_extension, upload_timestamp, uploaded_by, bytesize, tags FROM {TABLE_NAME} WHERE name LIKE '%{search_key}%'"
        if search_type is not None:
            query_str += " AND media_format = {search_type}"
        self.cursor.execute(query_str)

        rows = self.cursor.fetchall()
        result = []
        for row in rows:
            hash, name, type, media_format, file_extension, upload_timetsamp, uploaded_by, bytesize, tags = row
            object = Object(hash, name, type, file_extension, upload_timetsamp, uploaded_by, bytesize, tags)
            result.append(object.get_result())

        return result

    def process_metadata_result():
        pass


def main():
    parser = ArgumentParser(prog='IPFS-tables client')

    parser.add_argument('--search', help="Search phrase")
    parser.add_argument('--type', help="Search type (video, audio, text)")

    args = parser.parse_args()

    print(f"Using search phrase: {args.search}, search type: {args.type}")

    search = args.search
    cmd = SearchCommand()
    metadata_results = cmd.search_in_metadata(search, args.type)
    result = ''
    for result in metadata_results:
        url = cmd.process_metadata_result(metadata_result)
        result.append(result.get_formatted_result(url))

    additional_search = search.split()
    for subsearch in additional_search:
        metadata_results = cmd.search_in_metadata(subsearch, args.type)
        result = ''
        for result in metadata_results:
            url = cmd.process_metadata_result(metadata_result)
            result.append(result.get_formatted_result(url))

    if len(result) == 0:
        print('Nothing found')
    else:
        print(result)


if __name__ == '__main__':
    main()