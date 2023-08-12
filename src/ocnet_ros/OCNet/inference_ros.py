#!/usr/bin/env python3
# -*-coding:utf-8 -*-
import shutil
import os
import torch
import torch.nn as nn
import sys
import numpy as np
import rospy
from std_msgs.msg import Float64MultiArray
import time
repo_path, _ = os.path.split(os.path.realpath(__file__))
repo_path, _ = os.path.split(repo_path)
sys.path.append(repo_path)

from OCNet.common.seed import seed_all
from OCNet.common.config import CFG
from OCNet.common.dataset import get_dataset
from OCNet.common.model import get_model
from OCNet.common.logger import get_logger
from OCNet.common.io_tools import dict_to, _create_directory
import OCNet.common.checkpoint as checkpoint
import OCNet.data.io_data as SemanticKittiIO


def publish_coordinates(coordinates, publisher):
    coordinates_msg = Float64MultiArray()
    
    for coordinate in coordinates:
        coordinates_msg.data.extend(coordinate)
    
    publisher.publish(coordinates_msg)
    
    
    
def test(model, dset, _cfg, logger, out_path_root, coordinates_publisher):
    device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
    dtype = torch.float32
    ori_voxels_path = "/home/melodic/jetsonNX/Aerial-Walker/src/oc_navigation/plan_manage/raw_data/ori_voxels"
    model = model.to(device=device)
    logger.info('=> Passing the network on the test set...')
    model.eval()
    inv_remap_lut = dset.dataset.get_inv_remap_lut()

    start_time = time.time()
    inference_time = []

    with torch.no_grad():
        for t, (data, indices) in enumerate(dset):
            data = dict_to(data, device, dtype)

            # Record the inference start time
            inference_start_time = time.time()

            scores = model(data)
            
            # Record the inference end time
            inference_end_time = time.time()
            
            # Log the inference time of each sample
            inference_time.append(inference_end_time - inference_start_time)

            for key in scores:
                scores[key] = torch.argmax(scores[key], dim=1).data.cpu().numpy()

            curr_index = 0
            for score in scores['pred_semantic_1_1']:
                 # voxel occupancy file
                input_filename = dset.dataset.filepaths['3D_OCCUPANCY'][indices[curr_index]]
                print(input_filename)

                # Read the voxel occupancy from the file
                voxel_occupancy = SemanticKittiIO._read_occupancy_SemKITTI(input_filename)

                # Reshape the voxel occupancy array to the correct dimensions
                voxel_occupancy = voxel_occupancy.reshape(256, 32, 256)

                # Create a mask for occupied voxels
                voxel_mask = voxel_occupancy.ravel() == 1

                # Count the occupied voxels in the voxel file
                voxel_occupied_count = np.count_nonzero(voxel_mask)

                # Create a mask for occupied voxels in scores
                score_mask = score.ravel() > 0

                # Count the occupied voxels in scores
                score_occupied_count = np.count_nonzero(score_mask)

                # Compute the intersection of occupied voxels in both score and voxel_occupancy
                intersection = np.logical_and(voxel_mask, score_mask)

                # Count the intersected occupied voxels
                intersection_count = np.count_nonzero(intersection)

                # Compute the non-intersected occupied voxels coordinates in voxel_occupancy
                non_intersection = np.logical_and(score_mask, np.logical_not(voxel_mask))

                # Get the non-intersected occupied voxel coordinates
                non_intersection_coordinates = np.column_stack(np.nonzero(non_intersection.reshape(256, 32, 256)))

                print("Voxel occupancy occupied count:", voxel_occupied_count)
                print("Score occupied count:", score_occupied_count)
                print("Intersection occupied count:", intersection_count)
                print("Non-intersection (voxel_occupancy not occupied but score occupied) count:", len(non_intersection_coordinates))
                print("Non-intersection coordinates:")
                print(non_intersection_coordinates.shape)
                
                
                publish_coordinates(non_intersection_coordinates, coordinates_publisher)
                
                score = np.moveaxis(score, [0, 1, 2], [0, 2, 1]).reshape(-1).astype(np.uint16)
                score = inv_remap_lut[score].astype(np.uint16)
                
              
                filename, extension = os.path.splitext(os.path.basename(input_filename))
                sequence = os.path.dirname(input_filename).split('/')[-2]
                out_filename = os.path.join(out_path_root, 'predictions', filename + '.label')
                _create_directory(os.path.dirname(out_filename))
                score.tofile(out_filename)
                shutil.copy(input_filename, ori_voxels_path)
                os.remove(input_filename)
                #logger.info('=> Sequence {} - File {} saved'.format(sequence, os.path.basename(out_filename)))
                curr_index += 1
    # Calculate the average FPS for all samples
    avg_fps = len(dset) / np.sum(inference_time)
    logger.info('Average Inference FPS: {:.2f}'.format(avg_fps))
    elapsed_time = time.time() - start_time
    
    return


def main():
    rospy.init_node("inference_node")
    #Create the publisher using a specific ROS message type and topic
    coordinates_publisher = rospy.Publisher('/non_intersection_coordinates', Float64MultiArray, queue_size=10)

    
    torch.backends.cudnn.enabled = False
    seed_all(0)

    weights_f = rospy.get_param('~weights_file')
    dataset_f = rospy.get_param('~dataset_root')
    out_path_root = rospy.get_param('~output_path')

    assert os.path.isfile(weights_f), '=> No file found at {}'

    checkpoint_path = torch.load(weights_f)
    config_dict = checkpoint_path.pop('config_dict')
    config_dict['DATASET']['ROOT_DIR'] = dataset_f

    _cfg = CFG()
    _cfg.from_dict(config_dict)
    logger = get_logger(out_path_root, 'logs_test.log')
    logger.info('============ Test weights: "%s" ============\n' % weights_f)
    
   
    while not rospy.is_shutdown():
        
        dataset = get_dataset(_cfg)['test']
        logger.info('=> Loading network architecture...')
        model = get_model(_cfg, dataset.dataset)
        if torch.cuda.device_count() > 1:
            model = nn.DataParallel(model)
            model = model.module

        logger.info('=> Loading network weights...')
        model = checkpoint.load_model(model, weights_f, logger)

        rate = rospy.Rate(10)
        
        test(model, dataset, _cfg, logger, out_path_root, coordinates_publisher)
       
        logger.info('=> ============ Network Test Done ============')
        rate.sleep()


if __name__ == '__main__':
    main()