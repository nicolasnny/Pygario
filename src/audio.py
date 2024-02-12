from ursina import Audio
from constant import AUDIO_VOLUME

def playAudio(name: str, volume= AUDIO_VOLUME, **kargs):
    return Audio(f"./assets/sounds/{name}.wav", volume= volume, **kargs)