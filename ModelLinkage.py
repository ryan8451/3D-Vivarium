"""
Model our creature and wrap it in one class
First version at 09/28/2021

:author: micou(Zezhou Sun)
:version: 2021.2.1

Modified by Daniel Scrivener 08/2022
"""
import random

from Component import Component
from Shapes import Cube
from Shapes import Sphere
from Shapes import Cone
from Shapes import Cylinder

from Quaternion import Quaternion



from Point import Point
import ColorType as Ct
from EnvironmentObject import EnvironmentObject

try:
    import OpenGL

    try:
        import OpenGL.GL as gl
        import OpenGL.GLU as glu
    except ImportError:
        from ctypes import util

        orig_util_find_library = util.find_library


        def new_util_find_library(name):
            res = orig_util_find_library(name)
            if res:
                return res
            return '/System/Library/Frameworks/' + name + '.framework/' + name


        util.find_library = new_util_find_library
        import OpenGL.GL as gl
        import OpenGL.GLU as glu
except ImportError:
    raise ImportError("Required dependency PyOpenGL not present")

##### TODO 1: Construct your two different creatures
# Requirements:
#   1. For the basic parts of your creatures, feel free to use routines provided with the previous assignment.
#   You are also free to create your own basic parts, but they must be polyhedral (solid).
#   2. The creatures you design should have moving linkages of the basic parts: legs, arms, wings, antennae,
#   fins, tentacles, etc.
#   3. Model requirements:
#         1. Predator: At least one (1) creature. Should have at least two moving parts in addition to the main body
#         2. Prey: At least two (2) creatures. The two prey can be instances of the same design. Should have at
#         least one moving part.
#         3. The predator and prey should have distinguishable different colors.
#         4. You are welcome to reuse your PA2 creature in this assignment.

