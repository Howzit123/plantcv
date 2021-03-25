#!/usr/bin/env python
# coding: utf-8

# In[1]:


import argparse
import os
import sys
sys.path.append('/Users/garethtate/plantcv')
import numpy as np
import cv2
from matplotlib import pyplot as plt
from plantcv import plantcv as pcv

def options():
    parser = argparse.ArgumentParser(description="Imaging processing with PlantCV.")
    parser.add_argument("-i", "--image", help="Input image file.", required=True)
    parser.add_argument("-r","--result", help="Result file.", required= True )
    parser.add_argument("-o", "--outdir", help="Output directory for image files.", required=False)
    parser.add_argument("-w","--writeimg", help="Write out images.", default=False, action="store_true")
    parser.add_argument("-D", "--debug", help="Turn on debug, prints intermediate images.")
    args = parser.parse_args()
    return args

def main():
    # Get options
    args = options()

    # Set variables
    pcv.params.debug = args.debug     # Replace the hard-coded debug with the debug flag
    img_file = args.image             # Replace the hard-coded input image with image flag
    
    # Put workflow
    # steps from
    # Jupyter here

    # Print data that gets collected into the Outputs
    pcv.print_results(args.result)
    

if __name__ == '__main__':
    main()



# In[ ]:




