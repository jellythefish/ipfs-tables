import argparse

from clients.upload_client import UploadClient
from clients.search_client import SearchClient

def main():
    parser = argparse.ArgumentParser('IPFS DB Client')
    subparsers = parser.add_subparsers(help='Commands')

    upload_command = subparsers.add_parser('upload', help='Upload file or directory.')
    upload_command.add_argument('path', type=str, help='Path to file or directory')
    upload_command.add_argument('--format', type=str, choices=['audio', 'video', 'notes'])
    upload_command.add_argument('--tags', type=str, help="tags in following format 'tag1,tag2,tag3'")

    upload_command.set_defaults(upload_command=True)

    search_command = subparsers.add_parser('search', help='Search in IPFS db')
    search_command.add_argument('--search', help="Search phrase")
    search_command.add_argument('--type', help="Search type (video, audio, text)")
    search_command.set_defaults(search_command=True)

    args = parser.parse_args()

    if hasattr(args, 'upload_command'):
        upload_client = UploadClient()
        media_format = args.format if hasattr(args, 'format') else None
        tags = args.tags if hasattr(args, 'tags') else None
        upload_client.upload_to_ipfs(args.path, media_format, tags)
    elif hasattr(args, 'search_command'):
        search_client = SearchClient()
        search_client.search(args.search, args.type)


if __name__ == '__main__':
    main()
