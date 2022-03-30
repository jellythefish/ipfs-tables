#!/bin/bash

wget https://dist.ipfs.io/go-ipfs/v0.7.0/go-ipfs_v0.7.0_linux-amd64.tar.gz
tar -xvzf go-ipfs_v0.7.0_linux-amd64.tar.gz
cd go-ipfs
sudo bash install.sh
sudo su
cat <<EOT >> /lib/systemd/system/ipfs.service
[Unit]
Description=IPFS daemon
After=network.target
[Service]
User=ipfsuser
ExecStart=/usr/local/bin/ipfs daemon --enable-pubsub-experiment
[Install]
WantedBy=multiuser.target
EOT
exit
ipfs init
sudo systemctl start ipfs
sudo systemctl enable ipfs
