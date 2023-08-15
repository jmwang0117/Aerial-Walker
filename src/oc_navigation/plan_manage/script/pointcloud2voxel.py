#!/usr/bin/env python3
import rospy
import struct
import numpy as np
import os
import sensor_msgs.point_cloud2 as pc2
from sensor_msgs.msg import PointCloud2

scan_count = 0


class PointCloud2Voxelization:
    def __init__(self):
        self.output_folder = '/home/melodic/jetsonNX/Aerial-Walker/src/oc_navigation/plan_manage/raw_data/voxels'
        self.grid_size = (256, 256, 32)
        self.publish_interval = rospy.Duration(4)  # Set the desired interval in seconds
        self.last_publish_time = rospy.Time(0)

    def callback(self, data):
        global scan_count
        current_time = rospy.Time.now()
        points = pc2.read_points(data, field_names=("x", "y", "z", "intensity"), skip_nans=True)

        # Calculate remission and convert points to the required format
        point_cloud = []

        for point in points:
            x, y, z = point[:3]
            remission = np.sqrt(x ** 2 + y ** 2 + z ** 2)  # Calculate the distance from the origin
            remission = remission / 10
            # print(f"x: {x}, y: {y}, z: {z}, remission: {remission}")            
            point_cloud.append([x, y, z, remission])

        point_cloud = np.array(point_cloud, dtype=np.float32)

        # Convert point cloud to voxels and save as .bin file
        self.process_voxelization(point_cloud, scan_count)

        scan_count += 1
        
    def pack(self, array):
        assert array.size % 8 == 0, "The input array size must be divisible by 8."
        array = array.reshape((-1))

        # compressing bit flags.
        compressed = (
            (array[::8] << 7) | (array[1::8] << 6) | (array[2::8] << 5) | (array[3::8] << 4) 
            | (array[4::8] << 3) | (array[5::8] << 2) | (array[6::8] << 1) | array[7::8]
        )

        return np.array(compressed, dtype=np.uint8)
    
    def process_voxelization(self, points, scan_count):
        # Compute voxel origin and size for the entire sequence
        voxel_origin, voxel_size = self.compute_voxel_params(points)

        # Convert point cloud to voxels and save as .bin file in the output_folder
        self.voxelization(points, voxel_origin, voxel_size, scan_count)

    def compute_voxel_params(self, points):
        voxel_size = 0.1
        voxel_origin = np.array([-10, -10, -0.1])
        return voxel_origin, voxel_size

    def voxelization(self, points, voxel_origin, voxel_size, scan_count):
        # Compute voxel coordinates
        points_xyz = points[:, :3]
        voxel_coords = ((points_xyz - voxel_origin) // voxel_size).astype(int)
        valid_mask = np.all((voxel_coords >= 0) & (voxel_coords < self.grid_size), axis=1)
        voxel_coords = voxel_coords[valid_mask]

        # Create an empty voxel grid
        voxel_grid = np.zeros(np.prod(self.grid_size), dtype=np.uint8)

        # Reshape voxel grid and set occupied voxels
        voxel_grid_3d = voxel_grid.reshape(self.grid_size)
        voxel_grid_3d[voxel_coords[:, 0], voxel_coords[:, 1], voxel_coords[:, 2]] = 1

        # Flatten the voxel grid and save as a .bin file
        voxel_grid = voxel_grid_3d.flatten()
        
        # Convert voxel grid to bitwise representation
        voxel_grid_bin = self.pack(voxel_grid)

        # Save the voxel grid as a .bin file
        file_name = f'{scan_count:06}.bin'
        file_path = os.path.join(self.output_folder, file_name)
        voxel_grid_bin.tofile(file_path)
        

    def listener(self):
        rospy.init_node('pointcloud2_voxelization', anonymous=True)
        
        topic = "/sdf_map/occupancy_inflate"  
        
        rospy.Subscriber(topic, PointCloud2, self.callback)

        rospy.spin()


if __name__ == '__main__':
    pcl2vox = PointCloud2Voxelization()
    pcl2vox.listener()