class Bird(Component, EnvironmentObject):

    components = None
    rotation_speed = None
    translation_speed = None

    def __init__(self, parent, position, shaderProg):
        super(Bird, self).__init__(position)
        
        # Define body and wings specifically for Bird
        body = ModelBirdBody(parent, Point((0, 0, 0)), shaderProg, 0.1)
        wing1 = ModelBirdWing(parent, Point((0, 0, 0)), shaderProg, 0.1)
        wing1.setDefaultAngle(180, wing1.uAxis)
        wing2 = ModelBirdWing(parent, Point((0, 0, 0)), shaderProg, 0.1)
        wing2.setDefaultAngle(180, wing2.uAxis)
        wing2.setDefaultAngle(180, wing2.vAxis)

        # Set up components, children, and specific properties for Bird
        self.components = wing1.components + wing2.components
        self.addChild(body)
        self.addChild(wing1)
        self.addChild(wing2)
        
        # Rotation speeds for wing flapping
        self.rotation_speed = []
        for comp in self.components:

            comp.setRotateExtent(comp.uAxis, 0, 20)
            comp.setRotateExtent(comp.vAxis, -45, 45)
            comp.setRotateExtent(comp.wAxis, -45, 45)
            self.rotation_speed.append([0.75, 0, 0])
        
        self.translation_speed = Point([random.random()-0.5 for _ in range(3)]).normalize() * 0.01

        self.bound_center = Point((0, 0, 0))
        self.bound_radius = 0.1 * 4
        self.species_id = 1


        self.direction = Point((1, 0, 0)).normalize()
        self.speed = 0.01

    def animationUpdate(self):
        ##### TODO 2: Animate your creature!
        # Requirements:
        #   1. Set reasonable joints limit for your creature
        #   2. The linkages should move back and forth in a periodic motion, as the creatures move about the vivarium.
        #   3. Your creatures should be able to move in 3 dimensions, not only on a plane.

        # create periodic animation for creature joints
        for i, comp in enumerate(self.components):
            comp.rotate(self.rotation_speed[i][0], comp.uAxis)
            comp.rotate(self.rotation_speed[i][1], comp.vAxis)
            comp.rotate(self.rotation_speed[i][2], comp.wAxis)
            if comp.uAngle in comp.uRange:  # rotation reached the limit
                self.rotation_speed[i][0] *= -1
            if comp.vAngle in comp.vRange:
                self.rotation_speed[i][1] *= -1
            if comp.wAngle in comp.wRange:
                self.rotation_speed[i][2] *= -1
        # self.vAngle = (self.vAngle + 3) % 360

        ##### BONUS 6: Group behaviors
        # Requirements:
        #   1. Add at least 5 creatures to the vivarium and make it possible for creatures to engage in group behaviors,
        #   for instance flocking together. This can be achieved by implementing the
        #   [Boids animation algorithms](http://www.red3d.com/cwr/boids/) of Craig Reynolds.

        self.update()

    def stepForward(self, components, tank_dimensions, vivarium):

        ##### TODO 3: Interact with the environment
        # Requirements:
        #   1. Your creatures should always stay within the fixed size 3D "tank". You should do collision detection
        #   between the creature and the tank walls. When it hits the tank walls, it should turn and change direction to stay
        #   within the tank.
        #   2. Your creatures should have a prey/predator relationship. For example, you could have a bug being chased
        #   by a spider, or a fish eluding a shark. This means your creature should react to other creatures in the tank.
        #       1. Use potential functions to change its direction based on other creatures’ location, their
        #       inter-creature distances, and their current configuration.
        #       2. You should detect collisions between creatures.
        #           1. Predator-prey collision: The prey should disappear (get eaten) from the tank.
        #           2. Collision between the same species: They should bounce apart from each other. You can use a
        #           reflection vector about a plane to decide the after-collision direction.
        #       3. You are welcome to use bounding spheres for collision detection.

        epsilon = 1e-6

        for creature in vivarium.prey:
            prey_position = creature.currentPos
            # print(prey_position)
            distance_vector = prey_position.__sub__(self.currentPos)
            distance_squared = distance_vector.norm() ** 2
            # print(distance_squared)
            self.direction = self.direction.__add__((distance_vector.__mul__ (1/((distance_squared + epsilon)**2))).__mul__(0.05))
            # print(self.direction.coords)
            
            # print(creature.bound_radius)
            # print(self.bound_radius + creature.bound_radius)
            # print(distance_squared < (self.bound_radius + creature.bound_radius))

            collision_distance = 0.1
            if distance_squared < collision_distance:
                vivarium.delObjInTank(creature)
                
        for other_bird in vivarium.predators:  
            if other_bird is not self:  
                other_position = other_bird.currentPos
                
                distance_vector = self.currentPos.__sub__(other_position)
                distance_squared = distance_vector.norm() ** 2

                self.direction = self.direction.__add__((distance_vector.__mul__(1 / (distance_squared + epsilon))).__mul__(0.01))
          

        self.direction = self.direction.normalize()

        nextPosition = self.currentPos + (self.direction * self.speed)


        hitXright =  nextPosition.coords[0] > tank_dimensions[0] / 2 - self.bound_radius
        hitXleft =  nextPosition.coords[0] < (-tank_dimensions[0]) / 2 + self.bound_radius

        hitYtop = nextPosition.coords[1] > tank_dimensions[1] / 2 - self.bound_radius
        hitYbottom = nextPosition.coords[1] < -tank_dimensions[1] / 2 + self.bound_radius

        hitZfront = nextPosition.coords[2] > tank_dimensions[2] / 2 - self.bound_radius
        hitZback = nextPosition.coords[2] < -tank_dimensions[2] / 2 + self.bound_radius

        if hitXright or hitXleft:
            self.direction.coords[0] *= -1
        if hitYtop or hitYbottom:
            self.direction.coords[1] *= -1
        if hitZfront or hitZback:
            self.direction.coords[2] *= -1

        

        self.rotateDirection(self.direction, Point([1,0,0]))

        nextPosition = self.currentPos + self.direction * self.speed
        self.setCurrentPosition(nextPosition)

        return

    


