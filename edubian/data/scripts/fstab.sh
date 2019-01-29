#!/bin/sh -e
### BEGIN INIT INFO
# Provides:             fstab
# Required-Start:       
# Required-Stop:        
# Should-Start:
# Default-Start:        S
# Default-Stop:         0 1 6
# Short-Description:    fstab
### END INIT INFO

blkid >> /etc/fstab
update-rc.d -f fstab.sh remove

# Delete me
rm $0
