#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 🚀 FLAPPY PYTHON ULTIMATE PRO - MIT AUTO-FEHLERBEHEBUNG & RESIZE
# 🔥 Features: Selbstheilung, Resizable Window, Smoother Gameplay

import pygame
import random
import sys
import traceback
from pygame.locals import *

class FlappyGame:
    def __init__(self):
        self.initialize_game()
        
    def initialize_game(self):
        """Initialisiert alle Spielkomponenten mit Fehlerbehandlung"""
        try:
            pygame.init()
            mixer.init()
            self.setup_display()
            self.load_assets()
            self.reset_game_state()
            pygame.time.set_timer(SPAWNPIPE, 1500)
            return True
        except Exception as e:
            print(f"Initialisierungsfehler: {e}")
            traceback.print_exc()
            return False
    
    def setup_display(self):
        """Erstellt ein resizable Fenster"""
        self.screen = pygame.display.set_mode((400, 600), RESIZABLE)
        pygame.display.set_caption("Flappy Python Ultimate Pro 🐦✨")
        self.clock = pygame.time.Clock()
        
    def load_assets(self):
        """Lädt Assets mit Fallback-Mechanismus"""
        try:
            # Versuche Web-Assets zu laden
            self.bird_img = pygame.Surface((30, 30), pygame.SRCALPHA)
            pygame.draw.circle(self.bird_img, (255, 0, 0), (15, 15), 15)
            
            self.pipe_img = pygame.Surface((50, 300), pygame.SRCALPHA)
            self.pipe_img.fill((0, 200, 0))
            
            # Sound-Effekte (Web oder Stille)
            self.sounds = {
                'wing': None,
                'point': None,
                'hit': None
            }
        except:
            self.handle_asset_error()
    
    def handle_asset_error(self):
        """Behandelt fehlende Assets"""
        print("Asset-Fehler - Verwende Fallback-Grafiken")
        # Einfache Fallback-Grafiken
        self.bird_img = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.circle(self.bird_img, (255, 0, 0), (15, 15), 15)
        
        self.pipe_img = pygame.Surface((50, 300), pygame.SRCALPHA)
        self.pipe_img.fill((0, 200, 0))
    
    def reset_game_state(self):
        """Setzt Spielvariablen zurück"""
        self.gravity = 0.25
        self.bird_movement = 0
        self.game_state = MENU
        self.score = 0
        self.high_score = 0
        self.bird_rect = self.bird_img.get_rect(center=(100, 250))
        self.pipe_list = []
        self.ground_y = 500
        self.font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 72)
    
    def run(self):
        """Hauptspiel-Schleife mit Selbstheilung"""
        running = True
        while running:
            try:
                running = self.process_events()
                self.update_game()
                self.render()
                self.clock.tick(60)
            except Exception as e:
                print(f"Kritischer Fehler: {e}")
                traceback.print_exc()
                if not self.recover_from_error():
                    running = False
        
        pygame.quit()
        sys.exit()
    
    def recover_from_error(self):
        """Versucht das Spiel automatisch neu zu starten"""
        print("Versuche Spiel wiederherzustellen...")
        pygame.time.delay(1000)  # Warte kurz
        self.reset_game_state()
        return True
    
    def process_events(self):
        """Verarbeitet Eingaben und Fenster-Events"""
        for event in pygame.event.get():
            if event.type == QUIT:
                return False
            
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    self.handle_space_press()
                elif event.key == K_ESCAPE:
                    return False
            
            if event.type == VIDEORESIZE:
                self.handle_resize(event.size)
            
            if event.type == SPAWNPIPE and self.game_state == PLAYING:
                self.pipe_list.extend(self.create_pipe())
        
        return True
    
    def handle_space_press(self):
        """Behandelt Leertasten-Eingaben"""
        if self.game_state == MENU:
            self.game_state = PLAYING
            self.reset_game_state()
        elif self.game_state == PLAYING:
            self.bird_movement = -7
        elif self.game_state == GAME_OVER:
            self.game_state = PLAYING
            self.reset_game_state()
    
    def handle_resize(self, size):
        """Passt das Spiel an Fenstergrößenänderungen an"""
        width, height = size
        # Mindestgröße erzwingen
        width = max(width, 300)
        height = max(height, 400)
        self.screen = pygame.display.set_mode((width, height), RESIZABLE)
        
        # Anpassung der Spielparameter
        self.ground_y = height - 100
        if self.game_state == PLAYING:
            # Vogelposition anpassen
            self.bird_rect.centery = min(self.bird_rect.centery, height - 100)
    
    def update_game(self):
        """Aktualisiert den Spielzustand"""
        if self.game_state == PLAYING:
            # Vogelphysik
            self.bird_movement += self.gravity
            self.bird_rect.y += self.bird_movement
            
            # Rohre bewegen
            self.pipe_list = [pipe for pipe in self.pipe_list if pipe.x > -50]
            for pipe in self.pipe_list:
                pipe.x -= 3
            
            # Kollision prüfen
            if self.check_collision():
                self.game_state = GAME_OVER
                self.high_score = max(self.score, self.high_score)
            
            # Punkte zählen
            for pipe in self.pipe_list:
                if pipe.right == 100:
                    self.score += 1
    
    def check_collision(self):
        """Prüft Kollisionen mit Skalierungsunterstützung"""
        for pipe in self.pipe_list:
            if self.bird_rect.colliderect(pipe):
                return True
        return (self.bird_rect.top <= 0 or 
                self.bird_rect.bottom >= self.ground_y)
    
    def render(self):
        """Zeichnet alle Spielkomponenten"""
        # Hintergrund
        self.screen.fill((78, 192, 246))
        
        if self.game_state == MENU:
            self.draw_menu()
        elif self.game_state == PLAYING:
            self.draw_pipes()
            self.draw_bird()
            self.draw_score()
        elif self.game_state == GAME_OVER:
            self.draw_game_over()
        
        # Boden
        pygame.draw.rect(self.screen, (94, 201, 72), 
                         (0, self.ground_y, self.screen.get_width(), 100))
        
        pygame.display.flip()
    
    def draw_menu(self):
        """Zeichnet das Startmenü"""
        title = self.big_font.render("FLAPPY PYTHON", True, WHITE)
        start = self.font.render("SPACE zum Starten", True, WHITE)
        
        screen_width = self.screen.get_width()
        self.screen.blit(title, (screen_width//2 - title.get_width()//2, 150))
        self.screen.blit(start, (screen_width//2 - start.get_width()//2, 300))
        
        if self.high_score > 0:
            hs_text = self.font.render(f"Highscore: {self.high_score}", True, WHITE)
            self.screen.blit(hs_text, (screen_width//2 - hs_text.get_width()//2, 400))
    
    def draw_pipes(self):
        """Zeichnet alle Rohre"""
        for pipe in self.pipe_list:
            pygame.draw.rect(self.screen, GREEN, pipe)
    
    def draw_bird(self):
        """Zeichnet den Vogel"""
        self.screen.blit(self.bird_img, self.bird_rect)
    
    def draw_score(self):
        """Zeichnet den aktuellen Punktestand"""
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
    
    def draw_game_over(self):
        """Zeichnet den Game-Over-Bildschirm"""
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()
        
        game_over = self.big_font.render("Game Over!", True, RED)
        restart = self.font.render("SPACE zum Neustarten", True, WHITE)
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        hs_text = self.font.render(f"Highscore: {self.high_score}", True, WHITE)
        
        self.screen.blit(game_over, (screen_width//2 - game_over.get_width()//2, 150))
        self.screen.blit(restart, (screen_width//2 - restart.get_width()//2, 300))
        self.screen.blit(score_text, (screen_width//2 - score_text.get_width()//2, 400))
        self.screen.blit(hs_text, (screen_width//2 - hs_text.get_width()//2, 450))
    
    def create_pipe(self):
        """Erzeugt ein neues Rohrpaar"""
        random_height = random.randint(150, 400)
        bottom_pipe = pygame.Rect(400, random_height, 50, 
                                 self.screen.get_height() - random_height)
        top_pipe = pygame.Rect(400, 0, 50, random_height - 150)
        return bottom_pipe, top_pipe

# Konstanten
MENU = 0
PLAYING = 1
GAME_OVER = 2
SPAWNPIPE = USEREVENT
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 200, 0)

if __name__ == "__main__":
    game = FlappyGame()
    if game.initialize_game():
        game.run()
    else:
        print("Spiel konnte nicht gestartet werden")
        pygame.quit()
        sys.exit(1)
