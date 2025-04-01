import numpy as np
from .libcpp import pypne_cpp


def pnextract(image,resolution=1.):
    image = image.astype(np.uint8)
    nz,ny,nx = image.shape
    res = pypne_cpp.pnextract(nx,ny,nz,resolution,image.reshape(-1))
    image_VElems = res['VElems'].reshape(nz+2,ny+2,nx+2)
    pn = res['pn']
    return image_VElems,pn