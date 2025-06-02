'''
Define Our class which is stores collision detection and environment information here
Created on Nov 1, 2018

:author: micou(Zezhou Sun)
:version: 2021.1.1

modified by Daniel Scrivener 08/2022
'''

import math
from Point import Point
from Quaternion import Quaternion
import numpy as np


class EnvironmentObject:
    """
    Define properties and interface for a object in our environment
    """
    env_obj_list = None  # list<Environment>
    item_id = 0
    species_id = 0

    bound_radius = None
    bound_center = Point((0,0,0))

    def addCollisionObj(self, a):
        """
        Add an environment object for this creature to interact with
        """
        if isinstance(a, EnvironmentObject):
            self.env_obj_list.append(a)

    def rmCollisionObj(self, a):
        """
        Remove an environment object for this creature to interact with
        """
        if isinstance(a, EnvironmentObject):
            self.env_obj_list.remove(a)

    def animationUpdate(self):
        """
        Perform the next frame of this environment object's animation.
        """
        self.update()

    def stepForward(self):
        """
        Have this environment object take a step forward in the simulation.
        """
        return

    ##### TODO 4: Eyes on the road!
        # Requirements:
        #   1. Creatures should face in the direction they are moving. For instance, a fish should be facing the
        #   direction in which it swims. Remember that we require your creatures to be movable in 3 dimensions,
        #   so they should be able to face any direction in 3D space.
        
    def rotateDirection(self, v1, direction):
        """
        change this environment object's orientation to v1.
        :param v1: targed facing direction
        :type v1: Point
        """
        # self.setPostRotation(np.identity(4))

        current_direction = direction.normalize()
        target_direction = v1.normalize()

        rotation_axis = current_direction.cross3d(target_direction).normalize()
        dot_product = current_direction.dot(target_direction)
        rotation_angle = np.arccos(dot_product)

        sin_half_angle = np.sin(rotation_angle / 2)
        cos_half_angle = np.cos(rotation_angle / 2)

        q = Quaternion(
            cos_half_angle,
            sin_half_angle * rotation_axis.coords[0],
            sin_half_angle * rotation_axis.coords[1],
            sin_half_angle * rotation_axis.coords[2]
        )

        rotation_matrix = q.toMatrix()
        self.setPostRotation(rotation_matrix)