import numpy as np
from compas.plugins import plugin


#Import module from folder instead of using -> from _cgal import slicer

import sys
folder = "C:/IBOIS57/_Code/Software/Python/Pybind11Example/vsstudio/Release/"
if folder not in sys.path:
    sys.path.append(folder)
import pybind11module


@plugin(category='trimesh', pluggable_name='trimesh_slice')
def slice_mesh(mesh, planes):
    """Slice a mesh by a list of planes.
    Parameters
    ----------
    mesh : tuple of vertices and faces
        The mesh to slice.
    planes : list of (point, normal) tuples or compas.geometry.Plane
        The slicing planes.
    Returns
    -------
    list of arrays
        The points defining the slice polylines.
    """
    vertices, faces = mesh
    points, normals = zip(*planes)
    V = np.asarray(vertices, dtype=np.float64)
    F = np.asarray(faces, dtype=np.int32)
    P = np.array(points, dtype=np.float64)
    N = np.array(normals, dtype=np.float64)

    pybind11module.say_hello()
    pointsets = pybind11module.slicerCGAL.slice_meshCGAL(V, F, P, N)
    return pointsets

