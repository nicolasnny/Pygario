from agarBall import AgarBall
from random import randint
from constant import MIN_BLACK_HOLE_SIZE, MAX_BLACK_HOLE_SIZE, BLACK_HOLE_ROTATION_SPEED, BLACKHOLES_ENTITY_PREF
from world import get_blackholes
from texture import give_texture

class BlackHole(AgarBall):
    
    def __init__(self, size=-1) -> None: 
        if size == -1: size = randint(MIN_BLACK_HOLE_SIZE, MAX_BLACK_HOLE_SIZE)
        name = f"{BLACKHOLES_ENTITY_PREF}{len(get_blackholes())}"
        
        super().__init__(name, texture=give_texture("blackhole"), size=size)
        
        
    def movementHandler(self):
        self.rotation_y += BLACK_HOLE_ROTATION_SPEED
        
    def eat(self, ball):return
