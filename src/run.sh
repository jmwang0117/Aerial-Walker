#!/bin/bash
SESSION_NAME="fast_planner"
# Create a new tmux session
tmux new-session -d -s "$SESSION_NAME"
# Execute the commands in each window
tmux send-keys -t "$SESSION_NAME:0" 'source ~/Aerial-Walker/devel/setup.bash; roslaunch plan_manage kino_replan.launch' C-m
tmux new-window -t "$SESSION_NAME" 'sleep 2; source ~/Aerial-Walker/devel/setup.bash; roslaunch poly_traj_server traj_server.launch'
tmux new-window -t "$SESSION_NAME" 'sleep 3; source ~/Aerial-Walker/devel/setup.bash; roslaunch plan_manage pointcloud_listener.launch'
tmux new-window -t "$SESSION_NAME" 'sleep 3; source ~/Aerial-Walker/devel/setup.bash; roslaunch ocnet_ros inference.launch'
# Attach to the tmux session
tmux attach-session -t "$SESSION_NAME"