#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Komplette, selbstständige Version des Flappy Bird Spiels in Python mit Pygame.
# Sounds und Musik werden direkt im Code generiert, ohne externe Dateien.

import pygame
import random
import sys
import math
import array

# Initialisierung von Pygame und dem Mixer für Sound
pygame.init()
pygame.mixer.init()

# Setup des Mixers, um die Soundgenerierung zu ermöglichen
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.set_reserved(1)

screen = pygame.display.set_mode((400, 600))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()

# --- Spiel-Einstellungen und Farben ---
SKY_BLUE = (107, 187, 255)
# Neue Farben für die Rohre im Flappy Bird-Stil
PIPE_GREEN = (110, 184, 49)
PIPE_DARK_GREEN = (64, 107, 28)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
# Überarbeitete Farben für den Vogel
BIRD_ORANGE = (255, 165, 0)
BIRD_DARK_ORANGE = (200, 100, 0)
BIRD_RED = (255, 77, 0)
BIRD_WHITE = (255, 255, 255) # Weiße Farbe für den Bauch
RED = (255, 0, 0)
GROUND_BROWN = (222, 175, 94)
GROUND_DARK_BROWN = (200, 150, 70)

BIRD_WIDTH = 34
BIRD_HEIGHT = 24
GRAVITY = 0.25 # Die Gravitationskraft, die den Vogel nach unten zieht
FLAP_STRENGTH = -7.5 # Die Stärke des Flap-Sprungs. Ein negativer Wert für Bewegung nach oben.
FLAP_DELAY_MS = 100 # Eine kurze Verzögerung in Millisekunden, um Flap-Spamming zu verhindern.

# Dynamische Schwierigkeitseinstellungen
INITIAL_PIPE_SPEED = 2.0
MAX_PIPE_SPEED = 5.0

# Der Abstand zwischen den Rohren ist jetzt breiter
PIPE_GAP = 130 
PIPE_WIDTH = 52
GROUND_HEIGHT = 500

# --- Soundeffekte im Code generieren ---
def generate_tone(frequency, duration_ms, volume=0.5, sample_rate=44100):
    num_samples = int(sample_rate * duration_ms / 1000)
    max_amplitude = 2**15 - 1
    samples = []
    for i in range(num_samples):
        t = float(i) / sample_rate
        sample = int(max_amplitude * volume * math.sin(2 * math.pi * frequency * t))
        samples.append(sample)
    
    sound_array = array.array('h', samples)
    return pygame.mixer.Sound(sound_array)

try:
    flap_sound = generate_tone(frequency=880, duration_ms=50, volume=0.2)
    hit_sound = generate_tone(frequency=220, duration_ms=250, volume=0.4)
    point_sound = generate_tone(frequency=1000, duration_ms=40, volume=0.3)
    
    def generate_music_loop():
        music_samples = []
        notes = [261.63, 329.63, 392.00, 329.63, 261.63, 329.63, 392.00, 329.63]
        note_duration_ms = 125
        sample_rate = 44100
        max_amplitude = 2**15 - 1
        
        for note_freq in notes:
            num_samples = int(sample_rate * note_duration_ms / 1000)
            for i in range(num_samples):
                t = float(i) / sample_rate
                sample = int(max_amplitude * 0.2 * math.sin(2 * math.pi * note_freq * t))
                music_samples.append(sample)
        
        music_array = array.array('h', music_samples)
        return pygame.mixer.Sound(music_array)
    
    background_music = generate_music_loop()
    background_music.set_volume(0.2)
    
except Exception as e:
    print(f"Fehler bei der Sound-Generierung: {e}")
    flap_sound = None
    hit_sound = None
    point_sound = None
    background_music = None

