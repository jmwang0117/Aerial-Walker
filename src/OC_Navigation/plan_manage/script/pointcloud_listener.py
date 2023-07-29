#!/usr/bin/python3
import rospy
import struct
from sensor_msgs.msg import PointCloud2
import sensor_msgs.point_cloud2 as pc2

scan_count = 0

def callback(data):
    global scan_count
    points = pc2.read_points(data, field_names=("x", "y", "z"), skip_nans=True)

    remission_value = 1.0  # Assign a fixed value to the remission field

    with open(f'scan_{scan_count}.bin', 'wb') as f:
        for point in points:
            x = struct.pack('f', point[0])
            y = struct.pack('f', point[1])
            z = struct.pack('f', point[2])
            remission = struct.pack('f', remission_value)  # Assigning fixed value to remission
            f.write(x + y + z + remission)

    scan_count += 1

def listener():
    rospy.init_node('pointcloud_listener', anonymous=True)
    
    # Choose the desired topic ("/sdf_map/cloud" or "/sdf_map/occupancy")
    topic = "/sdf_map/depth_cloud"  # Replace with the desired topic name
    
    rospy.Subscriber(topic, PointCloud2, callback)
    
    rospy.spin()

if __name__ == '__main__':
    listener()