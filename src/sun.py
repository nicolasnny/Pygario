from ursina import Entity, PointLight, cos, sin, Vec3, color
from ursina.shaders import colored_lights_shader
from constant import SUN_ROTATION_SPEED, SUN_SIZE, MAP_DIMENTION, SUN_DISTANCE, \
                     SUN_HEIGHT, SUN_SPEED, SUN_ENTITY_PREF, LIGHT_ENTITY_PREF, PYGARIO_UI_SUF
from texture import give_texture

class Sun(Entity):
    
    def __init__(self):
        
        # cree une lumiere de la meme couleur que celle du soleil
        self.light = PointLight(parent = self, color=color.rgb(253.01, 250.99, 211.01), name=f"{LIGHT_ENTITY_PREF}sun{PYGARIO_UI_SUF}")
        
        super().__init__(True, model='sphere', texture=give_texture("sun"),
                        scale=(SUN_SIZE, SUN_SIZE, SUN_SIZE),
                        position=Vec3(0,SUN_HEIGHT,MAP_DIMENTION["cotes"][1] + SUN_DISTANCE),
                        shader=colored_lights_shader, name=SUN_ENTITY_PREF+PYGARIO_UI_SUF)
        
        # calculs pour la rotation du soleil
        self.cos = cos(SUN_SPEED)
        self.sin = sin(SUN_SPEED)
        
        
        
    def move(self):
        # faire tourner le soleil autour du centre en utilisant une matrice de rotaion
        self.position = Vec3(self.position.x * self.cos + self.position.z * self.sin,
                            self.position.y,
                            self.position.z * self.cos - self.position.x * self.sin)
        
        # faire bouger la lumiere egalement
        self.light.x = self.x
        self.light.y = self.y
        
        self.rotation_y += SUN_ROTATION_SPEED