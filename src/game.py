import ursina as Engine
import ursina.input_handler as inputHDL
import player
from robot import RobotPlayer
from world import *
from constant import TICK_RATE, DEVELOPMENT_MODE, MAX_BLACKHOLES, MAX_PLAYERS, MAX_GEMS
from gem import Gems
import ursina.application as app
from time import time
from sun import Sun
from blackHole import BlackHole
from audio import playAudio

debugCompteur = 0
debugTimer = time()
tickDT = 0 

class Game:
    def __init__(self, data, joueurs= MAX_PLAYERS, gems= MAX_GEMS, blackholes= MAX_BLACKHOLES, player_texture:str= None, binds= DEFAULT_BINDS, player_pseudo=PLAYER_DEFAULT_PSEUDO) -> None:
        """ Crée un nouveau jeu
            [INPUT]:
                -> data: l'instance Pygario créé dans le fichier __main__.py
                -> joueurs: Le nombre de joueurs (robots) dans la partie (défaut à 500)
                -> joueurs: Le nombre de gems dans la partie (défaut à 1000)
        """
        self.data = data
        
        #freeze la souris en place
        Engine.mouse.position = (0,0,0)
        Engine.mouse.locked = True
        
        # creation du joueur
        self.player = player.Player(binds=binds, texture=player_texture, pseudo=player_pseudo)
        self.gameEnd = False
        
        # creation des robots
        for _ in range(joueurs):
            RobotPlayer()
        # creation des gems
        for _ in range(gems):
            Gems()
        # creation des trous noirs
        for _ in range(blackholes):
            BlackHole()
        
        # mettre un soleil
        self.sun = Sun()
        
        #mettre une lumiere ambiante de la couleur du soleil
        Engine.AmbientLight(color=Engine.color.rgba(0.9922*BRIGHTNESS, 0.9843*BRIGHTNESS, 0.8275*BRIGHTNESS, 0.0000001),
                            name=LIGHT_ENTITY_PREF+"ambient"+PYGARIO_UI_SUF)
        
        # Être dans l'espace sans étoiles ? Mouai bof hein ?
        skybox = Engine.Sky(texture="./assets/background/space.png")
        skybox.texture.repeat = True
        skybox.texture.apply()
    
    def debugInput(self, key): # Only for debug purposes
        if DEVELOPMENT_MODE:
            ###debug info###
            if key == "i":
                print("##################\nInfo debug :")
                #print(sortedObjects)
                print("pos:", self.player.position)
                #print("size:", self.player.size)
                print("rotation:", self.player.rotation)
                #print("speed:", max(self.player.speed - 1/2 * self.player.size, 1))
                print("checks de collision:", debugCompteur)
            
            if key=="+":
                self.player.nextSize += 0.1 
    def update(self):
        global debugCompteur, tickDT, debugTimer
        doTickUpdate= tickDT >= 1/TICK_RATE

        forceSum = Engine.Vec3()
        
        for key, value in inputHDL.held_keys.items():
            if value:
                # sort en appuyant sur ESCAPE
                if key == inputHDL.Keys.escape:
                    return self.data.default()
                
                # touches du joueur
                force = self.player.genForce(key)
                if force: forceSum += force
                else: self.player.keyHandler(key)
                
                #debug
                if DEVELOPMENT_MODE: self.debugInput(key)
                
        # mouvements du joueurs (normalises)    
        self.player.addForce(forceSum.normalized())
        
        #mouvements du soleil
        self.sun.move()

        # logique de la souris
        if self.data.world.mouse.velocity.xy != (0, 0):
            self.player.rotatePlayer(self.data.world.mouse.velocity)
            
        # initialisation du classement
        if doTickUpdate: classement = []
        
        # logique d'animation des mouvements (pour les players & les blackholes)
        for e in get_entities(lambda e: is_player(e) or e.name.startswith(PLAYERS_ENTITY_PREF) or e.name.startswith(BLACKHOLES_ENTITY_PREF)):
            e.movementHandler()
            
            if doTickUpdate: # logique de tick (moments ou on checks les collisions) 
                tickDT= 0
                e.tickUpdate()
                #insertion des robots dans le classement
                if e.name.startswith(PLAYERS_ENTITY_PREF) or is_player(e):
                    classement.append((e.size, e.pseudoStr))
                

        # le joueur a perdu
        if not self.player.enabled and not self.gameEnd: 
            return self.lose()
        
        if doTickUpdate:
            # tri du classement
            if self.player.enabled:
                classement = sorted(classement, reverse=True)
                
                # affichage du classement
                playerIndex = classement.index((self.player.size, self.player.pseudoStr))
                supPseudo = classement[abs(playerIndex - 1)][1]
                infPseudo = classement[Engine.clamp(playerIndex + 1, 2, len(classement) - 1)][1]
                
                self.player.displayClassement(playerIndex + 1, supPseudo, infPseudo)
            
            #logique de collision
            debugCompteur = sortedAABBs.collisionHandler()
        tickDT += Engine.time.dt

    def lose(self):
        playAudio("death")
        self.data.world.mouse.locked = False
        self.gameEnd = True

        Entity(parent = Engine.camera.ui, model='quad', scale= (10,10),
                    color=Engine.color.rgba(0,0,0,100), name=f"blur{PYGARIO_UI_SUF}") #Cree un effet de flou
        Engine.Text('Vous êtes mort',scale=3, origin=(0,-3),
                           color=Engine.color.red, name=f"death_text{PYGARIO_UI_SUF}")
        backButton = Engine.Button(text="Retour au Menu",scale=(.25, .1),position=(-.5,-.2),
                                   name= f"{BUTTON_ENTITIES_PREF}back{PYGARIO_UI_SUF}",
                                   color=Engine.color.gray)
        quitButton = Engine.Button(text="Quitter le jeu",scale=(.25, .1),position=(.5,-.2),
                                   name= f"{BUTTON_ENTITIES_PREF}quit{PYGARIO_UI_SUF}",
                                   color=Engine.color.gray)

        endFct = self.data.default
        backButton.on_click = lambda: (playAudio("action_primary"), endFct())
        quitButton.on_click = app.quit
        del self
