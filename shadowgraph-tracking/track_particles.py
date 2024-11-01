import cv2
import sys
import pims
import trackpy as tp
from loguru import logger
from skimage.io import imread, imsave
import matplotlib.pyplot as plt

minmass = 250
diameter = 7
threshold = 20
max_displacement = 50
memory = 3

def run_settings_test(image_path):
    test_image = image_path
    
    img = imread(test_image)
    
    f = tp.locate(img, diameter=diameter, minmass=minmass, threshold=threshold)
    
    plt.figure()  # make a new figure
    tp.annotate(f, img)
    plt.show()


if __name__=="__main__":
    
    if len(sys.argv) < 2:
        logger.error("Usage: python track_particles.py [path to processed images with wildcard (eg. *.tiff)]")
        exit()

    # load images 
    frames = pims.open(sys.argv[1])

    # locate particles
    f = tp.batch(frames, diameter=diameter, minmass=minmass, threshold=threshold)

    # track particles
    t = tp.link(f, max_displacement, memory=memory)

    # save results
    f.to_csv("frames.csv")
    t.to_csv("tracks.csv")
