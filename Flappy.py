#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 🎵 FLAPPY BIRD - 100% OFFLINE MIT SYNTHETISCHEN SOUNDS
# 🚀 Läuft sofort nach Start

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
            }
        except Exception as e:
            print(f"Sound konnte nicht erzeugt werden: {e}")
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

# Spielvariablen
bird_rect = pygame.Rect(100, 300, 30, 30)
bird_speed = 0
gravity = 0.4
pipes = []
pipe_width = 70
pipe_gap = 150
pipe_frequency = 1500
last_pipe = pygame.time.get_ticks()
score = 0
high_score = 0
game_active = False
font = pygame.font.SysFont('Arial', 30, bold=True)
passed_pipes = set()

def draw_bird():
    pygame.draw.circle(screen, BIRD_RED, bird_rect.center, 15)
    pygame.draw.circle(screen, WHITE, (bird_rect.centerx + 7, bird_rect.centery - 5), 4)
    pygame.draw.circle(screen, BLACK, (bird_rect.centerx + 7, bird_rect.centery - 5), 2)
    pygame.draw.polygon(screen, BIRD_YELLOW, [
        (bird_rect.centerx + 15, bird_rect.centery),
        (bird_rect.centerx + 25, bird_rect.centery - 5),
        (bird_rect.centerx + 25, bird_rect.centery + 5)
    ])

def create_pipe():
    random_height = random.randint(200, 400)
    bottom_pipe = pygame.Rect(400, random_height, pipe_width, 600 - random_height)
    top_pipe = pygame.Rect(400, 0, pipe_width, random_height - pipe_gap)
    return bottom_pipe, top_pipe

def check_collision():
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return True
    return bird_rect.top <= 0 or bird_rect.bottom >= 580

def update_score():
    global score, high_score
    for pipe in pipes:
        if pipe.right < 100 and id(pipe) not in passed_pipes and pipe.y > 0:
            passed_pipes.add(id(pipe))
            score += 1
            high_score = max(score, high_score)
            sound_system.play('point')

def show_score():
    score_text = font.render(f"{score}", True, WHITE)
    screen.blit(score_text, (200 - score_text.get_width()//2, 50))

def show_menu():
    title = font.render("FLAPPY BIRD", True, WHITE)
    start = font.render("SPACE zum Starten", True, WHITE)
    high_score_text = font.render(f"Highscore: {high_score}", True, WHITE)
    
    screen.blit(title, (200 - title.get_width()//2, 200))
    screen.blit(start, (200 - start.get_width()//2, 300))
    screen.blit(high_score_text, (200 - high_score_text.get_width()//2, 400))

def show_game_over():
    overlay = pygame.Surface((400, 600), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))
    
    texts = [
        font.render("GAME OVER", True, RED),
        font.render("SPACE zum Neustart", True, WHITE),
        font.render(f"Punkte: {score}", True, WHITE),
        font.render(f"Highscore: {high_score}", True, WHITE)
    ]
    
    for i, text in enumerate(texts):
        screen.blit(text, (200 - text.get_width()//2, 200 + i * 100))

# Hauptspiel-Loop
running = True
while running:
    clock.tick(60)
    screen.fill(SKY_BLUE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not game_active:
                    # Neustart
                    game_active = True
                    bird_rect.y = 300
                    bird_speed = 0
                    pipes = []
                    score = 0
                    passed_pipes.clear()
                    last_pipe = pygame.time.get_ticks()
                else:
                    # Flügelschlag
                    bird_speed = -7
                    sound_system.play('wing')

    if game_active:
        # Spiel-Logik
        bird_speed += gravity
        bird_rect.y += bird_speed

        # Rohre generieren
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency:
            pipes.extend(create_pipe())
            last_pipe = time_now

        # Rohre bewegen
        for pipe in pipes[:]:
            pipe.x -= 3
            if pipe.right < 0:
                pipes.remove(pipe)

        # Kollision & Punkte
        if check_collision():
            sound_system.play('hit')
            game_active = False
        else:
            update_score()

        # Zeichnen
        for pipe in pipes:
            pygame.draw.rect(screen, GREEN, pipe)
            pygame.draw.rect(screen, (0, 180, 0), pipe, 3)
        
        draw_bird()
        show_score()
    else:
        if score > 0:
            show_game_over()
        else:
            show_menu()

    # Boden
    pygame.draw.rect(screen, (200, 180, 50), (0, 580, 400, 20))
    pygame.draw.rect(screen, (150, 130, 20), (0, 580, 400, 5))

    pygame.display.update()

pygame.quit()
sys.exit()
