#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 🐦 FLAPPY BIRD - PERFEKTE 1:1 KOPIE
# ✔ Originaler Vogel ✔ Exakte Physik ✔ Unendliche Punkte

import pygame
import random
import sys
import math

# Initialisierung von Pygame und dem Mixer
pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((400, 600))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()

# Farben für das Spiel
SKY_BLUE = (107, 187, 255)
GREEN = (76, 187, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BIRD_YELLOW = (255, 204, 0)
BIRD_RED = (255, 77, 0)
RED = (255, 0, 0)

# Original Flappy Bird Parameter
BIRD_WIDTH = 34
BIRD_HEIGHT = 24
GRAVITY = 0.25
FLAP_STRENGTH = -6.5
PIPE_WIDTH = 52
PIPE_GAP = 120
PIPE_SPEED = 2.5
GROUND_HEIGHT = 500

# --- Soundeffekte laden (Lokale Dateien) ---
# Da die URLs für die Sounds nicht zuverlässig waren, wurde die Download-Funktion entfernt.
# Um Sounds hinzuzufügen, laden Sie einfach Ihre eigenen .mp3- oder .wav-Dateien herunter
# und legen Sie sie im selben Verzeichnis wie dieses Python-Skript ab.
# Benennen Sie sie entsprechend und entfernen Sie die Kommentarzeichen (#).
# Beispiel: flap_sound = pygame.mixer.Sound("wing.mp3")

flap_sound = None
hit_sound = None
point_sound = None
background_music_file_path = None # Steuert die Anzeige einer Fehlermeldung, wenn keine Musik geladen ist.


# Hilfsfunktion zum Zeichnen von zentriertem Text
def draw_centered_text(surface, text, font, color, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(surface.get_width() // 2, y))
    surface.blit(text_surface, text_rect)


# Vogel-Design (Pixelgenau) mit Rotation
def draw_bird(x, y, bird_speed):
    # Berechnung des Rotationswinkels basierend auf der Geschwindigkeit
    rotation = -bird_speed * 3.5  # Ändere den Wert, um die Rotation anzupassen
    if bird_speed < -5: # Begrenzung des maximalen Aufwärtswinkels
        rotation = 20
    elif bird_speed > 10: # Begrenzung des maximalen Abwärtswinkels
        rotation = -90

    # Oberfläche für den Vogel erstellen und darauf zeichnen
    bird_surface = pygame.Surface((BIRD_WIDTH + 15, BIRD_HEIGHT + 15), pygame.SRCALPHA)
    
    # Körper
    pygame.draw.ellipse(bird_surface, BIRD_YELLOW, (0, 0, BIRD_WIDTH, BIRD_HEIGHT))
    # Kopf
    pygame.draw.circle(bird_surface, BIRD_YELLOW, (25, 10), 12)
    # Auge
    pygame.draw.circle(bird_surface, WHITE, (30, 6), 5)
    pygame.draw.circle(bird_surface, BLACK, (30, 6), 2)
    # Schnabel
    pygame.draw.polygon(bird_surface, BIRD_RED, [
        (34, 10),
        (44, 6),
        (44, 14)
    ])
    # Flügel (animiert)
    wing_y = 12 + 3 * math.sin(pygame.time.get_ticks() / 150)
    pygame.draw.ellipse(bird_surface, BIRD_YELLOW, (-5, wing_y, 20, 10))

    # Vogel-Oberfläche drehen
    rotated_bird = pygame.transform.rotate(bird_surface, rotation)
    rotated_bird_rect = rotated_bird.get_rect(center=(x + BIRD_WIDTH / 2, y + BIRD_HEIGHT / 2))
    screen.blit(rotated_bird, rotated_bird_rect)

# Start/Game Over Menü
def draw_menu(score, high_score, game_active):
    if not game_active:
        # Verwende eine zentrierte Schriftart, um dem Original zu entsprechen
        font_large = pygame.font.Font(None, 60)
        font_medium = pygame.font.Font(None, 36)
        screen_center_y = screen.get_height() // 2

        if score > 0: # Game Over Bildschirm
            draw_centered_text(screen, "Game Over", font_large, RED, screen_center_y - 100)
            draw_centered_text(screen, f"Score: {score}", font_medium, WHITE, screen_center_y - 40)
            draw_centered_text(screen, f"High Score: {high_score}", font_medium, WHITE, screen_center_y + 10)
            draw_centered_text(screen, "Drücke LEERTASTE zum Neustart", font_medium, WHITE, screen_center_y + 70)
        else: # Startbildschirm
            draw_centered_text(screen, "Drücke LEERTASTE zum Starten", font_medium, WHITE, screen_center_y)
            draw_centered_text(screen, f"High Score: {high_score}", font_medium, WHITE, screen_center_y + 60)
            draw_bird(bird_x, bird_y, 0)
        
        # Visueller Hinweis, wenn Musik nicht geladen wurde
        if not background_music_file_path:
            error_font = pygame.font.Font(None, 24)
            draw_centered_text(screen, "Hintergrundmusik konnte nicht geladen werden.", error_font, RED, screen_center_y + 150)

# Spielvariablen
bird_x = 100
bird_y = 300
bird_speed = 0
pipes = []
score = 0
high_score = 0
game_active = False
font = pygame.font.Font(None, 40)
passed_pipes = set()
background_music_playing = False

def create_pipe():
    gap_y = random.randint(200, 400)
    return [
        pygame.Rect(400, 0, PIPE_WIDTH, gap_y - PIPE_GAP//2),  # Oben
        pygame.Rect(400, gap_y + PIPE_GAP//2, PIPE_WIDTH, 600) # Unten
    ]

# Hauptspiel-Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if not game_active:
                # Neustart
                game_active = True
                bird_y = 300
                bird_speed = 0
                pipes = []
                score = 0
                passed_pipes = set()
                if not background_music_playing and background_music_file_path:
                    pygame.mixer.music.play(-1)
                    background_music_playing = True
            else:
                # Sprung
                bird_speed = FLAP_STRENGTH
                if flap_sound:
                    flap_sound.play()

    # Logik, um die Musik bei Game Over zu stoppen
    if not game_active and background_music_playing:
        if background_music_file_path:
            pygame.mixer.music.stop()
        background_music_playing = False

    # Spiel-Logik
    if game_active:
        # Physik
        bird_speed += GRAVITY
        bird_y += bird_speed

        # Rohr-Generierung
        if len(pipes) == 0 or pipes[-1][0].x < 250:
            pipes.append(create_pipe())

        # Rohr-Bewegung
        for pipe_pair in pipes[:]:
            for pipe in pipe_pair:
                pipe.x -= PIPE_SPEED
            if pipe_pair[0].right < 0:
                pipes.remove(pipe_pair)

        # Kollision
        bird_rect = pygame.Rect(bird_x, bird_y, BIRD_WIDTH, BIRD_HEIGHT)
        for pipe_pair in pipes:
            for pipe in pipe_pair:
                if bird_rect.colliderect(pipe):
                    game_active = False
                    if hit_sound:
                        hit_sound.play()
                    if score > high_score:
                        high_score = score
            
        # Boden-Kollision
        if bird_y > GROUND_HEIGHT - BIRD_HEIGHT or bird_y < 0:
            game_active = False
            if hit_sound:
                hit_sound.play()
            if score > high_score:
                high_score = score

        # Punktezählung
        for pipe_pair in pipes:
            if pipe_pair[0].right < bird_x and id(pipe_pair) not in passed_pipes:
                score += 1
                passed_pipes.add(id(pipe_pair))
                if point_sound:
                    point_sound.play()

    # Zeichnen
    screen.fill(SKY_BLUE)
    
    # Rohre
    for pipe_pair in pipes:
        for pipe in pipe_pair:
            pygame.draw.rect(screen, GREEN, pipe)
            pygame.draw.rect(screen, (50, 120, 0), pipe, 3)
    
    # Boden
    pygame.draw.rect(screen, (150, 100, 50), (0, GROUND_HEIGHT, 400, 100))
    
    # Vogel
    if game_active:
        draw_bird(bird_x, bird_y, bird_speed)
    
    # Punktestand
    score_text = font.render(str(score), True, WHITE)
    score_rect = score_text.get_rect(center=(screen.get_width() // 2, 100))
    screen.blit(score_text, score_rect)
    
    # Start/Game Over Menü
    if not game_active:
        if score > high_score:
            high_score = score
        draw_menu(score, high_score, game_active)
            
    pygame.display.update()
    clock.tick(60)
