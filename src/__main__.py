import ursina as Engine
import ursina.input_handler as inputHDL
import ursina.camera as Cam
from constant import FOV, DEVELOPMENT_MODE, MUSIC_VOLUME
from game import Game 
from world import get_entities, get_uis, delete_entity
from menu import Menu
from audio import playAudio

Engine.window.icon= "./assets/imgs/pygario.ico"
Engine.window.title= "STJ Labs - Pygario"

class Pygario:
    def __init__(self)   -> None:
        self.world= Engine.Ursina(title="PyGario3D", fullscreen=not DEVELOPMENT_MODE, development_mode= DEVELOPMENT_MODE)
        
        inputHDL.rebind('w', 'z')
        inputHDL.rebind('a', 'q')
        Cam.fov = FOV
        Engine.application.development_mode = DEVELOPMENT_MODE
        
        Engine.window.fps_counter.enabled = DEVELOPMENT_MODE
        
        self.state= None # Instance du state actuel (valeur prise dans la liste des states valides ci-dessous)
        self.validStates = [Game, Menu]
        self.onupdate= None
        self.oninput= None

    def resetWorld(self, entities= True, ui= True, evenPersistent= False, moreEntities: list[Engine.Entity]= []):
        """ Supprime toutes les entitées/éléments d'interface du monde (uniquement ceux créées par le jeu)
            [INPUT]
                -> entities: {bool} Supprimer les entitiées ?
                -> ui: {bool} Supprimer les éléments d'interfaces ?
                -> evenPersistent: {bool} Si les objets définies comme "invinsible" doivent également être supprimés (défaut à False)
        """
        toDelete= (get_entities() if entities else []) + (get_uis() if ui else []) + moreEntities
        for e in toDelete:
            if e.eternal and not evenPersistent: continue
            delete_entity(e)
            
    def resetState(self):
        self.onupdate= None
        self.oninput= None
        if self.state:
            del self.state
            self.state= None
            
    def update(self):
        if self.onupdate:
            self.onupdate()
        self.world.step()
        
    def launch(self, state: str, **args):
        """ Lancer un type de monde
            [INPUT]
                -> state: "game", "menu" (pour le moment)
        """
        self.resetState()
        self.resetWorld()
        for classe in self.validStates:
            if classe.__name__.lower() == state.lower():
                self.state = classe(self, **args)
                break
        assert self.state, "Invalid state provided"

        print("Changing state to:", state)
        if getattr(self.state, "update", None):
            self.onupdate= self.state.update
        if getattr(self.state, "input", None):
            self.oninput= self.state.input
            
    def default(self):
        return self.launch("menu")
    
    def run(self):
        playAudio("music", volume= MUSIC_VOLUME, loop= True)
        while self.world:
            self.update()

if __name__ == "__main__":
    pygario= Pygario()
    def debugInput(*arg):
        if pygario.oninput:
            pygario.oninput(*arg)
    pygario.default()
    pygario.run()