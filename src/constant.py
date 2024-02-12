from PIL import ImageFont
from ursina import Keys
from os.path import dirname

#dev only
DEVELOPMENT_MODE = False

# map
MAP_DIMENTION = {
    "abscisses": [-300, 300],
    "ordonnees": [-300, 300],
    "cotes": [-500, 500]
}
MAX_PLAYERS = 40
MAX_GEMS = 500
MAX_BLACKHOLES = 40

# light
BRIGHTNESS = 75

# sun
SUN_SPEED = 0.0005
SUN_ROTATION_SPEED = 0.25
SUN_SIZE = 200
SUN_DISTANCE = 1000
SUN_HEIGHT = 750

# agar ball
DEFAULT_PLANET_SIZE = 3
MOVEMENT_SMOOTHNESS = 2
GROWTH_SMOOTHNESS = 3
FORCE_TORC = 35
DASH_POWER = 50
DASH_COOLDOWN = 1
DASH_SIZE_LOSS = 0.05
BIG_FORCE_TORC = 50
PSEUDO_SIZE_X = 0.025
PSEUDO_SIZE_Y = 0.025
PSEUDO_OFFSET_Y = 0.75
PSEUDOS = ['Astraea', 'Barbapapa', 'BetaSky', 'BigChungus', 'BoltHulk', 'BronzeUranium', 'Darth Vader', 'Davide GoodEnough', 
           'Diego', 'Dix', 'Dora', 'Dr. Goku', 'Fireknight', 'FlyBlade', 'Flymeth', 'Gollum', 'Gruffle', 'Gurber', 'HealTroll', 
           'IGoByLotsOfNames', 'ITyra', 'Iceknith', 'Illuminatis', 'Jacque Chirac', 'Jony Joestar', 'Kayaba Akihiko', 'Kirito', 
           'LegendSteel', 'LotusCraby', 'LuckyRed', 'Luffy', 'Luke skywalker', 'MIAM', 'MambaSword', 'Math0S', 'Meaky Deaz', 'Meh', 
           'MiniMaster', 'MissPhantom', 'NASA', 'Naruto', 'NightHeal', 'Octavia', 'Oreo6945', 'OuiOui', "oWo", 'Piticat', 'Pitichicken', 
           'Retsag99', 'Rick Astley', 'Sasuke', 'Shanks le roux', 'SkyFreedom', 'SkyWorld', 'SteakGhost', 'SteelPhantom', 'SunshineFly', 
           'SushiCaptain', 'SynnCyber', 'Tartinus', 'Tchoupi', 'Technoblade', 'TekHydro', 'Tempest785', 'Tenalp', 'The Milkman', 'Trotro', 
           "UnPetitPasPourLHomme", "UwU", 'ViperGhost', 'Vivicaty', 'WhiteGamer', 'WitcherFlying', 'WorldBlack', 'Yo', 'ZeroBuger', 'chat', 'chlichli', 'dark link', 
           'dayo', 'devSoul', 'dos', 'globaxe', "proximaB",'hehe', 'histoiraios', 'je suis ...', 'jediSlayer', 'kabolop', 'la terre', 'le soleil', 
           'les escargots', 'lil kirby', 'luka', 'maman', 'manger', 'mangeur de patate', 'nilex', 'papa', 'pepe', 'souris verte', 
           'super globe', 'titouan du 95', 'un kiwi', 'unPASrobot',  'zelda', '[ ]']
NAME_FONT = ImageFont.truetype(f"{dirname(__file__)}/assets/fonts/minecraft.otf")

# gem
DEFAULT_GEM_SIZE = 2 

#robot
MAX_ROBOT_SIZE = 5*DEFAULT_PLANET_SIZE

# black hole
MIN_BLACK_HOLE_SIZE = 5
MAX_BLACK_HOLE_SIZE = 40
BLACK_HOLE_ROTATION_SPEED = 0.2

# camera
FOV = 90
ROTATION_SPEED = 10000
ROTATION_SMOOTHNESS = 10
CAMERA_HEIGHT = 1
CAMERA_DIST = 5
BORDER_RENDER_DIST = 25

#game
TICK_RATE = 35

#robot
MAX_ROBOT_SIZE = 5*DEFAULT_PLANET_SIZE

#player
PLAYER_DEFAULT_PSEUDO = "player"

# black hole
MIN_BLACK_HOLE_SIZE = 5
MAX_BLACK_HOLE_SIZE = 40
BLACK_HOLE_ROTATION_SPEED = 0.2

#naming (prefixed, suffixed, absolute name)
PLAYERS_ENTITY_PREF= "players_"
ROBOTS_ENTITY_PREF= PLAYERS_ENTITY_PREF + "robot_"
GEMS_ENTITY_PREF="gem_"
BLACKHOLES_ENTITY_PREF="blackhole_"
SUN_ENTITY_PREF = "sun_"
LIGHT_ENTITY_PREF="light_"
PYGARIO_ENTITIES_SUF="_pygario"

PLAYER_ENTITY_NAME= "player_player"

# ---

BUTTON_ENTITIES_PREF= "pg_button_"
PYGARIO_UI_SUF= "_pg_ui"

# Configuration
DEFAULT_BINDS= {"forward":"z","backward":"s","left":"q","right":"d","down":Keys.left_shift,"up":"space","dash":Keys.left_control} # Modifiable en jeu!
MUSIC_VOLUME= .85 # 0..1
AUDIO_VOLUME= 1 # 0..1