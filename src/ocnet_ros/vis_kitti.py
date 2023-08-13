import os
import numpy as np
from mayavi import mlab
import LMSCNet.data.io_data as SemanticKittiIO

point_file = '/home/jmwang/LMSCNet/vel/000145.bin'

voxel_file = '/home/jmwang/LMSCNet/vox/000145.bin'

label_file = '/home/jmwang/LMSCNet/label/000145.label'

yaml_file = '/home/jmwang/LMSCNet/LMSCNet/data/semantic-kitti.yaml'


def Vis_SemanticKITTI_point(point_file):
    # Read point cloud data
    pointcloud = SemanticKittiIO._read_pointcloud_SemKITTI(point_file)
    print(pointcloud.shape)

    # Creating figure object
    figure = mlab.figure(figure='Figure', bgcolor=(1, 1, 1), size=(1920, 1200))

    # Plotting the point cloud
    mlab.points3d(pointcloud[:, 0], pointcloud[:, 1], pointcloud[:, 2], pointcloud[:, 3],
                  colormap='jet', scale_factor=0.1)

    # Saving the visualization as an image
    mlab.view(azimuth=30)  # Set the viewing angle (optional)
    mlab.savefig('/home/jmwang/LMSCNet/vel/vis_007.jpg')

    mlab.show()

def Vis_SemanticKITTI_Label(label_file, yaml_file):
    # Read invalid mask and label data
    data_path = os.path.dirname(label_file)
    
    LABEL = SemanticKittiIO._read_label_SemKITTI(label_file)
    remap_lut = SemanticKittiIO.get_remap_lut(yaml_file)
    LABEL = remap_lut[LABEL.astype(np.uint16)].astype(np.float32)  # Remap 20 classes semanticKITTI SSC
    
    grid_dimensions = [256, 32, 256]

    scale_divide = 1  # Insert the correct value here
    LABEL = np.moveaxis(LABEL.reshape([int(grid_dimensions[0] / scale_divide),
                                       int(grid_dimensions[2] / scale_divide),
                                       int(grid_dimensions[1] / scale_divide)]),
                        [0, 1, 2], [0, 2, 1])
    print(np.count_nonzero(LABEL))
    # Creating figure object
    figure = mlab.figure(figure='Figure', bgcolor=(1, 1, 1), size=(1920, 1200))

    # Get grid coordinates X, Y, Z
    grid_coords, _, _, _ = SemanticKittiIO.get_grid_coords([LABEL.shape[0], LABEL.shape[2], LABEL.shape[1]], 0.2)
    grid_coords = np.vstack((grid_coords.T, np.moveaxis(LABEL, [0, 1, 2], [0, 2, 1]).reshape(-1))).T
    
    # Obtaining voxels with semantic class
    occupied_voxels = grid_coords[(grid_coords[:, 3] > 0) & (grid_coords[:, 3] < 255)]

    # Plot as points with cube as mode, resolution is 0.2,  we set scale_factor slightly smaller
    plt_plot = mlab.points3d(occupied_voxels[:, 0], occupied_voxels[:, 1], occupied_voxels[:, 2], occupied_voxels[:, 3],
                             colormap='jet', scale_factor=0.1, mode='cube', opacity=1)
    
    # Scaling all voxels the same size
    plt_plot.glyph.scale_mode = 'scale_by_vector'
    
    # Setting correct colormap
    plt_plot.module_manager.scalar_lut_manager.lut.table = SemanticKittiIO.get_cmap_semanticKITTI20()
    # Saving the visualization as an image
    mlab.view(azimuth=30)  # Set the viewing angle (optional)
    mlab.savefig('/home/jmwang/LMSCNet/label/vis_006.jpg')

    mlab.show()



def Vis_SemanticKITTI_Voxel(voxel_file):
    # Read the voxel occupancy from the file
    voxel_occupancy = SemanticKittiIO._read_occupancy_SemKITTI(voxel_file)
    
    # Reshape the voxel occupancy array to the correct dimensions
    voxel_occupancy = voxel_occupancy.reshape(256, 32, 256)
    print("count:", voxel_occupancy.shape)
    
    # Create a mask for occupied voxels
    voxel_mask = voxel_occupancy.ravel() == 1

    if not np.any(voxel_mask):
        print("No occupied voxels present.")
        return

    # Retrieve voxel grid coordinates (g_xx, g_yy, g_zz are not used in visualization)
    coords_grid, _, _, _ = SemanticKittiIO.get_grid_coords((256, 256, 32), 1)

    # Keep only occupied voxels' coordinates
    occupied_coords = coords_grid[voxel_mask]
    print(occupied_coords)
    # Print min and max coordinates
    print("Min coords:", np.min(occupied_coords, axis=0))
    print("Max coords:", np.max(occupied_coords, axis=0))
    print(np.count_nonzero(voxel_occupancy))
    # Mayavi visualization
    fig = mlab.figure(figure='Voxel', bgcolor=(1, 1, 1), size=(1920, 1200))

    occupied_voxels = mlab.points3d(occupied_coords[:, 0],
                                    occupied_coords[:, 1],
                                    occupied_coords[:, 2],
                                    mode='cube',
                                    opacity=1,
                                    scale_factor=0.2)
                                    
    # Saving the visualization as an image
    mlab.view(azimuth=30)  # Set the viewing angle (optional)
    mlab.savefig('/home/jmwang/LMSCNet/vox/vis_006.jpg')
    mlab.show()

def occupancy_stats(voxel_file, label_file):
    # Read the voxel occupancy from the file
    voxel_occupancy = SemanticKittiIO._read_occupancy_SemKITTI(voxel_file)
    
    # Reshape the voxel occupancy array to the correct dimensions
    voxel_occupancy = voxel_occupancy.reshape(256, 32, 256)
    
    # Create a mask for occupied voxels
    voxel_mask = voxel_occupancy.ravel() == 1

    # Count the occupied voxels in the voxel file
    voxel_occupied_count = np.count_nonzero(voxel_mask)

    # Read the label data from the label file
    LABEL = SemanticKittiIO._read_label_SemKITTI(label_file)
    label_occupancy = LABEL > 0

    # Count the occupied voxels in the label file
    label_occupied_count = np.count_nonzero(label_occupancy)

    # Compute the intersection of occupied voxels in both files
    intersection = np.logical_and(voxel_mask, label_occupancy.ravel())

    # Count the intersected occupied voxels
    intersection_count = np.count_nonzero(intersection)

    # Count the non-intersected occupied voxels
    non_intersection_voxel_count = voxel_occupied_count - intersection_count
    non_intersection_label_count = label_occupied_count - intersection_count
    
    
    print("Voxel file occupied count:", voxel_occupied_count)
    print("Label file occupied count:", label_occupied_count)
    print("Intersection occupied count:", intersection_count)
    print("Non-intersection voxel occupied count:", non_intersection_voxel_count)
    print("Non-intersection label occupied count:", non_intersection_label_count)

    return voxel_occupied_count, label_occupied_count, intersection_count, non_intersection_voxel_count, non_intersection_label_count



def main():
    #Vis_SemanticKITTI_point(point_file)
    #Vis_SemanticKITTI_Voxel(voxel_file)
    Vis_SemanticKITTI_Label(label_file, yaml_file)
    #occupancy_stats(voxel_file, label_file)


if __name__ == "__main__":
    main()