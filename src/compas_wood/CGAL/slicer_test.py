import os
import numpy as np

from compas_view2.app import App
from compas_view2.objects import Collection

from compas.geometry import Point
from compas.geometry import Vector
from compas.geometry import Plane
from compas.geometry import Polyline
from compas.datastructures import Mesh

from compas_wood import HERE #?
from compas_wood.CGAL import slicer



def test_slicer():

    print("Start")
    FILE = os.path.join(HERE,  'data', '3DBenchy.stl')#'../..',


    # ==============================================================================
    # Get benchy and construct a mesh
    # ==============================================================================

    benchy = Mesh.from_stl(FILE)

    # ==============================================================================
    # Create planes
    # ==============================================================================

    # replace by planes along a curve

    bbox = benchy.bounding_box()

    x, y, z = zip(*bbox)
    zmin, zmax = min(z), max(z)

    normal = Vector(0, 0, 1)
    planes = []
    for i in np.linspace(zmin, zmax, 50):
        plane = Plane(Point(0, 0, i), normal)
        planes.append(plane)



    # ==============================================================================
    # Slice
    # ==============================================================================

    M = benchy.to_vertices_and_faces()


    pointsets = slicer.slice_mesh(M, planes)


    # ==============================================================================
    # Process output
    # ==============================================================================

    polylines = []
    for points in pointsets:
        points = [Point(*point) for point in points]
        print(points[0])
        polyline = Polyline(points)
        polylines.append(polyline)
    print(len(polylines))

    print("End")
    return polylines


result = test_slicer()
#viewer
viewer = App(show_grid=False,width = 3840,height = 2160-250)
viewer.add(Collection(result),color = (0, 0, 0.0), linewidth = 1)
viewer.run()


