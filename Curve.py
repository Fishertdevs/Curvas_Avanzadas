import pygame
import colorsys
import random

class Curve:
    def __init__(self, color=None, thickness=None):
        """
        Inicializa una curva con un color específico y un grosor opcional.
        Si no se proporciona un color o grosor, se generan aleatoriamente.
        """
        self.points = []  # Lista de puntos que forman la curva
        self.hue = random.random()  # Tono inicial aleatorio para el color
        self.color = color if color else self.hsv_to_rgb(self.hue, 1, 1)  # Color único
        self.thickness = thickness if thickness else random.randint(1, 4)  # Grosor aleatorio
        self.current = [0, 0]  # Coordenadas actuales del punto

    def set_point_x(self, x):
        """
        Establece la coordenada X del punto actual.
        """
        self.current[0] = x

    def set_point_y(self, y):
        """
        Establece la coordenada Y del punto actual.
        """
        self.current[1] = y

    def update_points(self):
        """
        Actualiza la lista de puntos con el punto actual.
        """
        point = (int(self.current[0]), int(self.current[1]))
        if not self.points or self.points[-1] != point:  # Evita duplicados consecutivos
            self.points.append(point)

    def update_color(self):
        """
        Cambia dinámicamente el color de la curva utilizando HSV.
        """
        self.hue += 0.005  # Incrementa el tono
        if self.hue > 1:
            self.hue = 0  # Reinicia el tono si excede 1
        self.color = self.hsv_to_rgb(self.hue, 1, 1)

    @staticmethod
    def hsv_to_rgb(h, s, v):
        """
        Convierte un color HSV a RGB.
        """
        return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h, s, v))

    def draw(self, screen):
        """
        Dibuja la curva en la pantalla.
        """
        # Actualiza el color dinámicamente
        self.update_color()

        # Dibuja las líneas que conectan los puntos
        if len(self.points) > 1:
            pygame.draw.lines(screen, self.color, False, self.points, self.thickness)

        # Dibuja un círculo en el punto actual
        pygame.draw.circle(screen, self.color, (int(self.current[0]), int(self.current[1])), 5)

    def reset(self):
        """
        Reinicia la curva eliminando todos los puntos.
        """
        self.points = []