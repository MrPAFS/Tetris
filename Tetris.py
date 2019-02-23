# -*- coding: utf-8 -*-
"""
Created on Mon Feb 18 20:56:13 2019

@author: Casa
"""

import pygame
from random import randint
from Mesh import Mesh
from Block import Block

def adjust_block_position_x(position_x,block,mesh_size_x):
    array_of_block = block.get_array_of_block()
    
    move = 0
    
    if position_x < 0:
        for k in range(0,2):
            for i in range(5):
                if array_of_block[i][k] == 1:
                    move += 1
                    break
        position_x += move
    elif position_x > mesh_shape[0] - 5:
        move = 0
        for k in range(4,-1,-1):
            for i in range(5):
                if array_of_block[i][k] == 1:
                    move = mesh_size_x - k - 1
                    break
                if move != 0:
                    break
        position_x = move
    
    return position_x

def generate_random_Block(mesh_shape):
    
    possible_blocs_name = ['I','T','L','S-NORMAL','S-INVERTED','O']
    block_name = possible_blocs_name[randint(0,5)]
    block = Block(block_name)
    
    how_many_rotation = randint(0,4)
    for i in range(how_many_rotation):
        block.rotate_right()
    
    position_y = -5
    temp = randint(-2,mesh_shape[0])
    print(temp)
    position_x = adjust_block_position_x(temp, block,mesh_shape[0])
    
    return (block,position_x,position_y)

def draw_block(block, background,color,position_x,position_y,square_size):
    array_of_block = block.get_array_of_block()
    for i in range(5):
        for k in range(5):
            if array_of_block[i][k] == 1:
                pygame.draw.rect(background,color,((position_x + k)*20,(position_y + i)*20, square_size, square_size))

#             WHITE      DeepSkyBlue    RED      YELLOW   SpringGreen  DarkViolet     Silver
colors = [(255,255,255),(0,191,255),(255,0,0),(255,255,0),(0,255,127),(148,0,211),(192,192,192)]
screen_shape = (480,640)
square_size = 20
drop_speed = 0.1
mesh_shape = (int(screen_shape[0]/square_size),int(screen_shape[1]/square_size))

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
