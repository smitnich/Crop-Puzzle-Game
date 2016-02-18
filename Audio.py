import pygame
from pygame.locals import *
snd_cancel = None
snd_match = None

def Init():
    global snd_cancel, snd_match
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    pygame.mixer.init()
    snd_cancel = pygame.mixer.Sound("audio/error.aiff")
    snd_match = pygame.mixer.Sound("audio/match.wav")

def Match():
    global snd_match
    snd_match.play()

def Cancel():
    global snd_cancel
    snd_cancel.play()