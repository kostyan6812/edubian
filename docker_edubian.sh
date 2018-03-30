#!/bin/sh
sudo docker run --privileged --cap-add=SYS_ADMIN --cap-add=MKNOD --cap-add=SYS_PTRACE --dns 193.41.140.39 -p 10.0.1.24:5901:5901 -v output:/root/output/ -it 50d56ace1209
