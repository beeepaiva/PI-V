import sys
import pygame
import random
from threading import Thread
import SIR

# Parâmetros do tamanho da simulação (cada célula em 5 pixels)
random.seed(None)
size = width, height = 500, 700
width_surface = width/5
height_surface = height/5
still = False

# Estes são os códigos de cor que o pygame usa ((R,G,B))
black = ((0,0,0))
red = ((255,0,0))
blue = ((0,0,255))
green = ((0,255,0))
white = ((255, 255, 255))
colors = [black, blue, red, green, white]

pygame.init()
screen = pygame.display.set_mode(size)
font = pygame.font.SysFont('Calibri', 13)
model = SIR.Map()

# Paint function
def colorize(x, y, color_num):
    screen.set_at((x, y), colors[color_num])
    screen.set_at((x + 1, y), colors[color_num])
    screen.set_at((x, y + 1), colors[color_num])
    screen.set_at((x + 1, y + 1), colors[color_num])
    screen.set_at((x + 2, y), colors[color_num])
    screen.set_at((x, y + 2), colors[color_num])
    screen.set_at((x + 2, y + 2), colors[color_num])
    screen.set_at((x + 2, y + 1), colors[color_num])
    screen.set_at((x + 1, y + 2), colors[color_num])


# Paint map function
def paint_map(surface):
    do_colorize = colorize
    size = len(surface)
    for x in range(0, size):
        for y in range(0, size):
            do_colorize(x*5, y*5, surface[x][y].condition)


# Add count
def addCount():
    screen.blit(font.render('SIR Model', True, (255, 255, 255)), (20, 510))
    screen.blit(font.render('Total population: {}'.format(model.pop), True, (255, 255, 255)), (20, 540))
    screen.blit(font.render('Susceptible: {} [{:.2f} %]'.format(model.susceptible, model.susceptible * 100 / model.pop), True, (255, 255, 255)), (20, 560))
    screen.blit(font.render('Infected: {} [{:.2f} %]'.format(model.infected, model.infected * 100 / model.pop), True, (255, 255, 255)), (20, 580))
    screen.blit(font.render('Immune: {} [{:.2f} %]'.format(model.immune, model.immune * 100 / model.pop), True, (255, 255, 255)), (20, 600))
    screen.blit(font.render('Dead: {} [{:.2f} %]'.format(model.dead, model.dead * 100 / model.pop), True, (255, 255, 255)), (20, 620))

# Sim loop, paints and executes the next turn
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            still = True
            sys.exit(0)
    screen.fill((0, 0, 0))
    paint_map(model.get_surface())
    addCount()
    pygame.display.flip()
    pygame.time.wait(100)
    model.turn()
