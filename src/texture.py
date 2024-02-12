from random import randint
def give_texture_random(planet_only= False):
    textures= planet_textures if planet_only else valid_textures
    index=randint(0,len(textures)-1)
    return give_texture(textures[index])

def give_texture(planet):
    planet=planet.lower()
    if planet in valid_textures:
        return f"./assets/models/globe/textures/{planet}.jpg"
    else:
        return "black"
    
  
planet_textures=["callisto","earth","enceladus","europa","io","jupiter","mars","mimas","neptune","pluton","saturne","venus"]
valid_textures= planet_textures + ["blackhole","sun","gem"]

if __name__=="__main__":
    for planet in valid_textures:
        print("./assets/models/globe/textures/"+planet+".jpg")