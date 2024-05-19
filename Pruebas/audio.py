import pygame

def play_audio(filename):
    """
    Reproduce un archivo de audio dado.
    """
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

play_audio("luces_bajas.mp3")

# Esperar a que termine de reproducirse
while pygame.mixer.music.get_busy():
    pygame.time.Clock().tick(10)