class ModelBirdBody(Component):
    """
    Define our linkage model
    """

    components = None
    contextParent = None

    def __init__(self, parent, position, shaderProg, linkageLength=0.75, display_obj=None):
        super().__init__(position)
        head1 = Cube(Point((0, 0, 0)), shaderProg, [linkageLength, linkageLength, linkageLength], Ct.GREEN)
        eye1 = Sphere(Point((0.03, 0.005, 0.02)), shaderProg, [0.03, 0.03, 0.02], Ct.WHITE)
        eyeball1 = Sphere(Point((0.05, 0.005, 0.02)), shaderProg, [0.01, 0.01, 0.01], Ct.BLACK)
        eye2 = Sphere(Point((0.03, 0.005, -0.02)), shaderProg, [0.03, 0.03, 0.02], Ct.WHITE)
        eyeball2 = Sphere(Point((0.05, 0.005, -0.02)), shaderProg, [0.01, 0.01, 0.01], Ct.BLACK)
        beak = Cone(Point((0.05, -0.01, 0.02)), shaderProg, [0.03, 0.03, 0.02], Ct.YELLOW)
        beak.setDefaultAngle(90, beak.uAxis)
        self.addChild(head1)
        head1.addChild(eye1)
        head1.addChild(eyeball1)
        head1.addChild(eye2)
        head1.addChild(eyeball2)
        head1.addChild(beak)
        self.components = [head1, eye1, eye2, beak, eyeball1, eyeball2]

class ModelBirdWing(Component):
    """
    Define our linkage model
    """

    components = None
    contextParent = None

    def __init__(self, parent, position, shaderProg, linkageLength=0.75, display_obj=None):
        super().__init__(position, display_obj)
        super().__init__(position)
        link1 = Cube(Point((0, 0, 0)), shaderProg, [linkageLength / 4, linkageLength / 4, linkageLength], Ct.GREEN)
        link2 = Cube(Point((0, 0, linkageLength)), shaderProg, [linkageLength, linkageLength / 4, linkageLength], Ct.DARKORANGE2)
        self.addChild(link1)
        link1.addChild(link2)   
        self.components = [link1, link2]    









##### TODO 1: Construct your two different creatures
# Requirements:
#   1. For the basic parts of your creatures, feel free to use routines provided with the previous assignment.
#   You are also free to create your own basic parts, but they must be polyhedral (solid).
#   2. The creatures you design should have moving linkages of the basic parts: legs, arms, wings, antennae,
#   fins, tentacles, etc.
#   3. Model requirements:
#         1. Predator: At least one (1) creature. Should have at least two moving parts in addition to the main body
#         2. Prey: At least two (2) creatures. The two prey can be instances of the same design. Should have at
#         least one moving part.
#         3. The predator and prey should have distinguishable different colors.
#         4. You are welcome to reuse your PA2 creature in this assignment.

