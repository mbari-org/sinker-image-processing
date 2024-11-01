import os
import sys
import glob
from loguru import logger
import numpy as np
from skimage.filters import scharr, gaussian
from skimage.io import imsave, imread
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.colors import Normalize

def process_frame(frame, low=0.0, high=0.1):
    
    edges_mag = scharr(frame)
    
    # scale to 8-bit
    edges_mag = 255 * (edges_mag - low) / high
    
    return edges_mag.astype(np.uint8)

if __name__=="__main__":
    
    if len(sys.argv) < 3:
        logger.error("Usage: python process_images.py [path to images with wilcard (eg. *.tiff)] [path to output]")
        exit()

    image_path = sys.argv[1]
    output_dir = sys.argv[2]

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    rawframes = sorted(glob.glob(image_path))
    
    for frame in rawframes:
        logger.info("Processing frame: " + frame)
        output_frame = process_frame(imread(frame))
        imsave(os.path.join(output_dir, os.path.basename(frame)), output_frame)

