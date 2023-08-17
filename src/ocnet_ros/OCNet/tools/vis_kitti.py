# from mayavi import mlab
# import os
# import numpy as np
# data_path = '/home/jmwang/Downloads'
# import LMSCNet.data.io_data as SemanticKittiIO
# scale_divide=1
# #INVALID = SemanticKittiIO._read_invalid_SemKITTI(os.path.join(data_path, '000000.invalid'))
# LABEL = SemanticKittiIO._read_label_SemKITTI(os.path.join(data_path, '000045.label'))
# remap_lut = SemanticKittiIO.get_remap_lut('/home/jmwang/LMSCNet/LMSCNet/data/semantic-kitti.yaml')
# LABEL = remap_lut[LABEL.astype(np.uint16)].astype(np.float32)  # Remap 20 classes semanticKITTI SSC
# #LABEL[np.isclose(INVALID, 1)] = 255  # Setting to unknown all voxels marked on invalid mask...
# grid_dimensions = [256, 32, 256]
# LABEL = np.moveaxis(LABEL.reshape([int(grid_dimensions[0] / scale_divide),
#                                    int(grid_dimensions[2] / scale_divide),
#                                    int(grid_dimensions[1] / scale_divide)]), [0, 1, 2], [0, 2, 1])

# # Creating figure object
# figure = mlab.figure(figure='Figure', bgcolor=(1, 1, 1), size=(1200, 1920))

# # Get grid coordinates X, Y, Z
# grid_coords, _, _, _ = SemanticKittiIO.get_grid_coords([LABEL.shape[0], LABEL.shape[2], LABEL.shape[1]], 0.2)
# grid_coords = np.vstack((grid_coords.T, np.moveaxis(LABEL, [0, 1, 2], [0, 2, 1]).reshape(-1))).T
# # Obtaining voxels with semantic class
# occupied_voxels = grid_coords[(grid_coords[:, 3] > 0) & (grid_coords[:, 3] < 255)]

# # Plot as points with cube as mode, resolution is 0.2,  we set scale_factor slightly smaller
# plt_plot = mlab.points3d(occupied_voxels[:, 0], occupied_voxels[:, 1], occupied_voxels[:, 2], occupied_voxels[:, 3],
#                          colormap='viridis', scale_factor=0.19, mode='cube', opacity=1)
# # Scaling all voxels the same size
# plt_plot.glyph.scale_mode = 'scale_by_vector'
# # Setting correct colormap
# plt_plot.module_manager.scalar_lut_manager.lut.table = SemanticKittiIO.get_cmap_semanticKITTI20()

# mlab.show()

from mayavi import mlab
import os
import numpy as np
import LMSCNet.data.io_data as SemanticKittiIO

scale_divide = 1

label_file = '/home/jmwang/LMSCNet/000000.label'
yaml_file = '/home/jmwang/LMSCNet/LMSCNet/data/semantic-kitti.yaml'

def Vis_SemanticKITTI_Label(label_file, yaml_file):
    # Read label data
    LABEL = SemanticKittiIO._read_label_SemKITTI(label_file)
    remap_lut = SemanticKittiIO.get_remap_lut(yaml_file)
    LABEL = remap_lut[LABEL.astype(np.uint16)].astype(np.float32)  # Remap 20 classes semanticKITTI SSC
    grid_dimensions = [256, 32, 256]
    LABEL = np.moveaxis(LABEL.reshape([int(grid_dimensions[0] / scale_divide),
                                       int(grid_dimensions[2] / scale_divide),
                                       int(grid_dimensions[1] / scale_divide)]), [0, 1, 2], [0, 2, 1])

    # Creating figure object
    figure = mlab.figure(figure='Figure', bgcolor=(1, 1, 1), size=(1200, 1920))

    # Get grid coordinates X, Y, Z
    grid_coords, _, _, _ = SemanticKittiIO.get_grid_coords([LABEL.shape[0], LABEL.shape[2], LABEL.shape[1]], 0.2)
    grid_coords = np.vstack((grid_coords.T, np.moveaxis(LABEL, [0, 1, 2], [0, 2, 1]).reshape(-1))).T
    # Obtaining voxels with semantic class
    occupied_voxels = grid_coords[(grid_coords[:, 3] > 0) & (grid_coords[:, 3] < 255)]

    # Plot as points with cube as mode, resolution is 0.2,  we set scale_factor slightly smaller
    plt_plot = mlab.points3d(occupied_voxels[:, 0], occupied_voxels[:, 1], occupied_voxels[:, 2], occupied_voxels[:, 3],
                             colormap='viridis', scale_factor=0.19, mode='cube', opacity=1)
    # Scaling all voxels the same size
    plt_plot.glyph.scale_mode = 'scale_by_vector'
    # Setting correct colormap
    plt_plot.module_manager.scalar_lut_manager.lut.table = SemanticKittiIO.get_cmap_semanticKITTI20()

    mlab.show()

def main():
    
    Vis_SemanticKITTI_Label(label_file, yaml_file)

if __name__ == "__main__":
    main()
