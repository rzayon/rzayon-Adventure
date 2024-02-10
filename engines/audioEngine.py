import pygame
import os
import time
import inspect

import musicPlaying


# Play Audio

def musicPlay(music):
    if os.path.exists(music):
        if music != musicPlaying.musicPlaying:
            pygame.mixer.music.load(music)
            pygame.mixer.music.set_volume(1)
            pygame.mixer.music.play(-1)
            musicPlaying.musicPlaying = music
    else:
        musicPlaying.musicPlaying = music
        pygame.mixer.music.stop()

def sfxPlay(sfx, channel):
    if os.path.exists(sfx):
        pygame.mixer.Channel(channel).play(pygame.mixer.Sound(sfx))

def sfxPlayLoop(sfx, channel):
    if os.path.exists(sfx):
        pygame.mixer.Channel(channel).play(pygame.mixer.Sound(sfx), -1)


# Misc Audio

def musicVolumeLower():
    volume = pygame.mixer.music.get_volume()
    if volume == 1:
        for i in range(50):
            pygame.mixer.music.set_volume(volume)
            volume -= 0.013
            time.sleep(0.001)

def musicVolumeReset():
    volume = pygame.mixer.music.get_volume()
    if volume != 1:
        for i in range(50):
            pygame.mixer.music.set_volume(volume)
            volume += 0.012
            time.sleep(0.001)
    pygame.mixer.music.set_volume(1)

def musicFadeOut(temps):
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.fadeout(int(temps))


# Stop Audio

def musicStop():
    if pygame.mixer.music.get_busy():
        musicPlaying.musicPlaying = None
        pygame.mixer.music.stop()

def sfxStop(channel):
    if pygame.mixer.music.get_busy():
        pygame.mixer.Channel(channel).stop()

pygame.mixer.init()
global musicPlaying