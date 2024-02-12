from constant import *
from random import randint
from ursina import Entity, time, Vec3, lerp, clamp, Texture, destroy, scene
from ursina.shaders import lit_with_shadows_shader, unlit_shader
from texture import give_texture_random
from world import sortedAABBs
from PIL import Image, ImageDraw
from random import choice
from time import time as t
from math import log
from audio import playAudio
from world import is_player

class AgarBall(Entity):
    def __init__(self, name, base_coordonates=[0,0,0], model="sphere",
                 texture=None, size=DEFAULT_PLANET_SIZE) -> None:
        
        if not texture:
            texture = give_texture_random(planet_only= True)
        
        super().__init__(name=name + PYGARIO_ENTITIES_SUF,
            model=model, texture=texture,
            scale=(size, size, size), position=base_coordonates,
            shader=lit_with_shadows_shader)
      
        self.size = size
        self.speed = max(FORCE_TORC - log(self.size), 5)
        self.deleted = False
        
        self.movement = False
        self.growth = False 

        self.oldPos = self.position
        self.oldSize = self.size
        self.hasChanged = False
        
        self.nextPos = self.position
        self.nextRotation = Vec3(0, 0, 0)
        self.nextSize = self.size
        
        self.lastDashTime = t()
        self.speed = max(FORCE_TORC - 4*self.size**0.5, 5)
        
        sortedAABBs.insert(self)
        
        if base_coordonates == [0,0,0]:
            self.rand_pos()

        if name.startswith(GEMS_ENTITY_PREF) or name.startswith(BLACKHOLES_ENTITY_PREF):
            self.hasPseudo = False
        else:
            if not name.startswith(PLAYER_ENTITY_NAME):
                self.pseudoStr = choice(PSEUDOS)
                self.displayPseudo(self.pseudoStr)


    def rand_pos(self):
        sortedAABBs.remove(self)

        self.x = randint(MAP_DIMENTION["abscisses"][0] + self.size,
                        MAP_DIMENTION["abscisses"][1] - self.size) \
                        + randint(-1000, 1000) / 1000 # petit offset aleatoire pour ne pas avoir 2* la meme position

        self.y = randint(MAP_DIMENTION["ordonnees"][0] + self.size,
                        MAP_DIMENTION["ordonnees"][1] - self.size) \
                        + randint(-1000, 1000) / 1000

        self.z = randint(MAP_DIMENTION["cotes"][0] + self.size,
                        MAP_DIMENTION["cotes"][1] - self.size) \
                        + randint(-1000, 1000) / 1000

        self.nextPos = self.position
        self.oldPos = self.position
        self.movement = True
        self.hasChanged = True

        sortedAABBs.insert(self)

    def displayPseudo(self, pseudo):
        """Génère et affiche une Entité (un cube) self.pseudo, qui a comme texture
        une image de la chaîne de caractère pseudo

        Args:
            pseudo (str): le pseudo à afficher au-dessus de la balle
        """
        self.hasPseudo = True
        
        print("NAME_FONT:", NAME_FONT.getname())

        lines = pseudo.split('\n')

        max_width = 0
        total_height = 0

        for line in lines:
            line_width = NAME_FONT.getmask(line).getbbox()[2] - NAME_FONT.getmask(line).getbbox()[0]
            max_width = max(max_width, line_width)
            total_height += NAME_FONT.getmask(line).getbbox()[3] - NAME_FONT.getmask(line).getbbox()[1]

        pseudo_size = (max_width, total_height)

        texture = Image.new("RGBA", pseudo_size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(texture)

        y = 0
        for line in lines:
            line_width = NAME_FONT.getmask(line).getbbox()[2] - NAME_FONT.getmask(line).getbbox()[0]
            line_height = NAME_FONT.getmask(line).getbbox()[3] - NAME_FONT.getmask(line).getbbox()[1]
            draw.text((0, y), line, font=NAME_FONT, fill=(255,255,255,200))
            y += line_height

        self.pseudoSizeX = PSEUDO_SIZE_X * pseudo_size[0]
        self.pseudoSizeY = PSEUDO_SIZE_Y * pseudo_size[1]

        self.pseudo = Entity(model='cube', 
                            scale=(self.size * self.pseudoSizeX, self.size * self.pseudoSizeY, 0),
                            position=(self.x, self.y + PSEUDO_OFFSET_Y*self.size, self.z),
                            texture=Texture(texture), shader=unlit_shader)


    def tickUpdate(self):
        """Gere tout ce qui doit ce passer lors d'un tick
        (mise a jour de sortedAABBs, logique de l'IA, ect...)
        A appeler uniquement lors d'un tick
        """
        #mise a jour de sortedAABBs
        if self.hasChanged:
            sortedAABBs.remove(self)

            self.oldPos = self.position
            self.oldSize = self.size
            self.hasChanged = False
                
            sortedAABBs.insert(self)
        
    def movementHandler(self):
        """Gere les mouvements de la balle,
        les rend smooth
        A appeler chaque frame
        """
        
        if -0.01 >= self.nextSize - self.size or self.nextSize - self.size >= 0.01:
            if self.nextSize < DEFAULT_PLANET_SIZE:
                self.nextSize = DEFAULT_PLANET_SIZE
                self.set_size(DEFAULT_PLANET_SIZE)
            self.set_size(lerp(self.size, self.nextSize, GROWTH_SMOOTHNESS * time.dt))

            self.pseudo.scale = (self.size * self.pseudoSizeX, self.size * self.pseudoSizeY, 0)
            self.hasChanged = True
        else:
            self.growth = False

        if self.is_big_dist(self.nextPos - self.position):
            mov = MOVEMENT_SMOOTHNESS * time.dt

            self.nextPos.x = clamp(self.nextPos.x, MAP_DIMENTION["abscisses"][0] + self.size/2, MAP_DIMENTION["abscisses"][1] - self.size/2)
            self.nextPos.y = clamp(self.nextPos.y, MAP_DIMENTION["ordonnees"][0] + self.size/2, MAP_DIMENTION["ordonnees"][1] - self.size/2)
            self.nextPos.z = clamp(self.nextPos.z, MAP_DIMENTION["cotes"][0] + self.size/2, MAP_DIMENTION["cotes"][1] - self.size/2)
            
            self.x = lerp(self.x, self.nextPos.x, mov)
            self.y = lerp(self.y, self.nextPos.y, mov)
            self.z = lerp(self.z, self.nextPos.z, mov)

            self.pseudo.position = (self.x, self.y + PSEUDO_OFFSET_Y*self.size, self.z)
            self.hasChanged = True
        else:
            self.movement = False

        if self.is_big_dist(self.nextRotation - self.rotation):
            rot = ROTATION_SMOOTHNESS * time.dt

            self.rotation_x = lerp(self.rotation_x, self.nextRotation.x, rot)
            self.rotation_y = lerp(self.rotation_y, self.nextRotation.y, rot)
            self.rotation_z = lerp(self.rotation_z, self.nextRotation.z, rot)
            
    def dash(self):
        if t() - self.lastDashTime < DASH_COOLDOWN or self.size <= 2*DEFAULT_PLANET_SIZE: return
        
        self.lastDashTime = t()
        self.nextPos += self.forward.normalized() * DASH_POWER
        self.nextSize *= (1 - DASH_SIZE_LOSS)

    def is_big_dist(self, d: Vec3) -> bool:
        """Retourne Vrai si la distance entre les coordonnees
        de cet element et du point est 'grande' (superieure a |0.01|)
        Est utilise pour optimiser les mouvements avec lerp()

        Args:
            d (Vec3): le point duquel on regarde la distance

        Returns:
            bool: Si la difference entre les coordonnees des elements est inferieure a |0.01|
        """
        if d.x < -0.01 or 0.01 < d.x:
            return True
        if d.y < -0.01 or 0.01 < d.y:
            return True
        if d.z < -0.01 or 0.01 < d.z:
            return True

    def set_size(self, size):
        self.size = size
        self.speed = max(FORCE_TORC - 4*self.size**0.5, 5)

        self.scale_x = self.size
        self.scale_y = self.size
        self.scale_z = self.size

        if not self.growth:
            self.growth = True

    def addForce(self, force = Vec3()):
        self.nextPos.x += force.x * time.dt * self.speed
        self.nextPos.y += force.y * time.dt * self.speed
        self.nextPos.z += force.z * time.dt * self.speed
        if not self.movement: self.movement = True

    def delete(self):
        #print("deletion", self)
        sortedAABBs.remove(self)
        self.deleted = True
        if self.hasPseudo:
            self.pseudo.disable()
            Entity.disable(self.pseudo)
            
        scene.entities.remove(self)
        Entity.disable(self)
        destroy(self)
        
    def kill(self):
        """
            Permet d'executer les scripts qui font en sorte que cette entité est mangé
            Attention:  Cette fonction peut être 'overwritten', notament dans la class 'Gems'
                        Ne pas utiliser d'autre méthode pour manger cette entitée
        """
        self.delete()

    def dist(self, ball):
        return  (self.x - ball.x)**2 \
                + (self.y- ball.y)**2 \
                + (self.z - ball.z)**2

    def collide(self, ball):
        if not self.deleted:
            return self.dist(ball) < (self.size / 2 + ball.size / 2)**2
        else:
            print("COLLISION")
            print(self)
            for q in sortedAABBs:
                print(self in q)
            print(self in scene.entities)

    def eat(self, ball):
        """ Permet de manger une planète
            [INPUT]
                -> ball: {AgarBall} La boule à manger
        """
        if ball.name.startswith(BLACKHOLES_ENTITY_PREF):
            if self.size >= ball.size:
                if is_player(self): playAudio("touching_blackhole")

                self.addForce(self.back.normalized() * DASH_POWER)
                self.nextSize /= 2
            return
        
        if is_player(self):
            if ball.name.startswith(GEMS_ENTITY_PREF):
                playAudio("eating_gem")
            else: playAudio("eating_planet")
        # d'apres la formule de l'aire
        self.nextSize = (self.nextSize ** 2 + ball.size ** 2) ** 0.5
        ball.kill()
        del ball
        
    def __str__(self):
        return self.name
