#!/bin/sh -e


blkid >> /etc/fstab
service fstab disable
service fstab remove

# Delete me
rm /etc/systemd/system/fstab.service
rm $0
