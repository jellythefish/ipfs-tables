import argparse
import logging

import pathlib
import time
import socket

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)

#    hash VARCHAR PRIMARY KEY,
#    name VARCHAR NOT NULL, -- 'i.e. lectures, lecture01.mov'
#    type VARCHAR NOT NULL, -- 'file' or 'directory'
#    file_extension VARCHAR, -- 'i.e. .pdf, .doc, .py'
#    media_format VARCHAR, -- 'audio, video, notes'
#    upload_timestamp timestamp NOT NULL,
#    bytesize INT NOT NULL,
#    tags VARCHAR[],
#    uploaded_by VARCHAR

def extract_meta(file, media_format=None, tags=None):
    meta = {}
    meta["name"] = file.name
    filename_parts = file.name.split('.')
    if len(filename_parts) > 1:
        meta["file_extension"] = ".{}".format(filename_parts[1])
    else:
        meta["file_extension"] = ""
    meta["media_format"] = media_format if media_format else ""
    meta["upload_timestamp"] = int(time.time())
    meta["bytesize"] = file.stat().st_size
    meta["tags"] = tags.split(',') if tags else []
    meta["uploaded_by"] = socket.gethostname()
    return meta


def upload_to_ipfs(path, media_format=None, tags=None):
    object = pathlib.Path(path)
    assert object.exists(), "path {} does not exist".format(path)

    if object.is_file():
        logging.debug("Uploading file {} to ipfs db".format(object.resolve()))
        metadata = extract_meta(object, media_format, tags)
        return [(object, metadata)]
    if object.is_dir():
        files = []
        logging.debug("Uploding files in directory {} to ipfs".format(object.resolve()))
        for file in object.iterdir():
            files.append((file, extract_meta(file, media_format, tags)))
        return files


def main():
    parser = argparse.ArgumentParser('IPFS DB Client')
    subparsers = parser.add_subparsers(help='Commands')

    upload_command = subparsers.add_parser('upload', help='Upload file or directory.')
    upload_command.add_argument('path', type=str, help='Path to file or directory')
    upload_command.add_argument('--format', type=str, choices=['audio', 'video', 'notes'])
    upload_command.add_argument('--tags', type=str, help="tags in following format 'tag1,tag2,tag3'")
    upload_command.set_defaults(upload_command=True)

    search_command = subparsers.add_parser('search', help='Search in IPFS db')
    search_command.add_argument('request', type=str, help='Path to file or directory')
    search_command.set_defaults(search_command=True)

    args = parser.parse_args()

    if hasattr(args, 'upload_command'):
        media_format = args.format if hasattr(args, 'format') else None
        tags = args.tags if hasattr(args, 'tags') else None
        upload_to_ipfs(args.path, media_format, tags)
    elif hasattr(args, 'search_command'):
        print("Search command called with request", args.request)
        # Call To Search Engine


if __name__ == '__main__':
    main()
