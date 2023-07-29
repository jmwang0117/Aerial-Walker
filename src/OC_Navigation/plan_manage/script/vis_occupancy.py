#!/usr/bin/python3
import rospy
import open3d as o3d
from sensor_msgs.msg import PointCloud2
from sensor_msgs import point_cloud2

def callback(point_cloud_msg):
    # Convert PointCloud2 message to Open3D PointCloud
    points = []
    for p in point_cloud2.read_points(point_cloud_msg, field_names=("x", "y", "z"), skip_nans=True):
        points.append(p)
    point_cloud = o3d.geometry.PointCloud()
    point_cloud.points = o3d.utility.Vector3dVector(points)

    # Create visualization
    vis = o3d.visualization.Visualizer()
    vis.create_window()
    vis.add_geometry(point_cloud)
    vis.run()
    vis.destroy_window()

def main():
    rospy.init_node('occupancy_map_visualizer')
    cloud_topic = rospy.get_param('~cloud_topic', '/sdf_map/occupancy')
    rospy.Subscriber(cloud_topic, PointCloud2, callback)
    rospy.spin()

if __name__ == '__main__':
    main()