class Mouse(Component, EnvironmentObject):
    """A mouse creature with body, ears, and tail."""
    def __init__(self, parent, position, shaderProg):
        super(Mouse, self).__init__(position)
        
        # Define body and tail for the mouse
        body = ModelMouseBody(parent, Point((0, 0, 0)), shaderProg, 0.2)
        tail = ModelMouseTail(parent, Point((-0.2, 0, 0)), shaderProg, 0.1)  

        # Set up components
        self.components = tail.components
        self.addChild(body)
        self.addChild(tail)
        
        # Set up animation properties for tail wiggle
        self.rotation_speed = [[0, 0, 0] for _ in self.components]  # Default rotation speeds for components
        # tail_index = len(tail.components)  # Index of the tail component in self.components
        self.rotation_speed[0] = [0, 0, 1]  # Set rotation speed for tail wiggle

        # Movement properties
        self.translation_speed = Point([random.random() - 0.5 for _ in range(3)]).normalize() * 0.01
        self.bound_radius = 0.4
        self.species_id = 2
        self.direction = Point((1, 0, 0)).normalize()
        self.speed = 0.01

    def animationUpdate(self):
        """Animate the mouse by moving its tail periodically."""
        for i, comp in enumerate(self.components):
            comp.rotate(self.rotation_speed[i][0], comp.uAxis)
            comp.rotate(self.rotation_speed[i][1], comp.vAxis)
            comp.rotate(self.rotation_speed[i][2], comp.wAxis)
            if i == len(self.components) - 1:  
                if comp.wAngle in comp.wRange:
                    self.rotation_speed[i][2] *= -1
        self.update()

    def stepForward(self, components, tank_dimensions, vivarium):
        """Move the mouse within the tank while avoiding walls."""
        epsilon = 1e-6

        for predator in vivarium.predators:  
            predator_position = predator.currentPos
            
            distance_vector = self.currentPos.__sub__(predator_position).__mul__(2)
            distance_squared = distance_vector.norm() ** 2
            
            self.direction = self.direction.__add__(
                (distance_vector.__mul__(1 / (distance_squared + epsilon))).__mul__(0.01)
            )

        self.direction = self.direction.normalize()



        nextPosition = self.currentPos + (self.direction * self.speed)

        # Collision detection with tank walls
        hitXright = nextPosition.coords[0] > tank_dimensions[0] / 2 - self.bound_radius
        hitXleft = nextPosition.coords[0] < (-tank_dimensions[0]) / 2 + self.bound_radius
        hitYtop = nextPosition.coords[1] > tank_dimensions[1] / 2 - self.bound_radius
        hitYbottom = nextPosition.coords[1] < -tank_dimensions[1] / 2 + self.bound_radius
        hitZfront = nextPosition.coords[2] > tank_dimensions[2] / 2 - self.bound_radius
        hitZback = nextPosition.coords[2] < -tank_dimensions[2] / 2 + self.bound_radius

        if hitXright or hitXleft:
            self.direction.coords[0] *= -1
        if hitYtop or hitYbottom:
            self.direction.coords[1] *= -1
        if hitZfront or hitZback:
            self.direction.coords[2] *= -1

        nextPosition = self.currentPos + (self.direction * self.speed)
        self.rotateDirection(self.direction, Point([1,0,0]))
        # Set new position
        self.setCurrentPosition(nextPosition)


class ModelMouseBody(Component):
    """Define the body structure of the Mouse."""
    def __init__(self, parent, position, shaderProg, bodyLength=0.2):
        super().__init__(position)
        body = Sphere(Point((0, 0, 0)), shaderProg, [bodyLength / 2, bodyLength / 2, bodyLength / 2], Ct.GRAY)
        head = Sphere(Point((0.15, 0, 0)), shaderProg, [bodyLength / 2, bodyLength / 2, bodyLength / 2], Ct.GRAY)

        # Eyes
        eye1 = Sphere(Point((0.18, 0.05, 0.05)), shaderProg, [0.02, 0.02, 0.02], Ct.BLACK)
        eye2 = Sphere(Point((0.18, 0.05, -0.05)), shaderProg, [0.02, 0.02, 0.02], Ct.BLACK)

        eye1 = Sphere(Point((0.08, 0.025, 0.05)), shaderProg, [0.02, 0.02, 0.02], Ct.BLACK)
        eye2 = Sphere(Point((0.08, 0.025, -0.05)), shaderProg, [0.02, 0.02, 0.02], Ct.BLACK)

        # Nose
        nose = Sphere(Point((0.1, 0, 0)), shaderProg, [0.01, 0.01, 0.01], Ct.PINK)

        # Ears
        ear1 = Sphere(Point((0.05, 0.03, 0.08)), shaderProg, [0.05, 0.05, 0.02], Ct.GRAY)
        ear2 = Sphere(Point((0.05, 0.03, -0.08)), shaderProg, [0.05, 0.05, 0.02], Ct.GRAY)

        # Set up hierarchy
        self.addChild(body)
        body.addChild(head)
        head.addChild(eye1)
        head.addChild(eye2)
        head.addChild(nose)
        head.addChild(ear1)
        head.addChild(ear2)
        self.components = [body, head, eye1, eye2, nose, ear1, ear2]

class ModelMouseTail(Component):
    """Define a tail for the Mouse."""
    def __init__(self, parent, position, shaderProg, tailLength=0.3):
        super().__init__(position)
        tail = Cylinder(Point((0.1, 0, 0)), shaderProg, [tailLength, 0.02, 0.02], Ct.PINK)
        tail.setRotateExtent(tail.wAxis, -20, 20)  # Set rotation extent for tail wiggle
        self.addChild(tail)
        self.components = [tail]