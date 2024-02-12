from constant import DEFAULT_PLANET_SIZE, ROBOTS_ENTITY_PREF, MAX_ROBOT_SIZE
from agarBall import AgarBall
from ursina import Vec3
from random import randint
from world import sortedAABBs, get_robots
from copy import copy

class RobotPlayer(AgarBall):
    def __init__(self, size=-1):
        if size == -1: size = randint(DEFAULT_PLANET_SIZE, MAX_ROBOT_SIZE)
        super().__init__(f"{ROBOTS_ENTITY_PREF}{len(get_robots())}", size=size)
        
        self.target = None 
        self.direction = Vec3(1,0,0)
    
    def look_at(self, target):
        tempRotation = copy(self.rotation)
        
        super().look_at(target)
        
        self.nextRotation = copy(self.rotation)
        self.rotation = tempRotation
    
    def movementHandler(self):
        self.addForce(self.forward.normalized())
        
        return super().movementHandler()
        
    def find_target(self):
        return sortedAABBs.findNearestSmaller(self)
    
    def eat(self, ball):
        if ball == self.target: self.target = None
        return super().eat(ball)
    
    def kill(self):
        RobotPlayer(size=DEFAULT_PLANET_SIZE)
        return super().kill()
        
        
    def tickUpdate(self):
        super().tickUpdate()
        
        lookAtTarget= False
        if not self.target or self.target.deleted or self.target.size > self.size:
            self.target=self.find_target()
            lookAtTarget = True
        
        elif self.target.movement:
            # si la proie bouge, regarder si elle n'est pas trop loin (a environ 10s)
            if self.dist(self.target)**0.5 >= 10 * self.speed:
                self.target= self.find_target()
            lookAtTarget= True
        
        if lookAtTarget and self.target: self.look_at(self.target)
