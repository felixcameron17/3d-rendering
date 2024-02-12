from pywavefront import Wavefront
import numpy as np

light_direction = np.array([1, 1, 1])
view_direction = np.array([0, 0, -1])
ambient_colour = np.array([50, 50, 50])
diffuse_colour = np.array([255, 255, 255])
specular_colour = np.array([255, 255, 255])
shininess = 32

def num_to_rgb(num):
    # Ensure the number is within the valid range
    num = max(1, min(num, 16777216))

    # Convert the number to RGB components
    blue = (num - 1) % 256
    green = ((num - 1) // 256) % 256
    red = ((num - 1) // 65536) % 256

    return (red, green, blue)

def read_dot_obj(file):
    obj = Wavefront(file, create_materials=True, collect_faces=True)
    verts_ = obj.vertices
    faces_ = []

    for mesh in obj.mesh_list:
        if hasattr(mesh, 'faces'):
            faces_.extend(mesh.faces)

    return verts_, faces_