#!/bin/sh
sudo docker run --privileged --cap-add=SYS_ADMIN --cap-add=MKNOD --cap-add=SYS_PTRACE -v ${PWD}/output:/root/output -it edubian:1.1 -c "export TERM=$TERM" -d --rm
