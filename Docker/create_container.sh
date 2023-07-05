xhost local:root
docker create -t --name bnv_fusion \
--gpus all \
--network host \
--ipc host \
--privileged \
--shm-size 8G \
-v /dev:/dev \
-v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY \
--device=/dev/dri:/dev/dri \
-v /home/jmwang/datasets:/datasets \
nvcr.io/nvidia/pytorch:23.01-py3 bash
