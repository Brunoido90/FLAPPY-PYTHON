#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 🚀 FLAPPY PYTHON PRO - MIT WEB-SOUNDS & GRAFIKEN
# Steuerung: LEERTASTE zum Fliegen!

import pygame
import random
import sys
import requests
import io
from pygame import mixer

# Initialisierung
pygame.init()
mixer.init()
screen = pygame.display.set_mode((400, 600))
pygame.display.set_caption("Flappy Python Pro 🐦🔥")

# Lade Assets direkt aus dem Web (keine lokalen Dateien nötig!)
def load_web_asset(url):
    response = requests.get(url)
    return io.BytesIO(response.content)

# Grafiken (Pixel-Art aus dem Web)
try:
    bird_img = pygame.image.load(load_web_asset(
        "https://img.icons8.com/color/48/000000/bird.png"))
    pipe_img = pygame.image.load(load_web_asset(
        "https://img.icons8.com/color/48/000000/pipe.png"))
    bg_img = pygame.image.load(load_web_asset(
        "https://img.icons8.com/color/48/000000/sky.png"))
except:
    # Fallback-Simple-Grafiken
    bird_img = pygame.Surface((30, 30), pygame.SRCALPHA)
    pygame.draw.circle(bird_img, (255, 0, 0), (15, 15), 15)
    pipe_img = pygame.Surface((50, 300), pygame.SRCALPHA)
    pipe_img.fill((0, 200, 0))
    bg_img = pygame.Surface((400, 600))
    bg_img.fill((78, 192, 246))

# Soundeffekte (Web-API)
def play_web_sound(url):
    try:
        sound_data = requests.get(url).content
        sound = mixer.Sound(io.BytesIO(sound_data))
        sound.play()
    except:
        pass  # Silent-Fallback

# Spielvariablen
gravity = 0.25
bird_movement = 0
game_active = True
score = 0
high_score = 0
font = pygame.font.Font(None, 36)
bird_rect = bird_img.get_rect(center=(100, 250))
ground_y = 500

# Rohre
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1500)

# Hauptspiel-Loop
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if game_active:
                bird_movement = -7
                play_web_sound("https://www.soundjay.com/buttons/sounds/button-09.mp3")  # Flügelschlag
            else:
                # Neustart
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100, 250)
                bird_movement = 0
                score = 0
        if event.type == SPAWNPIPE and game_active:
            pipe_list.extend(create_pipe())
            play_web_sound("https://www.soundjay.com/buttons/sounds/button-10.mp3")  # Rohr-Spawn

    # Hintergrund
    screen.blit(pygame.transform.scale(bg_img, (400, 600)), (0, 0))

    if game_active:
        # Vogel-Physik
        bird_movement += gravity
        bird_rect.y += bird_movement
        
        # Rohre bewegen
        pipe_list = [pipe for pipe in pipe_list if pipe.x > -50]
        for pipe in pipe_list:
            pipe.x -= 3
        
        # Kollision
        if any(bird_rect.colliderect(pipe) for pipe in pipe_list) or bird_rect.top <= 0 or bird_rect.bottom >= ground_y:
            play_web_sound("https://www.soundjay.com/buttons/sounds/button-08.mp3")  # Game Over
            game_active = False
        
        # Score
        for pipe in pipe_list:
            if pipe.right == 100:  # Wenn Vogel passiert
                score += 1
                play_web_sound("https://www.soundjay.com/buttons/sounds/button-02.mp3")  # Punkt
                high_score = max(score, high_score)
        
        # Zeichnen
        for pipe in pipe_list:
            screen.blit(pygame.transform.scale(pipe_img, (50, pipe.height)), pipe)
        screen.blit(bird_img, bird_rect)
        
        # Score-Anzeige
        screen.blit(font.render(f"Score: {score}", True, (255, 255, 255)), (10, 10))
    else:
        # Game Over Screen
        screen.fill((0, 0, 0))
        screen.blit(font.render("Game Over! SPACE zum Neustart", True, (255, 255, 255)), (50, 250))
        screen.blit(font.render(f"High Score: {high_score}", True, (255, 255, 255)), (120, 300))

    # Boden
    pygame.draw.rect(screen, (94, 201, 72), (0, ground_y, 400, 100))
    
    pygame.display.update()
    clock.tick(60)

def create_pipe():
    random_height = random.randint(150, 400)
    bottom_pipe = pygame.Rect(400, random_height, 50, 600 - random_height)
    top_pipe = pygame.Rect(400, 0, 50, random_height - 150)
    return bottom_pipe, top_pipe
