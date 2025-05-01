import pygame

# Inicializa o mixer uma única vez
if not pygame.mixer.get_init():
    pygame.mixer.init()

def playOnce(audio_file, volume=100):
    """
    Reproduz um arquivo de áudio uma vez.
    """
    volume = max(0, min(volume, 100)) / 100
    som = pygame.mixer.Sound(audio_file)
    som.set_volume(volume)
    som.play()

def playLoop(audio_file, volume=100):
    """
    Reproduz um arquivo de áudio em loop.
    """
    volume = max(0, min(volume, 100)) / 100
    som = pygame.mixer.Sound(audio_file)
    som.set_volume(volume)
    som.play(loops=-1)

def stopAudio():
    """
    Para todos os sons em execução.
    """
    pygame.mixer.stop()
