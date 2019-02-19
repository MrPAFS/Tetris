# -*- coding: utf-8 -*-
"""
Created on Mon Feb 18 20:56:13 2019

@author: Casa
"""

import pygame
from random import randint
from Mesh import Mesh
from Block import Block

def generate_random_Block(mesh_shape):
    
    possible_blocs_name = ['I','T','L','S-NORMAL','S-INVERTED','O']
    block_name = possible_blocs_name[randint(0,6)]
    block = Block(block_name)
    
    how_many_rotation = randint(0,4)
    for i in range(how_many_rotation):
        block.rotate_right()
    
    position_y = randint(0,mesh_shape[0])
    position_x = randint(0,mesh_shape[1])
    
    return (block,position_x,position_y)

#             WHITE      DeepSkyBlue    RED      YELLOW   SpringGreen  DarkViolet     Silver
colors = [(255,255,255),(0,191,255),(255,0,0),(255,255,0),(0,255,127),(148,0,211),(192,192,192)]
screen_shape = (480,640)
rect_size = 20
drop_speed = 0.1
mesh_shape = (screen_shape[0]/rect_size,screen_shape[1]/rect_size)

mesh = Mesh(mesh_shape)

pygame.display.init()
background = pygame.display.set_mode(screen_shape)

play = True
while play:
    
    background.fill(colors[0])
    pygame.display.update()
    
    for event in pygame.event.get():
        print(event)
        
        if event.type == pygame.QUIT:
            play = False
    
pygame.display.quit()