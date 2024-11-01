# Shadowgraph Particle Tracking

## Overview

Process shadowgraph images into particle trajectories using standard python modules and the [trackpy library](https://soft-matter.github.io/trackpy/dev/).

## Required python modules

- trackpy
- opencv-python
- loguru
- scikit-image
- scipy
- numpy
- pandas
- matplotlib
- pims

## Basic usage

1. Process raw images into edge detected images using `process_image.py`
2. Track particles in processed images using `track_particles.py`
3. Compute velocities and make video using `make_velocity_video.py`



