# warp image

import cv2
import os
import numpy as np
from plantcv.plantcv import print_image
from plantcv.plantcv import plot_image
from plantcv.plantcv import fatal_error
from plantcv.plantcv import color_palette
from plantcv.plantcv import params


def warp(img, refimg, pts, refpts, method='default'):
    """Warp an image to another perspective

    Inputs:
    img = grayscale or binary image data to be warped
    refimg = RGB or grayscale image data to be used as reference
    pts = 4 coordinates on img1
    refpts = 4 coordinates on img2
    method = method of finding the transformation. 'default', 'ransac', 'lmeds', 'rho'
    Returns:
    warped_img = warped image

    :param img: numpy.ndarray
    :param refimg: numpy.ndarray
    :param pts: list of tuples
    :param refpts: list of tuples
    :param method: str
    :return warped_img: numpy.ndarray
    """

    params.device += 1

    if len(pts)<4 and len(refpts)<4:
        fatal_error('Please provide 4 pairs of corresponding coordinates.')
    if len(img.shape)>2:
        fatal_error('The input `img` should be grayscale or binary.')

    methods = {
        'default': 0,
        'ransac': cv2.RANSAC,
        'lmeds': cv2.LMEDS,
        'rho': cv2.RHO}

    shape_ref = refimg.shape
    rows_ref, cols_ref = shape_ref[0:2]
    # scale marker_size and line_thickness for different resolutions
    rows_img = img.shape[0]
    if rows_img > rows_ref:
        res_ratio_i = int(np.ceil(rows_img/rows_ref)) #ratio never smaller than 1 with np.ceil
        res_ratio_r = 1
    else:
        res_ratio_r = int(np.ceil(rows_ref/rows_img))
        res_ratio_i = 1
    # marker colors
    colors = color_palette(len(pts))

    img2 = img.copy()
    img2 = cv2.merge((img2, img2, img2))
    for i, pt in enumerate(pts):
        cv2.drawMarker(img2, pt, color=colors[i],
                       markerType=cv2.MARKER_CROSS,
                       markerSize=params.marker_size*res_ratio_i,
                       thickness=params.line_thickness*res_ratio_i)

    refimg2 = refimg.copy()
    if len(shape_ref)==2:
        refimg2 = cv2.merge((refimg2, refimg2, refimg2))
    for i, pt in enumerate(refpts):
        cv2.drawMarker(refimg2, pt, color=colors[i],
                       markerType=cv2.MARKER_CROSS,
                       markerSize=params.marker_size*res_ratio_r,
                       thickness=params.line_thickness*res_ratio_r)

    ptsarr = np.array(pts, dtype='float32')
    refptsarr = np.array(refpts, dtype='float32')

    M, S = cv2.findHomography(ptsarr, refptsarr, method=methods.get(method))
    warped_img = cv2.warpPerspective(src=img, M=M, dsize=(cols_ref, rows_ref))

    if params.debug != None:
        if len(np.unique(img))==2:
            # i was trying to get a blend effect in the debug output but I can' figure out how to get that when img is an rgb image. if refimg is a grayscale then it happens automatically.
            # nothing new happens if dividing by 1
            warped_blend = np.divide(warped_img, 1, out=np.zeros_like(warped_img), casting='unsafe')
        else:
            warped_blend = warped_img
        if len(refimg.shape)==2:
            imgadd = cv2.add(refimg, warped_blend)
        else:
            warped_blend3 = cv2.merge((warped_blend, warped_blend, warped_blend))
            imgadd = cv2.add(refimg, warped_blend3)
        if params.debug == 'plot':
            plot_image(img2)
            plot_image(refimg2)
            plot_image(imgadd)
        if params.debug == 'print':
            print_image(img2, os.path.join(params.debug_outdir, str(params.device) + "_img-to-warp.png"))
            print_image(refimg2, os.path.join(params.debug_outdir, str(params.device) + "_img-ref.png"))
            print_image(imgadd, os.path.join(params.debug_outdir, str(params.device) + "_warp_overlay.png"))

    return warped_img