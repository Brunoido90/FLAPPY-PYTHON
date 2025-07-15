#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 🐦 FLAPPY BIRD - PERFEKTE 1:1 KOPIE
# ✔ Originaler Vogel ✔ Exakte Physik ✔ Unendliche Punkte

import pygame
import random
import sys
import math
import requests # Importiere das requests Modul
import os       # Importiere das os Modul für Dateipfade

# Initialisierung
pygame.init()
pygame.mixer.init() # Initialisiere den Pygame Mixer

screen = pygame.display.set_mode((400, 600))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()

# Farben
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

# --- URLs für Sounddateien (DIESE SIND PLATZHALTER! BITTE ERSETZEN SIE DIESE!) ---
# Sie müssen hier direkte Download-Links zu WAV-Dateien finden, z.B. von Freesound.org
# Beispiel: SOUND_URLS = {"flap": "https://freesound.org/data/previews/274/274093_4981146-lq.wav", ...}
SOUND_URLS = {
    "flap": "https://www.101soundboards.com/sounds/13789-flap",
    "hit": "https://www.101soundboards.com/sounds/13786-flappy-bird-hit-sound",
    "point": "https://www.101soundboards.com/sounds/13787-point",
    "music": "https://www.101soundboards.com/sounds/31661337-super-mario-bros-nes-music-overworld-theme"
}

# --- Funktion zum Herunterladen von Dateien ---
def download_file(url, filename):
    if not url or url.startswith("https://www.example.com/"): # Überspringe Platzhalter-URLs
        print(f"Skipping download for placeholder URL: {url}")
        return False
    if os.path.exists(filename):
        print(f"Datei '{filename}' existiert bereits. Überspringe Download.")
        return True
    try:
        print(f"Lade '{filename}' von {url} herunter...")
        response = requests.get(url, stream=True, timeout=10) # Timeout hinzugefügt
        response.raise_for_status() # Löst einen HTTPError für schlechte Antworten (4xx oder 5xx) aus
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Download von '{filename}' abgeschlossen.")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Fehler beim Herunterladen von {url} zu {filename}: {e}")
        return False

# --- Soundeffekte laden (Versuche, sie herunterzuladen und dann zu laden) ---
flap_sound = None
hit_sound = None
point_sound = None
background_music_file_path = None # Variable für den Pfad der Musikdatei

# Versuche, die Sounds herunterzuladen und zu laden
if download_file(SOUND_URLS["flap"], "wing.wav"):
    try:
        flap_sound = pygame.mixer.Sound("wing.wav")
    except pygame.error as e:
        print(f"Fehler beim Laden von wing.wav: {e}")

if download_file(SOUND_URLS["hit"], "hit.wav"):
    try:
        hit_sound = pygame.mixer.Sound("hit.wav")
    except pygame.error as e:
        print(f"Fehler beim Laden von hit.wav: {e}")

if download_file(SOUND_URLS["point"], "point.wav"):
    try:
        point_sound = pygame.mixer.Sound("point.wav")
    except pygame.error as e:
        print(f"Fehler beim Laden von point.wav: {e}")

if download_file(SOUND_URLS["music"], "background_music.wav"):
    background_music_file_path = "background_music.wav"
    try:
        pygame.mixer.music.load(background_music_file_path)
        pygame.mixer.music.set_volume(0.5)
    except pygame.error as e:
        print(f"Fehler beim Laden der Hintergrundmusik: {e}")
        background_music_file_path = None


# Vogel-Design (Pixelgenau)
def draw_bird(x, y):
    # Körper
    pygame.draw.ellipse(screen, BIRD_YELLOW, (x, y, BIRD_WIDTH, BIRD_HEIGHT))
    # Kopf
    pygame.draw.circle(screen, BIRD_YELLOW, (x + 25, y + 10), 12)
    # Auge
    pygame.draw.circle(screen, WHITE, (x + 30, y + 6), 5)
    pygame.draw.circle(screen, BLACK, (x + 30, y + 6), 2)
    # Schnabel
    pygame.draw.polygon(screen, BIRD_RED, [
        (x + 34, y + 10),
        (x + 44, y + 6),
        (x + 44, y + 14)
    ])
    # Flügel (animiert)
    wing_y = y + 12 + 3 * math.sin(pygame.time.get_ticks() / 150)
    pygame.draw.ellipse(screen, BIRD_YELLOW, (x - 5, wing_y, 20, 10))

# Spielvariablen
bird_x = 100
bird_y = 300
bird_speed = 0
pipes = []
score = 0
high_score = 0
game_active = False
font = pygame.font.SysFont('Arial', 50, bold=True)
passed_pipes = set()
background_music_playing = False # Flag, um den Zustand der Musik zu verfolgen

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
                if pygame.mixer.music.get_busy():
                    pygame.mixer.music.stop()
                background_music_playing = False # Reset the flag
                
            else:
                # Sprung
                bird_speed = FLAP_STRENGTH
                if flap_sound:
                    flap_sound.play()

    # Spiele Hintergrundmusik, wenn das Spiel aktiv ist und die Musik noch nicht läuft
    if game_active and not background_music_playing and background_music_file_path:
        pygame.mixer.music.play(-1) # -1 bedeutet, dass die Musik in einer Schleife gespielt wird
        background_music_playing = True
    elif not game_active and background_music_playing: # Stoppe die Musik, wenn das Spiel nicht aktiv ist
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
        draw_bird(bird_x, bird_y)
    
    # Punktestand
    score_text = font.render(str(score), True, WHITE)
    screen.blit(score_text, (screen.get_width() // 2 - score_text.get_width() // 2, 100))
    
    # Start/Game Over Menü
    if not game_active:
        if score > high_score:
            high_score = score

        if score > 0: # Display "Game Over" and restart if a game was played
            game_over_text = font.render("Game Over", True, RED)
            score_display_text = font.render(f"Score: {score}", True, WHITE)
            high_score_text = font.render(f"High Score: {high_score}", True, WHITE)
            restart_text = font.render("Press SPACE to restart", True, WHITE)

            screen.blit(game_over_text, (screen.get_width() // 2 - game_over_text.get_width() // 2, 150))
            screen.blit(score_display_text, (screen.get_width() // 2 - score_display_text.get_width() // 2, 220))
            screen.blit(high_score_text, (screen.get_width() // 2 - high_score_text.get_width() // 2, 280))
            screen.blit(restart_text, (screen.get_width() // 2 - restart_text.get_width() // 2, 350))
        else: # Display "Press SPACE to start" at the very beginning
            start_text = font.render("Press SPACE to start", True, WHITE)
            high_score_text = font.render(f"High Score: {high_score}", True, WHITE)
            
            screen.blit(start_text, (screen.get_width() // 2 - start_text.get_width() // 2, 280))
            screen.blit(high_score_text, (screen.get_width() // 2 - high_score_text.get_width() // 2, 340))
            draw_bird(bird_x, bird_y)
            
    pygame.display.update()
    clock.tick(60)
