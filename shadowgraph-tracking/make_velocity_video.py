import os
import sys
import cv2
import pims
from loguru import logger
import numpy as np
import trackpy as tp
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.colors import Normalize
from scipy.signal import savgol_filter

if __name__=="__main__":

    if len(sys.argv) < 2:
        logger.error("Usage: python make_velocitiy_video.py [path to images with wildcard (eg. *.tiff)]")
        exit()

    image_path = sys.argv[1]

    if not os.path.exists('velocities.csv'):

        # load tracks
        if os.path.exists('filtered_tracks.csv'):
            t = pd.read_csv('filtered_tracks.csv')
        else:
            t = pd.read_csv('tracks.csv')
            
            # filter spurious tracks
            t = tp.filter_stubs(t, 60)
            
            # filter the particle tracks
            for item in set(t.particle):
                logger.info("Filerting particle: " + str(item))
                t.loc[t.particle==item,'x'] = savgol_filter(t[t.particle==item].x, window_length=11, polyorder=1)
                t.loc[t.particle==item,'y'] = savgol_filter(t[t.particle==item].y, window_length=11, polyorder=1)

            # Save out filtered tracks
            t.to_csv('filtered_tracks.csv')

        # Compute velocities
        data = pd.DataFrame()
        for item in set(t.particle):
            sub = t[t.particle==item]
            dvx = np.diff(sub.x)
            dvy = np.diff(sub.y)
            for x, y, dx, dy, frame in zip(sub.x[:-1], sub.y[:-1], dvx, dvy, sub.frame[:-1],):
                logger.info("frame: " +str(frame) + ", particle: " + str(item))
                data = pd.concat([data, pd.DataFrame([{'dx': dx,
                                    'dy': dy,
                                    'x': x,
                                    'y': y,
                                    'frame': frame,
                                    'particle': item,
                                    }])], axis=0)

        # save out of the data frame of velocities
        data.to_csv('velocities.csv')
        
    else:
        
        data = pd.read_csv('velocities.csv')

    # load a frame
    rawframes = pims.open(image_path)

    output_dir = 'output_frames_v2'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
            
    for i in range(0,12000):
        logger.info("Visualizing frame: " + str(i))
        d = data[data.frame==i]
        fig, ax = plt.subplots()
        plt.imshow(rawframes[i], cmap='gray', vmin=0, vmax=255)
        colormap = cm.viridis
        colors = 24.0 * 3600 *10 * np.sqrt(d.dx**2 + d.dy**2) / 1000000 # displacement in m/d
        norm = Normalize(vmin=0, vmax=25)
        plt.quiver(d.x, d.y, d.dx, -d.dy, color=colormap(norm(colors)), scale_units='xy', scale=0.1, pivot='tail', width=.0008, headwidth=5, headlength=5)
        #plt.axis('off')
        cbar = fig.colorbar(cm.ScalarMappable(norm=norm, cmap=colormap), ax=ax)
        cbar.set_label('Estimated speed (m/d)')
        #plt.show()
        plt.savefig(os.path.join(output_dir,"viz_particles_frame_%06d.png" % i), dpi=300)
        plt.close(fig)