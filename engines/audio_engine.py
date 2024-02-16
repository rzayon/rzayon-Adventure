""" Moteur audio du jeu.
Contient des fonctions pour lancer une musique, un sfx, réduire le volume et arrêter avec ou sans fondu. """


import pygame
import os
import time

from engines import music_playing


# Play Audio

def music_play(music):
    if os.path.exists(music):
        if music != music_playing.music_playing:
            pygame.mixer.music.load(music)
            pygame.mixer.music.set_volume(1)
            pygame.mixer.music.play(-1)
            music_playing.music_playing = music
    else:
        music_playing.music_playing = music
        pygame.mixer.music.stop()

def sfx_play(sfx, channel):
    if os.path.exists(sfx):
        pygame.mixer.Channel(channel).play(pygame.mixer.Sound(sfx))

def sfx_play_loop(sfx, channel):
    if os.path.exists(sfx):
        pygame.mixer.Channel(channel).play(pygame.mixer.Sound(sfx), -1)


# Misc Audio

def music_volume_lower():
    volume = pygame.mixer.music.get_volume()
    if volume == 1:
        for i in range(50):
            pygame.mixer.music.set_volume(volume)
            volume -= 0.013
            time.sleep(0.001)

def music_volume_reset():
    volume = pygame.mixer.music.get_volume()
    if volume != 1:
        for i in range(50):
            pygame.mixer.music.set_volume(volume)
            volume += 0.012
            time.sleep(0.001)
    pygame.mixer.music.set_volume(1)

def music_fade_out(temps):
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.fadeout(int(temps))


# Stop Audio

def music_stop():
    if pygame.mixer.music.get_busy():
        music_playing.music_playing = None
        pygame.mixer.music.stop()

def sfx_stop(channel):
    if pygame.mixer.music.get_busy():
        pygame.mixer.Channel(channel).stop()

pygame.mixer.init()