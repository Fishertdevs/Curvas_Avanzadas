import pygame
import os
import math
from Curve import Curve
import colorsys
import numpy as np

# Configuración inicial
os.environ["SDL_VIDEO_CENTERED"] = '1'
width, height = 1280, 720
size = (width, height)
fps = 60

# Colores
white, black, gray, red = (245, 245, 245), (15, 15, 15), (150, 150, 150), (255, 50, 50)

# Parámetros iniciales
w = 140
speed = 0.01
radius_factor = 0.8
restart = False
angle = 0

# Inicialización de Pygame
pygame.init()
pygame.display.set_caption("Curvas avanzadas")
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 20)

# Configuración de la cuadrícula
columns = width // w - 1
rows = height // w - 1
radius = int((w // 2) * radius_factor)
curves = [[None for _ in range(columns)] for _ in range(rows)]

# Función para convertir HSV a RGB
def hsv_to_rgb(h, s, v):
    return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h, s, v))

# Inicializar curvas con colores únicos
def initialize_curves():
    h = 0
    for x in range(rows):
        for y in range(columns):
            curves[x][y] = Curve(hsv_to_rgb(h, 1, 1))
            h += 0.001

# Dibujar texto en pantalla
def draw_text(text, x, y, color=white):
    label = font.render(text, True, color)
    screen.blit(label, (x, y))

# Dibujar círculos y líneas guía
def draw_guides():
    for i in range(columns):
        a = w + 10 + i * w + w // 2
        b = w // 2 + 15
        pygame.draw.circle(screen, white, (a, b), radius, 1)
        x = radius * math.cos(angle * (i + 1) - math.pi / 2)
        pygame.draw.line(screen, gray, (int(a + x), 0), (int(a + x), height), 1)
        pygame.draw.circle(screen, red, (int(a + x), b), 8)
        for j in range(rows):
            curves[j][i].set_point_x(a + x)

    for j in range(rows):
        a = w // 2 + 15
        b = w + 10 + j * w + w // 2
        pygame.draw.circle(screen, white, (a, b), radius, 1)
        y = radius * math.sin(angle * (j + 1) - math.pi / 2)
        pygame.draw.line(screen, gray, (0, int(b + y)), (width, int(b + y)), 1)
        pygame.draw.circle(screen, red, (a, int(b + y)), 8)
        for i in range(columns):
            curves[j][i].set_point_y(b + y)

# Actualizar y dibujar curvas
def update_and_draw_curves():
    for x in range(rows):
        for y in range(columns):
            curves[x][y].update_points()
            curves[x][y].draw(screen)

# Reiniciar curvas
def reset_curves():
    global angle, restart
    for x in range(rows):
        for y in range(columns):
            curves[x][y].points = []
    angle = 0
    restart = False

# Manejar eventos del usuario
def handle_events():
    global run, restart, speed, radius_factor
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False
            if event.key == pygame.K_r:
                restart = True
            if event.key == pygame.K_UP:
                speed += 0.005
            if event.key == pygame.K_DOWN:
                speed = max(0.005, speed - 0.005)
            if event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                radius_factor = min(1.0, radius_factor + 0.05)
            if event.key == pygame.K_MINUS:
                radius_factor = max(0.5, radius_factor - 0.05)
    return True

# Inicializar curvas
initialize_curves()

# Bucle principal
run = True
while run:
    clock.tick(fps)
    screen.fill(black)

    # Manejar eventos
    run = handle_events()

    # Dibujar guías y curvas
    draw_guides()
    update_and_draw_curves()

    # Reiniciar si es necesario
    if restart:
        reset_curves()

   # Dibujar información en pantalla
    draw_text(f"Velocidad: {speed:.3f}", 10, 10)
    draw_text("Controles: [R] Reiniciar | [↑/↓] Velocidad | [+/-] Tamaño", 10, 40)

    # Mostrar crédito al lado derecho de los controles
    draw_text("Desarrollado por Harry Fishert - GitHub", 500, 40, gray)

    # Actualizar ángulo
    angle -= speed
    if angle < -2 * math.pi:
        reset_curves()

    pygame.display.update()

pygame.quit()