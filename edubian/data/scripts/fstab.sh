#!/bin/sh -e


blkid >> /etc/fstab
systemctl disable fstab.service

# Delete me
rm /etc/systemd/system/fstab.service
rm $0
