import os
import numpy as np

def unpack(compressed):
  ''' given a bit encoded voxel grid, make a normal voxel grid out of it.  '''
  uncompressed = np.zeros(compressed.shape[0] * 8, dtype=np.uint8)
  uncompressed[::8] = compressed[:] >> 7 & 1
  uncompressed[1::8] = compressed[:] >> 6 & 1
  uncompressed[2::8] = compressed[:] >> 5 & 1
  uncompressed[3::8] = compressed[:] >> 4 & 1
  uncompressed[4::8] = compressed[:] >> 3 & 1
  uncompressed[5::8] = compressed[:] >> 2 & 1
  uncompressed[6::8] = compressed[:] >> 1 & 1
  uncompressed[7::8] = compressed[:] & 1

  return uncompressed

def _read_SemKITTI(path, dtype, do_unpack):
  bin = np.fromfile(path, dtype=dtype)  # Flattened array
  if do_unpack:
    bin = unpack(bin)
  return bin

def _read_pointcloud_SemKITTI(path):
    # Return point cloud semantic kitti with remissions (x, y, z, intensity)
    point_cloud = _read_SemKITTI(path, dtype=np.float32, do_unpack=False)
    point_cloud = point_cloud.reshape((-1, 4))
    return point_cloud


def pack(array):
    assert array.size % 8 == 0, "The input array size must be divisible by 8."
    array = array.reshape((-1))

    # compressing bit flags.
    compressed = (
        (array[::8] << 7) | (array[1::8] << 6) | (array[2::8] << 5) | (array[3::8] << 4) | (array[4::8] << 3) | (array[5::8] << 2) | (array[6::8] << 1) | (array[7::8])
    )

    return np.array(compressed, dtype=np.uint8)


def voxelization(input_folder, output_folder, grid_size):
    for file_name in os.listdir(input_folder):
        if file_name.endswith('.bin'):
            input_path = os.path.join(input_folder, file_name)
            output_path = os.path.join(output_folder, file_name)

            # Read point cloud
            point_cloud = _read_pointcloud_SemKITTI(input_path)
            points_xyz = point_cloud[:, :3]

            # Voxelization
            voxel_coords = ((points_xyz - voxel_origin) // voxel_size).astype(int)
            valid_mask = np.all((voxel_coords >= 0) & (voxel_coords < grid_size), axis=1)
            voxel_coords = voxel_coords[valid_mask]

            # Create an empty voxel grid
            voxel_grid = np.zeros(np.prod(grid_size), dtype=np.uint8)

            # Reshape voxel grid before assigning values
            voxel_grid_3d = voxel_grid.reshape(grid_size)

            # Set occupied voxels
            voxel_grid_3d[voxel_coords[:, 0], voxel_coords[:, 1], voxel_coords[:, 2]] = 1

            # Convert voxel grid back to a 1D array
            voxel_grid = voxel_grid_3d.flatten()

            # Convert voxel grid to bitwise representation
            voxel_grid_bin = pack(voxel_grid)

            # Save voxel grid to binary file
            voxel_grid_bin.tofile(output_path)
            # Count occupied voxels
            occupied_voxels_count = np.count_nonzero(voxel_grid == 1)

            # Print the file name and occupied voxels count
            print(f"File: {file_name}, Occupied voxels: {occupied_voxels_count}")


if __name__ == '__main__':
    input_folder = '/home/melodic/jetsonNX/Aerial-Walker/src/oc_navigation/plan_manage/raw_data/velodyne'
    output_folder = '/home/melodic/jetsonNX/Aerial-Walker/src/oc_navigation/plan_manage/raw_data/voxels'
    grid_size = (256, 256, 32)  # Set the desired grid size (x, y, z)

    voxel_origin = np.array([0.0, 0.0, 0.0])  # Specify the origin of the voxel grid
    voxel_size = 0.05 # Set the desired voxel size

    voxelization(input_folder, output_folder, grid_size)