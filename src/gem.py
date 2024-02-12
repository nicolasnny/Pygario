from agarBall import AgarBall
from constant import DEFAULT_GEM_SIZE, GEMS_ENTITY_PREF
from world import get_gems

class Gems(AgarBall):
    def __init__(self):
        super().__init__(f"{GEMS_ENTITY_PREF}{len(get_gems())}", texture="gem.jpg", size=DEFAULT_GEM_SIZE)

    def kill(self):
        self.rand_pos()


if __name__ == '__main__': 
    gem = Gems()
    gem.rand_pos()
    print(gem.coord)
    gem.kill()
    print(gem.coord)
    gem.kill()
    print(gem.coord)
    gem.kill()
    print(gem.coord)
    gem.kill()
    print(gem.coord)
