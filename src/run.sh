roslaunch plan_manage real_kino_replan.launch & sleep 1;
roslaunch poly_traj_server traj_server.launch & sleep 1;
# rosrun plan_manage pointcloud_listener.py & sleep 1;
wait;