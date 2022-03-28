import ipfshttpclient

class IPFSClient(object):
    def __init__(self, address = None):
        if address is None:
            self.client = ipfshttpclient.connect()
        else:
            self.client = ipfshttpclient.connect(address)

    def create_file(self, filename):
        return self.client.add(filename)

    def get_file(self, filename):
        return self.client.get(filename)
