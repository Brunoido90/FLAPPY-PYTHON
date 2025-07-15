#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 🎵 FLAPPY BIRD - 100% OFFLINE SOUNDS
# 🔇 Keine MP3s, kein Internet, keine Dateien

import pygame
import random
import sys
import math
from pygame import sndarray
import numpy

# Initialisierung
pygame.init()
mixer = pygame.mixer
mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
screen = pygame.display.set_mode((400, 600))
pygame.display.set_caption("Flappy Bird 🐦")
clock = pygame.time.Clock()

# Farben
SKY_BLUE = (107, 187, 255)
GREEN = (118, 255, 122)
BIRD_YELLOW = (255, 204, 0)
BIRD_RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

class SoundSystem:
    def __init__(self):
        self.sounds = {}
        self.enabled = True
        self.create_sounds()
    
    def generate_beep(self, frequency=440, duration=0.1, volume=0.5):
        sample_rate = mixer.get_init()[0]
        samples = int(duration * sample_rate)
        buf = numpy.zeros((samples, 2), dtype=numpy.int16)
        
        for s in range(samples):
            t = float(s) / sample_rate
            wave = volume * math.sin(2 * math.pi * frequency * t)
            buf[s][0] = int(32767 * wave)
            buf[s][1] = int(32767 * wave)
        
        sound = pygame.sndarray.make_sound(buf)
        return sound
    
    def create_sounds(self):
        try:
            self.sounds = {
                'wing': self.generate_beep(800, 0.1),
                'point': self.generate_beep(1200, 0.15),
                'hit': self.generate_noise(0.3),
                'background': None  # Kein Hintergrundsound
            }
        except:
            self.enabled = False
    
    def generate_noise(self, duration=0.3):
        sample_rate = mixer.get_init()[0]
        samples = int(duration * sample_rate)
        buf = numpy.zeros((samples, 2), dtype=numpy.int16)
        
        for s in range(samples):
            val = random.randint(-32767, 32767)
            buf[s][0] = val
            buf[s][1] = val
        
        return pygame.sndarray.make_sound(buf)
    
    def play(self, name):
        if self.enabled and name in self.sounds and self.sounds[name]:
            self.sounds[name].play()

sound_system = SoundSystem()

# [Rest des Spielcodes bleibt identisch wie in Ihrer ursprünglichen Version]
# ...

# In der Hauptspielschleife ersetzen Sie die Soundaufrufe mit:
# sound_system.play('wing')  # Beim Flügelschlag
# sound_system.play('point') # Bei Punkten
# sound_system.play('hit')   # Bei Kollision

pygame.quit()
sys.exit()
