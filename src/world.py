from ursina import scene, Entity, destroy, color
from aabb_sorted_array import AABB_sorted_array
from constant import *

# trie tous les objets du jeu par rapport a l'axe des abscisses
sortedAABBs = AABB_sorted_array()

def get_player() -> Entity | None:
    """Renvoie le joueur, si il y en as un dans le monde
    Returns:
	    Player: le joueur
    """
    found = get_entities(is_player)
    return found[0] if len(found) else None

def is_player(e: Entity) -> bool:
    """Regarde si l'entité est un joueur
    Args:
        e (Entity) : L'entité en question
    Returns:
         bool : si e est un joueur
    """
    return e.name == PLAYER_ENTITY_NAME + PYGARIO_ENTITIES_SUF

def get_players() -> list[Entity]:    
    """Renvoie toute les joueurs du monde (online et offline)
    Returns:
         list[Entity] : la liste des joueurs
    """
    return get_entities(lambda e: e.name.startswith(PLAYERS_ENTITY_PREF) or is_player(e))

def get_robots() -> list[Entity]:
    """Renvoie tous les robots du monde
    Returns:
         list[Entity] : la liste des robots
    """
    return get_entities(lambda e: e.name.startswith(ROBOTS_ENTITY_PREF))

def get_gems() -> list[Entity]:
    """Renvoie toute les gems du monde
    Returns:
         list[Entity] : la liste des gems
    """
    return get_entities(lambda e: e.name.startswith(GEMS_ENTITY_PREF))

def get_blackholes() -> list[Entity]:
    """Renvoie tous les trous noirs du monde
    Returns:
         list[Entity] : la liste des trous noirs
    """
    return get_entities(lambda e: e.name.startswith(BLACKHOLES_ENTITY_PREF))
    
def get_entities(filterer = lambda e: True) -> list[Entity]:
    """ Renvoie toutes les entitées (filtrées ou non) du monde
        [INPUT]
            -> filterer?: {Function<(e: Entity) -> bool>} Filtrer uniquement les entitées passant ce test (défaut à: (e) -> True)
    """
    return [e for e in scene.entities if e.name.endswith(PYGARIO_ENTITIES_SUF) and filterer(e)]

def get_buttons():
    """Renvoie tous les boutons du monde
    Returns:
         list[Entity] : la liste des boutons
    """
    return get_uis(lambda ui: ui.name.startswith(BUTTON_ENTITIES_PREF))

def get_uis(filterer = lambda e: True) -> list[Entity]:
    """ Renvoie toutes les GUI (filtrées ou non) du monde
        [INPUT]
            -> filterer?: {Function<(e: Entity) -> bool>} Filtrer uniquement les GUI passant ce test (défaut à: (e) -> True)
    """
    return [e for e in scene.entities if e.name.endswith(PYGARIO_UI_SUF) and filterer(e)]

def delete_entity(e: Entity):
    """Supprime une entité du monde
    Args:
         e (Entity) : l'entité à supprimer
    """
    if e.name.endswith(PYGARIO_ENTITIES_SUF):
        e.delete()
    else:
        if e.name.startswith(LIGHT_ENTITY_PREF):
            e.color = color.rgba(0,0,0,0)
        if e in scene.entities:
            scene.entities.remove(e)
        destroy(e)