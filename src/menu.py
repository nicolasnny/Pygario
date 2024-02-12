from ursina import Button, mouse, Text, Keys, input_handler, Entity, camera, InputField, time, application, invoke
from constant import PYGARIO_UI_SUF, BUTTON_ENTITIES_PREF, DEFAULT_BINDS, PLAYER_DEFAULT_PSEUDO
from texture import planet_textures
from audio import playAudio
from texture import give_texture

skinModelId=0
input_handler.rebind("q","a")
input_handler.rebind("a","q")
input_handler.rebind("w","z")
input_handler.rebind("z","w")

class Menu:
    def __init__(self, data, binds= DEFAULT_BINDS, directInit= True) -> None:
        self.keyList=["a","z","e","r","t","y","u","i","o","p","q","s","d","f","g","h","j","k","l","m","w","x","c","v","b","n","space",Keys.left_shift,Keys.left_control,Keys.up_arrow,Keys.down_arrow,Keys.left_arrow,Keys.right_arrow]
        self.forceDeleteButton=None
        mouse.locked=False
        self.pygario= data # Pour acceder au monde: self.pygario.world
        self.binds= binds
        
        self.is_selecting_binds = False
        self.is_selecting_skin = False
        self.was_not_left_click = True
        
        if directInit:
            self.initMenu()

    def update(self):
        if self.is_selecting_binds:
            for key, value in input_handler.held_keys.items():
                if value >= 1:
                    self.bindAssigning(key, self.bindAction)

        if self.is_selecting_skin:
            # faire tourner le skin
            self.skin.rotation_y += 10*time.dt

            # detecter si l'on appuie sur le skin
            if mouse.x **2 + mouse.y **2 <= (self.skin.scale/2)**2:
                for key, value in input_handler.held_keys.items():
                    if key == "left mouse":
                        if value == 1 and self.was_not_left_click:
                            self.was_not_left_click = False
                            playAudio("eating_gem")
                            self.setNextSkin()
                        elif value == 0:
                            self.was_not_left_click = True
        
    def Logo(self):
        """Methode permettant d'afficher le logo du jeu
        """
        self.logo=Entity(model="quad",parent=camera.ui, scale=(1,.5,1),position=(.05,.25),
                        texture='./assets/imgs/banner.png', name= f"logo{PYGARIO_UI_SUF}")
        
    def playBackgroud(self):
        """génère la video d'arrière plan
        """
        Entity(model='quad', parent=camera.ui, scale=(3,2,1), texture='./assets/background/menu.mp4', name= f"background{PYGARIO_UI_SUF}")
    
    def buttonAction(self, action, sound= "action_primary"):
        return lambda: (playAudio(sound),action())

    def initMenu(self):
        """Menu initial du jeu permetant d'acceder aux options et à l'onglet de lancement de la partie
        """
        self.clearMenu()
        self.Logo()
        self.playButton=Button(text="Jouer",scale=(.25, .1),position=(.25,0), name= f"{BUTTON_ENTITIES_PREF}play{PYGARIO_UI_SUF}")
        self.playButton.on_click=self.buttonAction(self.playMenu)
        self.OptionButton=Button(text='Options', scale=(.25, .1), position=(-.25,0), name= f"{BUTTON_ENTITIES_PREF}options{PYGARIO_UI_SUF}")
        self.OptionButton.on_click=self.buttonAction(self.optionMenu)
        self.QuitButton=Button(text='Quitter', scale=(.25, .1), position=(0,-.25), name= f"{BUTTON_ENTITIES_PREF}quit{PYGARIO_UI_SUF}")
        self.QuitButton.on_click=self.buttonAction(application.quit, "action_secondary")

    def playMenu(self):
        """Methode permettant l'affichage de l'onglet de lancement de la partie
        """
        self.clearMenu()
        self.exit(self.initMenu)
        self.Logo()
        self.pseudo_text = Text('Votre Pseudonyme :', position=(-.13,.1), name=f"pseudo_text{PYGARIO_UI_SUF}")
        self.pseudo_field = InputField(text=PLAYER_DEFAULT_PSEUDO, name= f"user_name{PYGARIO_UI_SUF}", character_limit=15)
        self.launchButton=Button(text='Lancer une nouvelle\n partie', scale=(.25, .1), position=(0,-.3), name= f"{BUTTON_ENTITIES_PREF}launch_offline_game{PYGARIO_UI_SUF}")
        self.launchButton.on_click=self.launchGame

    def launchGame(self):
        """methode de lancement de la partie à l'aide la méthode launch de la classe Pygario du fichier __main__.py
            (self.pygario est une instance de la classe Pygario)
        """
        print("Starting a new game...")
        if not self.pseudo_field.text:
            print("Pseudo is required to start a new game... Aborting!")
            return self.playMenu()
        playAudio("eating_planet")
        self.clearMenu()
        mouse.position = (0,0,0)
        self.pygario.launch("game", binds= self.binds, player_texture= planet_textures[skinModelId], player_pseudo=self.pseudo_field.text)
        del self

    def optionMenu(self):
        """méthode permettant l'affichage du menu des options permettant l'accès aux modifications de skins et de touches
        """
        self.clearMenu()
        self.exit(self.initMenu)
        if self.is_selecting_skin: self.is_selecting_skin = False

        self.Logo()
        self.skinButton=Button(text="Changez votre skin",scale=(.25, .1),position=(-.25,.0), name= f"{BUTTON_ENTITIES_PREF}modify_skin{PYGARIO_UI_SUF}")
        self.skinButton.on_click=self.buttonAction(self.skinMenu)
        self.bindButton=Button(text="Changez vos touches",scale=(.25, .1),position=(.25,.0), name= f"{BUTTON_ENTITIES_PREF}binds{PYGARIO_UI_SUF}")
        self.bindButton.on_click=self.buttonAction(self.bindMenu)
        

    def skinMenu(self):
        """methode permettant l'affichage du  menu de personnalisation du skin/texture de la planète du joueur
        """
        self.clearMenu()
        self.exit(self.optionMenu)

        self.planetName = Text(planet_textures[skinModelId],x=-.036,y=-.3, name= f"skin_edit_text{PYGARIO_UI_SUF}")
        self.text = Text("Choissez votre skin en cliquant sur la planète",x=-.255,y=.3, name= f"skin_edit_text{PYGARIO_UI_SUF}")
        self.skin = Entity(model = "sphere", parent=camera.ui, scale=(.5,.5,.5),
                        texture=give_texture(planet_textures[skinModelId]),
                        name= f"{BUTTON_ENTITIES_PREF}skin_edit{PYGARIO_UI_SUF}")
        def activateSelector():
            self.is_selecting_skin = True
        invoke(activateSelector, delay=.1)
        
         
    def setNextSkin(self):
        global skinModelId
        skinModelId+=1
        if skinModelId >= len(planet_textures): skinModelId = 0
        self.planetName.text = planet_textures[skinModelId]
        self.skin.texture = give_texture(planet_textures[skinModelId])
              
    def exit(self, destination):
        self.exitButton=Button("Retour",scale=(.15, .06),position=(-.8,.46), name= f"{BUTTON_ENTITIES_PREF}exit{PYGARIO_UI_SUF}")
        self.exitButton.on_click=self.buttonAction(destination, "action_secondary")

    def clearMenu(self):
        """méthode permettant de supprimer tout les elements d'un onglet
        """
        self.pygario.resetWorld()
        self.playBackgroud()

    def bindMenu(self):
        """méthode permettant l'affichage du menu de personnalisation des touches
        """
        self.clearMenu()
        self.exit(self.optionMenu)
        
        if self.forceDeleteButton:
            self.forceDeleteButton.root.destroy()
        
        def set_on_click(type: str):
            return lambda: (playAudio("action_primary"), self.setBind(type))

        if type(self.binds["forward"])==str:
            self.forwardButton=Button(text=f"devant: [{self.binds['forward']}]",size=1,scale=(.25, .1),position=(-.2,.3), name= f"{BUTTON_ENTITIES_PREF}move_forward{PYGARIO_UI_SUF}",on_click=set_on_click("forward"))
        else:
            self.forwardButton=Button(text=f"devant: {str(self.binds['forward'])[5:]}",size=1,scale=(.25, .1),position=(-.2,.3), name= f"{BUTTON_ENTITIES_PREF}move_forward{PYGARIO_UI_SUF}",on_click=set_on_click("forward"))
        if type(self.binds["backward"])==str:
            self.backwardButton=Button(text=f"arrière: [{self.binds['backward']}]",size=1,scale=(.25, .1),position=(.2,.3), name= f"{BUTTON_ENTITIES_PREF}move_backward{PYGARIO_UI_SUF}",on_click=set_on_click("backward"))
        else:
            self.backwardButton=Button(text=f"arrière: {str(self.binds['backward'])[5:]}",size=1,scale=(.25, .1),position=(.2,.3), name= f"{BUTTON_ENTITIES_PREF}move_backward{PYGARIO_UI_SUF}",on_click=set_on_click("backward"))
        if type(self.binds["left"])==str:
            self.leftButton=Button(text=f"gauche: [{self.binds['left']}]",size=1,scale=(.25, .1),position=(-.2,.1), name= f"{BUTTON_ENTITIES_PREF}move_leftward{PYGARIO_UI_SUF}",on_click=set_on_click("left"))
        else:
            self.leftButton=Button(text=f"gauche: [{str(self.binds['left'])[5:]}]",size=1,scale=(.25, .1),position=(-.2,.1), name= f"{BUTTON_ENTITIES_PREF}move_leftward{PYGARIO_UI_SUF}",on_click=set_on_click("left"))
        if type(self.binds["right"])==str:
            self.rightButton=Button(text=f"droite: [{self.binds['right']}]",size=1,scale=(.25, .1),position=(.2,.1), name= f"{BUTTON_ENTITIES_PREF}move_rightward{PYGARIO_UI_SUF}",on_click=set_on_click("right"))
        else:
            self.rightButton=Button(text=f"droite: [{str(self.binds['right'])[5:]}]",size=1,scale=(.25, .1),position=(.2,.1), name= f"{BUTTON_ENTITIES_PREF}move_rightward{PYGARIO_UI_SUF}",on_click=set_on_click("right"))
        if type(self.binds["down"])==str:
            self.downButton=Button(text=f"bas: [{self.binds['down']}]",size=1,scale=(.25, .1),position=(-.2,-.1), name= f"{BUTTON_ENTITIES_PREF}move_downward{PYGARIO_UI_SUF}",on_click=set_on_click("down"))
        else:
            self.downButton=Button(text=f"bas: [{str(self.binds['down'])[5:]}]",size=1,scale=(.25, .1),position=(-.2,-.1), name= f"{BUTTON_ENTITIES_PREF}move_downward{PYGARIO_UI_SUF}",on_click=set_on_click("down"))
        if type(self.binds["up"])==str:
            self.upButton=Button(text=f"haut: [{self.binds['up']}]",size=1,scale=(.25, .1),position=(.2,-.1), name= f"{BUTTON_ENTITIES_PREF}move_upward{PYGARIO_UI_SUF}",on_click=set_on_click("up"))
        else:
            self.upButton=Button(text=f"haut: [{str(self.binds['up'])[5:]}]",size=1,scale=(.25, .1),position=(.2,-.1), name= f"{BUTTON_ENTITIES_PREF}move_upward{PYGARIO_UI_SUF}",on_click=set_on_click("up"))
        if type(self.binds["dash"])==str:
            self.upButton=Button(text=f"dash: [{self.binds['dash']}]",size=1,scale=(.25, .1),position=(-.2,-.3), name= f"{BUTTON_ENTITIES_PREF}dash{PYGARIO_UI_SUF}",on_click=set_on_click("dash"))
        else:
            self.upButton=Button(text=f"dash: [{str(self.binds['dash'])[5:]}]",size=1,scale=(.25, .1),position=(-.2,-.3), name= f"{BUTTON_ENTITIES_PREF}dash{PYGARIO_UI_SUF}",on_click=set_on_click("dash"))
        
        
    def bindAssigning(self, key, action):
        """méthode permettant d'assigner la touche pressé par l'utilisateur à une action du jeu
        args:
            -->key(str ou objet de la class Keys de Ursina): touche préssée par le joueur 
            -->action(str): action du jeu à laquelle il faut assigner la touche key
        """
        if key in self.keyList:
            if key in self.binds.values():
                # enlever la touche de l'action utilisant cette touche
                pass
            playAudio("action_secondary")
            self.binds[action] = key
            self.is_selecting_binds = False
            self.clearMenu()
            self.bindMenu()

    def setBind(self, action):
        """méthode permettant d'activer la recuperation des touches préssées graçe à la methode update.

        Args:
            action (str): action à laquelle la touche préssée sera assignée
        """
        self.is_selecting_binds = True
        self.clearMenu()
        self.bindAction = action
        self.bindText = Text(f"Appuyez sur la touche que vous voulez assigner à l'action \"{action}\"",x=-.35,y=0, name= f"press_bind{PYGARIO_UI_SUF}")

if __name__=="__main__":
    menu=Menu()
