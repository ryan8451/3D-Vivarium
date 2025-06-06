"""
All creatures should be added to Vivarium. Some help functions to add/remove creature are defined here.
Created on 20181028

:author: micou(Zezhou Sun)
:version: 2021.1.1

modified by Daniel Scrivener
"""

import numpy as np
from Point import Point
from Component import Component
from ModelTank import Tank
from EnvironmentObject import EnvironmentObject
from ModelLinkage import Bird, Mouse



class Vivarium(Component):
    """
    The Vivarium for our animation
    """
    components = None  # List
    parent = None  # class that have current context
    tank = None
    tank_dimensions = None

    predators = None  
    prey = None  

    ##### BONUS 5(TODO 5 for CS680 Students): Feed your creature
    # Requirements:
    #   Add chunks of food to the vivarium which can be eaten by your creatures.
    #     * When ‘f’ is pressed, have a food particle be generated at random within the vivarium.
    #     * Be sure to draw the food on the screen with an additional model. It should drop slowly to the bottom of
    #     the vivarium and remain there within the tank until eaten.
    #     * The food should disappear once it has been eaten. Food is eaten by the first creature that touches it.

    def __init__(self, parent, shaderProg):
        self.parent = parent
        self.shaderProg = shaderProg

        self.tank_dimensions = [4, 4, 4]
        tank = Tank(Point((0,0,0)), shaderProg, self.tank_dimensions)
        super(Vivarium, self).__init__(Point((0, 0, 0)))

        # Build relationship
        self.addChild(tank)
        self.tank = tank

        # Store all components in one list, for us to access them later
        self.components = [tank]

        self.predators = []  # Initialize predators list
        self.prey = []       # Initialize prey list


        # self.addNewObjInTank(Linkage(parent, Point((0,0,0)), shaderProg))

        self.addNewObjInTank(Bird(parent, Point((0,0,0)), shaderProg))

        self.addNewObjInTank(Mouse(parent, Point((1,-1,0)), shaderProg))
        self.addNewObjInTank(Mouse(parent, Point((-1,1,0)), shaderProg))




    def animationUpdate(self):
        """
        Update all creatures in vivarium
        """
            
        for c in self.components[::-1]:
            if isinstance(c, EnvironmentObject):
                c.animationUpdate()
                c.stepForward(self.components, self.tank_dimensions, self)
        
        self.update()

    def delObjInTank(self, obj):
        if isinstance(obj, Component):
            if obj in self.tank.children:
                self.tank.children.remove(obj)
            else:
                print("Warning: Object not found in tank.children")

            # Remove from components if it exists
            if obj in self.components:
                self.components.remove(obj)
            else:
                print("Warning: Object not found in components")

            # Remove from predators or prey lists if applicable
            if isinstance(obj, Bird) and obj in self.predators:
                self.predators.remove(obj)
            elif isinstance(obj, Mouse) and obj in self.prey:
                self.prey.remove(obj)
            del obj

    def addNewObjInTank(self, newComponent):
        if isinstance(newComponent, Component):
            self.tank.addChild(newComponent)
            self.components.append(newComponent)
            if isinstance(newComponent, Bird):
                self.predators.append(newComponent)
            elif isinstance(newComponent, Mouse):
                self.prey.append(newComponent)
        if isinstance(newComponent, EnvironmentObject):
            # Add environment components list reference to this new object
            newComponent.env_obj_list = self.components

