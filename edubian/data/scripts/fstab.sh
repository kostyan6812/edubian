#!/bin/bash

blkid >> /etc/fstab
update-rc.d -f fstab.sh remove

# Delete me
rm $0
