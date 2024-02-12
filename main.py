from math import *
import pygame as pg
import numpy as np
from pywavefront import Wavefront
from funcs import *
import time

def main():
    class Shape:
        def __init__(self, shape):
            verts_y = []
            self.shape = shape
            verts, faces = read_dot_obj('objs\\' + self.shape + '.obj')
            self.faces = np.array(faces)
            self.verts = np.array(verts)
            self.verts = self.verts.reshape(-1, 3)
            self.clr = (0, 128, 0)
            for vert in self.verts:
                verts_y.append(vert[1])

                y_offset = (max(verts_y) - min(verts_y)) / 2

            for i, vert in enumerate(self.verts):
                self.verts[i][1] -= y_offset

        
        def depth_sort(self):
            face_depths = np.empty(len(self.faces))
            for i, face in enumerate(self.faces):
                try:
                    face_verts = self.verts[face]
                    face_depths[i] = np.mean(face_verts[:, 2])
                except:
                    print('index:', i)

            sorted_indices = np.argsort(face_depths)

            return self.faces[sorted_indices]

    model = Shape('teapot')

    model.verts = model.verts.reshape(-1, 3)

    if vars:
        # constant variables
        WIDTH, HEIGHT = 800, 600
        CIRCLE_POS = [WIDTH/2, HEIGHT/2]
        DRAW_POINTS = False


        # pygame variables
        pg.display.set_caption('3D projection')
        screen = pg.display.set_mode((WIDTH, HEIGHT))
        clock = pg.time.Clock()
        running = True

        # vars
        scale = 100
        scale_apply = 0
        angle = 0
        verts = []
        y_offest = 0

        verts_x, verts_y, verts_z = [], [], []

        angle_x = 0
        angle_y = 0
        angle_z = 0

        x_input = 0
        y_input = 0
        z_input = 0

        # projection matrix. this is a constant variable
        PROJECTION_MATRIX = np.matrix([
            [1, 0, 0],
            [0, 1, 0]
        #   [0, 0, 0] but its not needed to compute as it is all zeroes
        ])

        # initialize list for x, y cords to display on screen
        projected_verts = [
            [n, n] for n in range(len(model.verts))
        ]


    while running:
        # check if 'game' ended
        clock.tick(60)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_a or event.key == pg.K_LEFT:
                    angle_y -= 0.05
                elif event.key == pg.K_d or event.key == pg.K_RIGHT:
                    angle_y += 0.05
                elif event.key == pg.K_w or event.key == pg.K_UP:
                    angle_x += 0.05
                elif event.key == pg.K_s or event.key == pg.K_DOWN:
                    angle_x -= 0.05
                elif event.key == pg.K_q:
                    angle_z += 0.05
                elif event.key == pg.K_e:
                    angle_z -= 0.05
                elif event.key == pg.K_z:
                    scale += 1
                elif event.key == pg.K_x:
                    scale -= 1
                elif event.key == pg.K_ESCAPE:
                    pg.quit()
            if event.type == pg.KEYUP:
                angle_x, angle_y, angle_z = angle_x, angle_y, angle_z


    
        rot_x = np.matrix([ # rotation matrix for x axis
            [1,            0,             0],
            [0, cos(angle_x), -sin(angle_x)],
            [0, sin(angle_x),  cos(angle_x)]
        ])

        rot_y = np.matrix([ # rotation matrix for y axis
            [cos(angle_y),  0, sin(angle_y)],
            [0,             1,            0],
            [-sin(angle_y), 0, cos(angle_y)]
        ])

        rot_z = np.matrix([ # rotation matrix for z axis
            [cos(angle_z), -sin(angle_z), 0],
            [sin(angle_z),  cos(angle_z), 0],
            [           0,             0, 1]
        ])


        screen.fill((225, 255, 245))


        for i, point in enumerate(model.verts):
            rotated2d = rot_x @ rot_y @ rot_z @ point.reshape((3, 1))
            projected2d = PROJECTION_MATRIX @ rotated2d


            x = int(projected2d[0][0] * scale) + CIRCLE_POS[0]
            y = -int(projected2d[1][0] * scale) + CIRCLE_POS[1]

            projected_verts[i] = [x, y]
            model.verts[i] = rotated2d.reshape(3,)
            if DRAW_POINTS == True:
                pg.draw.circle(screen, 'BLACK', projected_verts[i], 2)

        sorted_faces = model.depth_sort()

        for i, face in enumerate(sorted_faces):
            triangle = ((projected_verts[sorted_faces[i][0]]), (projected_verts[sorted_faces[i][1]]), (projected_verts[sorted_faces[i][2]]))

            green = i / len(sorted_faces) * 100 + 155
            pg.draw.polygon(screen, (0, green,  255-green), triangle, 0)

        pg.display.update()


main()