def draw_centered_text(surface, text, font, color, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(surface.get_width() // 2, y))
    surface.blit(text_surface, text_rect)

def draw_bird(x, y, bird_speed):
    # Logik für die Rotation des Vogels
    rotation = -bird_speed * 3.5
    if bird_speed < -5:
        rotation = 20
    elif bird_speed > 10:
        rotation = -90

    bird_surface = pygame.Surface((BIRD_WIDTH + 20, BIRD_HEIGHT + 20), pygame.SRCALPHA)
    
    # Hauptkörper
    pygame.draw.ellipse(bird_surface, BIRD_ORANGE, (0, 0, BIRD_WIDTH, BIRD_HEIGHT))
    
    # Kopf
    pygame.draw.circle(bird_surface, BIRD_ORANGE, (BIRD_WIDTH + 5, BIRD_HEIGHT // 2), 12)
    
    # Weißer Bauchfleck
    pygame.draw.ellipse(bird_surface, BIRD_WHITE, (0, BIRD_HEIGHT - 10, BIRD_WIDTH - 5, 10))
    
    # Auge
    pygame.draw.circle(bird_surface, BLACK, (BIRD_WIDTH + 8, BIRD_HEIGHT // 2 - 5), 4)
    pygame.draw.circle(bird_surface, WHITE, (BIRD_WIDTH + 9, BIRD_HEIGHT // 2 - 6), 2)
    
    # Schnabel
    pygame.draw.polygon(bird_surface, BIRD_RED, [
        (BIRD_WIDTH + 12, BIRD_HEIGHT // 2 - 3),
        (BIRD_WIDTH + 22, BIRD_HEIGHT // 2),
        (BIRD_WIDTH + 12, BIRD_HEIGHT // 2 + 3)
    ])
    
    # Flügel
    wing_y = BIRD_HEIGHT // 2 + 5 * math.sin(pygame.time.get_ticks() / 150)
    pygame.draw.ellipse(bird_surface, BIRD_DARK_ORANGE, (5, wing_y, 25, 10))

    rotated_bird = pygame.transform.rotate(bird_surface, rotation)
    rotated_bird_rect = rotated_bird.get_rect(center=(x + BIRD_WIDTH / 2, y + BIRD_HEIGHT / 2))
    screen.blit(rotated_bird, rotated_bird_rect)

def draw_menu(score, high_score, game_active):
    if not game_active:
        font_large = pygame.font.Font(None, 60)
        font_medium = pygame.font.Font(None, 36)
        screen_center_y = screen.get_height() // 2

        if score > 0:
            draw_centered_text(screen, "Game Over", font_large, RED, screen_center_y - 100)
            draw_centered_text(screen, f"Score: {score}", font_medium, WHITE, screen_center_y - 40)
            draw_centered_text(screen, f"High Score: {high_score}", font_medium, WHITE, screen_center_y + 10)
            draw_centered_text(screen, "Drücke LEERTASTE zum Neustart", font_medium, WHITE, screen_center_y + 70)
        else:
            draw_centered_text(screen, "Drücke LEERTASTE zum Starten", font_medium, WHITE, screen_center_y)
            draw_centered_text(screen, f"High Score: {high_score}", font_medium, WHITE, screen_center_y + 60)
            draw_bird(bird_x, bird_y, 0)
        
        if not background_music:
            error_font = pygame.font.Font(None, 24)
            draw_centered_text(screen, "Musik konnte nicht generiert werden.", error_font, RED, screen_center_y + 150)

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
music_channel = pygame.mixer.Channel(0)
last_flap_time = 0

# Variablen für die dynamische Schwierigkeit
current_pipe_speed = INITIAL_PIPE_SPEED

def create_pipe():
    gap_y = random.randint(200, 400)
    return [
        pygame.Rect(400, 0, PIPE_WIDTH, gap_y - PIPE_GAP // 2),
        pygame.Rect(400, gap_y + PIPE_GAP // 2, PIPE_WIDTH, 600)
    ]

# Hauptspiel-Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if not game_active:
                game_active = True
                bird_y = 300
                bird_speed = 0
                pipes = []
                score = 0
                passed_pipes = set()
                # Setze Schwierigkeit zurück
                current_pipe_speed = INITIAL_PIPE_SPEED
                if background_music:
                    music_channel.play(background_music, -1)
            else:
                # Verbesserter Sprung: Prüfe auf Verzögerung
                now = pygame.time.get_ticks()
                if now - last_flap_time > FLAP_DELAY_MS:
                    bird_speed = FLAP_STRENGTH
                    if flap_sound:
                        flap_sound.play()
                    last_flap_time = now

    if not game_active and music_channel.get_busy():
        music_channel.stop()

    if game_active:
        bird_speed += GRAVITY
        bird_y += bird_speed

        # Logik zur dynamischen Schwierigkeitsanpassung
        if score > 0 and score % 10 == 0 and score not in passed_pipes:
            if current_pipe_speed < MAX_PIPE_SPEED:
                current_pipe_speed += 0.2
        
        if len(pipes) == 0 or pipes[-1][0].x < 250:
            pipes.append(create_pipe())

        for pipe_pair in pipes[:]:
            for pipe in pipe_pair:
                pipe.x -= current_pipe_speed
            if pipe_pair[0].right < 0:
                pipes.remove(pipe_pair)
        
        # Verbesserte Kollisionserkennung: Verwende eine kleinere Kollisionsbox für den Vogel
        bird_rect = pygame.Rect(bird_x + 5, bird_y + 5, BIRD_WIDTH - 10, BIRD_HEIGHT - 10)
        for pipe_pair in pipes:
            for pipe in pipe_pair:
                if bird_rect.colliderect(pipe):
                    game_active = False
                    if hit_sound:
                        hit_sound.play()
                    if score > high_score:
                        high_score = score
            
        if bird_y > GROUND_HEIGHT - BIRD_HEIGHT or bird_y < 0:
            game_active = False
            if hit_sound:
                hit_sound.play()
            if score > high_score:
                high_score = score

        for pipe_pair in pipes:
            if pipe_pair[0].right < bird_x and id(pipe_pair) not in passed_pipes:
                score += 1
                passed_pipes.add(id(pipe_pair))
                if point_sound:
                    point_sound.play()

    screen.fill(SKY_BLUE)
    
    # Hier werden die Rohre mit der neuen Grafik gezeichnet
    for pipe_pair in pipes:
        # Hauptkörper des oberen und unteren Rohrs
        pygame.draw.rect(screen, PIPE_GREEN, pipe_pair[0])
        pygame.draw.rect(screen, PIPE_GREEN, pipe_pair[1])
        # Kappe des oberen Rohrs
        pipe_cap_top_rect = pygame.Rect(pipe_pair[0].x - 3, pipe_pair[0].y + pipe_pair[0].height, PIPE_WIDTH + 6, 15)
        pygame.draw.rect(screen, PIPE_GREEN, pipe_cap_top_rect)
        # Kappe des unteren Rohrs
        pipe_cap_bottom_rect = pygame.Rect(pipe_pair[1].x - 3, pipe_pair[1].y - 15, PIPE_WIDTH + 6, 15)
        pygame.draw.rect(screen, PIPE_GREEN, pipe_cap_bottom_rect)
        # Dunklere Umrandung und Kappen
        pygame.draw.rect(screen, PIPE_DARK_GREEN, pipe_pair[0], 3)
        pygame.draw.rect(screen, PIPE_DARK_GREEN, pipe_pair[1], 3)
        pygame.draw.rect(screen, PIPE_DARK_GREEN, pipe_cap_top_rect, 3)
        pygame.draw.rect(screen, PIPE_DARK_GREEN, pipe_cap_bottom_rect, 3)
    
    # Zeichne den Boden mit einem Muster, um die Textur zu simulieren
    for i in range(0, 400, 20):
        color = GROUND_BROWN if (i // 20) % 2 == 0 else GROUND_DARK_BROWN
        pygame.draw.rect(screen, color, (i, GROUND_HEIGHT, 20, 100))
    
    if game_active:
        draw_bird(bird_x, bird_y, bird_speed)
    
    score_text = font.render(str(score), True, WHITE)
    score_rect = score_text.get_rect(center=(screen.get_width() // 2, 100))
    screen.blit(score_text, score_rect)
    
    if not game_active:
        if score > high_score:
            high_score = score
        draw_menu(score, high_score, game_active)
            
    pygame.display.update()
    clock.tick(60)
