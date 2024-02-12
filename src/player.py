from constant import *
from ursina import camera, time, clamp, Entity, color, Text, Vec3
from agarBall import AgarBall
from ursina.input_handler import Keys
from ursina.shaders import unlit_shader
from world import get_players
from audio import playAudio

class Player(AgarBall):
    def __init__(self, pseudo= PLAYER_DEFAULT_PSEUDO, binds=DEFAULT_BINDS, texture=None, base_coordonates = [0,0,0]) -> None:
        
        super().__init__(PLAYER_ENTITY_NAME, base_coordonates, texture=texture) 

        self.binds = binds
        self.pseudoStr = pseudo
        self.displayPseudo(pseudo)
        self.placeCam()

        self.bordureX = None
        self.bordureY = None
        self.bordureZ = None
        
        # s'occupe de l'affichage de la taille
        Text.size = 0.025
        Text.default_resolution = 1080 * Text.size
        self.sizeText = Text("Taille :", position=(-.85,.49))
        self.sizeBar = Entity(parent = camera.ui, model='quad', scale= (.03,.02), position=(-.765,.48), color=color.red)
        
        # s'occupe du classement
        self.affichageClassement = [Entity(parent = camera.ui, model='quad', scale= (.35,.23), position=(.75,.2), color=color.rgba(100,100,100,75)),
                        Text("Classement :", position=(.59,.3)),
                        Text(f"Autre : {16}ème", position=(.6,.25)),
                        Text(f"Vous : {15}ème", color=color.yellow, position=(.6,.2)),
                        Text(f"Autre : {15}ème", position=(.6,.15))]
        self.positionClassement = 0

    def genForce(self, key: str) -> Vec3 | None:      
        if key == self.binds["right"]:
            return camera.right
        elif key == self.binds["left"]:
            return camera.left
        elif key == self.binds["forward"]:
            return camera.forward
        elif key == self.binds["backward"]:
            return camera.back
        elif key == self.binds["up"]:
            return camera.up
        elif key == self.binds["down"]:
            return camera.down

    def keyHandler(self, key: str):
        if key == Keys.left_control and self.size > DEFAULT_PLANET_SIZE:
            self.dash()

    def movementHandler(self):
        super().movementHandler()

        self.displayBorders()
        camera.rotation = self.rotation

        # change l'orientation de tous les pseudo pour qu'ils fassent face au joueur
        for obj in get_players():
            if obj.hasPseudo:
                obj.pseudo.rotation = camera.rotation

        self.placeCam()
        
    def set_size(self, size):
        super().set_size(size)
        
        self.sizeBar.scale_x = self.size / 100
        self.sizeBar.x = -0.78 + self.sizeBar.scale_x/2
        
        if self.size >= 2*DEFAULT_PLANET_SIZE:
            self.sizeBar.color = color.green
        else:
            self.sizeBar.color = color.red

    def rotatePlayer(self, movement):
        self.nextRotation.y += movement.x * ROTATION_SPEED * time.dt
        self.nextRotation.x -= movement.y * ROTATION_SPEED * time.dt
        self.nextRotation.x = clamp(self.nextRotation.x, -90, 90)

    def delete(self):
        Entity.disable(self.sizeText)
        Entity.disable(self.sizeBar)
        
        for e in self.affichageClassement: Entity.disable(e)
        
        return super().delete()

    def placeCam(self):      
        camera.position = self.position + camera.back * CAMERA_DIST * self.size + \
            camera.up * CAMERA_HEIGHT * self.size

        #replacer la camera pour qu'elle ne passe pas derriere les barrieres

        # x:
        if MAP_DIMENTION["abscisses"][0] > camera.x or camera.x > MAP_DIMENTION["abscisses"][1]:
            p = min(abs(MAP_DIMENTION["abscisses"][0] - self.position.x),
                    abs(MAP_DIMENTION["abscisses"][1] - self.position.x)) / abs(camera.x - self.position.x)

            # replacement camera
            camera.position = self.position + (camera.position - self.position) * p

        # y:
        if MAP_DIMENTION["ordonnees"][0] > camera.y or camera.y > MAP_DIMENTION["ordonnees"][1]:
            p = min(abs(MAP_DIMENTION["ordonnees"][0] - self.position.y),
                    abs(MAP_DIMENTION["ordonnees"][1] - self.position.y)) / abs(camera.y - self.position.y)

            # replacement camera
            camera.position = self.position + (camera.position - self.position) * p

        # z:
        if MAP_DIMENTION["cotes"][0] > camera.z or camera.z > MAP_DIMENTION["cotes"][1]:
            p = min(abs(MAP_DIMENTION["cotes"][0] - self.position.z),
                    abs(MAP_DIMENTION["cotes"][1] - self.position.z)) / abs(camera.z - self.position.z)

            # replacement camera
            camera.position = self.position + (camera.position - self.position) * p

    def displayBorders(self):
        """Affiche les bordures lorsque le joueur en est proche
        """

        sizeX = MAP_DIMENTION["abscisses"][1] - MAP_DIMENTION["abscisses"][0]
        sizeY = MAP_DIMENTION["ordonnees"][1] - MAP_DIMENTION["ordonnees"][0]
        sizeZ = MAP_DIMENTION["cotes"][1] - MAP_DIMENTION["cotes"][0]

        # x:
        if abs((self.x - MAP_DIMENTION["abscisses"][0]) < self.size + BORDER_RENDER_DIST 
            or (self.x - MAP_DIMENTION["abscisses"][1])**2 < 16*self.size**2) :

            if not self.bordureX:

                if self.x < (MAP_DIMENTION["abscisses"][0] + MAP_DIMENTION["abscisses"][1])/2:
                    x = MAP_DIMENTION["abscisses"][0]
                else:
                    x = MAP_DIMENTION["abscisses"][1]

                self.bordureX = Entity(model='cube', scale=(0, sizeY, sizeZ),
                    position=(x, 0, 0), color=color.rgba(255, 0, 0, 50), shader=unlit_shader)

        elif self.bordureX:
            Entity.disable(self.bordureX)
            self.bordureX = None

        # y:
        if abs((self.y - MAP_DIMENTION["ordonnees"][0])**2 < self.size + BORDER_RENDER_DIST
            or (self.y - MAP_DIMENTION["ordonnees"][1])**2 < 16*self.size**2):

            if not self.bordureY:

                if self.y < (MAP_DIMENTION["ordonnees"][0] + MAP_DIMENTION["ordonnees"][1])/2:
                    y = MAP_DIMENTION["ordonnees"][0]
                else:
                    y = MAP_DIMENTION["ordonnees"][1]
                

                self.bordureY = Entity(model='cube', scale=(sizeX, 0, sizeZ),
                    position=(0, y, 0), color=color.rgba(255, 0, 0, 50), shader=unlit_shader)

        elif self.bordureY:
            Entity.disable(self.bordureY)
            self.bordureY = None

        # z:
        if abs((self.z - MAP_DIMENTION["cotes"][0])**2 < self.size + BORDER_RENDER_DIST
            or (self.z - MAP_DIMENTION["cotes"][1])**2 < 16*self.size**2):

            if not self.bordureZ:
                
                if self.z < (MAP_DIMENTION["cotes"][0] + MAP_DIMENTION["cotes"][1])/2:
                    z = MAP_DIMENTION["cotes"][0]
                else:
                    z = MAP_DIMENTION["cotes"][1]

                self.bordureZ = Entity(model='cube', scale=(sizeX, sizeY, 0),
                    position=(0, 0, z), color=color.rgba(255, 0, 0, 50), shader=unlit_shader)

        elif self.bordureZ:
            Entity.disable(self.bordureZ)
            self.bordureZ = None
            
    def displayClassement(self, position, pseudo1, pseudo2):
        """Gere tout ce qui as un rapport avec le classement
        A appeler chaque tick
        """
        
        if position == 1:
            
            # changement de place des pseudos existants
            self.affichageClassement[3].text = f"{pseudo1[:16]} : 2ème"
            self.affichageClassement[4].text = f"{pseudo2[:16]} : 3ème"
            
            # changement de place du joueur
            self.affichageClassement[2].text = f"{self.pseudoStr} : 1er"
            
            # changement des couleurs
            self.affichageClassement[2].color = color.gold
            self.affichageClassement[3].color = color.white
            self.affichageClassement[4].color = color.white
            
        elif position == 2:
            
            # changement de texte des pseudos existants
            self.affichageClassement[2].text = f"{pseudo1[:16]} : 1er"
            self.affichageClassement[4].text = f"{pseudo2[:16]} : 3ème"
            
            # changement de texte du joueur
            self.affichageClassement[3].text = f"{self.pseudoStr} : 2ème"
            
            # reset des couleurs si necessaire
            if self.affichageClassement[3].color != color.yellow:
                self.affichageClassement[2].color = color.white
                self.affichageClassement[3].color = color.yellow
                self.affichageClassement[4].color = color.white
            
        else:
            
            # changement de texte des pseudos existants
            self.affichageClassement[2].text = f"{pseudo1[:16]} : {position - 1}ème"
            
            if pseudo2 != self.pseudoStr: self.affichageClassement[4].text = f"{pseudo2[:16]} : {position + 1}ème"
            else: self.affichageClassement[4].text = ""
                
            # changement de texte du joueur
            self.affichageClassement[3].text = f"{self.pseudoStr} : {position}ème"
            
            # reset des couleurs si necessaire
            if self.affichageClassement[3].color != color.yellow:
                self.affichageClassement[2].color = color.white
                self.affichageClassement[3].color = color.yellow
                self.affichageClassement[4].color = color.white
            