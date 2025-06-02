Name: Ryan Chen
Collaborators: Thomas Quan, Aparna Signh 
Class: CS480

Summary: 

1. ModelLinkage.py: In the ModelLinkage file I implemented two different classes in which the predator as a bird and the prey as a mouse.
The bird is built with a body and flapping wings which was taken from the original linkage model taken, animating it as it actively chases
the mouse. Using potential functions, it adjusts its direction based on the Mouse’s position, aiming to capture it, while avoiding the tank 
walls through collision detection. When the Bird closes in on the Mouse, it triggers the Mouse’s removal, simulating a capture. he Mouse, 
acting as the prey, features a rounded body, expressive eyes, and a wagging tail. It moves within the tank, reacting to the Bird’s 
approach by adjusting its course in an attempt to evade capture.

Specfic function:
- animationUpdate: adjusted the original movement of the squid to fit my model and nothing else change
- stepForward: calculates the potential function, detect tank walls, check if the creature collides with one another and have different
interaction base on who it collides with (Eats mouse if it collides and avoid other birds)
- rotateDirection: used here but not coded here but handles the direction its facing

2. Vivarium: Added the creatures and created prey and predator list to manage the amount of predator and prey there is

3. Sketch: Added the different binding for the reset and a scene that contains one predator and prey

4. EnvironmentObject: The rotateDirection helps an object to face a target direction v1 using quaternion rotation. 
It first normalizes both the current direction and the target direction. Then, it calculates a rotation axis from the 
cross product of these directions and the rotation angle using their dot product. A quaternion is created using this angle and axis, 
converted into a 4x4 rotation matrix, and applied setPostRotation to update the object’s orientation smoothly toward v1. 
This approach ensures fluid rotation without common issues like gimbal lock.






