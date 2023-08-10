#!/usr/bin/python3
import rospy
import struct
import numpy as np
import os
import sensor_msgs.point_cloud2 as pc2
from sensor_msgs.msg import PointCloud2
from sensor_msgs.msg import PointField
import mapping

scan_count = 0


def callback(data):
    global scan_count

    points = pc2.read_points(data, field_names=("x", "y", "z", "intensity"), skip_nans=True)

    # Save point cloud as .bin file in Velodyne format
    save_point_cloud_as_bin(points, scan_count)

    
    scan_count += 1

def save_point_cloud_as_bin(points, scan_count):
    file_name = f'{scan_count:06}.bin'
    file_path = os.path.join('/home/melodic/jetsonNX/Aerial-Walker/src/oc_navigation/plan_manage/raw_data/velodyne', file_name)

    with open(file_path, 'wb') as f:
        for point in points:
            x, y, z = point
            remission = np.sqrt(x**2 + y**2 + z**2)  # Calculate the distance from the origin
            remission = remission / 10
            point_data = struct.pack('ffff', x, y, z, remission)
            f.write(point_data)



def listener():
    rospy.init_node('pointcloud_listener', anonymous=True)

    # Choose the desired topic ("/sdf_map/cloud" or "/sdf_map/occupancy")
    topic = "/sdf_map/obstacle_cloud"  # Replace with the desired topic name

    rospy.Subscriber(topic, PointCloud2, callback)

    rospy.spin()

if __name__ == '__main__':
    listener()
