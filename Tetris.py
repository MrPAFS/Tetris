# -*- coding: utf-8 -*-
"""
Created on Mon Feb 18 20:56:13 2019

@author: Casa
"""

import pygame
from random import randint
from random import choice
from Mesh import Mesh
from Block import Block

def generate_random_Block():
    
    possible_blocs_name = ['I','T','L-NORMAL','L-INVERTED','S-NORMAL','S-INVERTED','O']
    block_name = choice(possible_blocs_name)
    block = Block(block_name)
    
    how_many_rotation = randint(0,4)
    for i in range(how_many_rotation):
        block.rotate_clockwise()
    
    return block

def draw_block(block,color,position_x,position_y):
    array_of_block = block.get_array_of_block()
    for i in range(5):
        for k in range(5):
            if array_of_block[i][k] == 1:
                pygame.draw.rect(background,color,((position_x + k)*square_size,(position_y + i)*square_size, square_size, square_size))

def draw_mesh(mesh,blockColor):
    array_of_mesh = mesh.get_array_of_mesh()
    shape = mesh.get_shape()
    for i in range(shape[0]):
        for j in range(shape[1]):
            if(array_of_mesh[i][j] == 1):
                 pygame.draw.rect(background,blockColor,(j*square_size,i*square_size, square_size, square_size))

def switch(movent):
    return {
            'DOWN':(0,1),
            'LEFT':(-1,0),
            'RIGHT':(1,0)}[movent];
    
def move(block,movement,position_x,position_y):
    move_x,move_y = switch(movement)
    
    position_x += move_x
    position_y += move_y
    
    return (position_x,position_y)

def rotate(block,direction):
    if(direction == 'CLOCKWISE'):
        block.rotate_clockwise()
    elif(direction == 'ANTICLOCKWISE'):
        block.rotate_anticlockwise()
        
def adjust(block,pos_x):
    for i in range(5):
        for k in range(5):
            if (block.get_array_of_block()[k][i] == 1) & (pos_x + i < 0):
                pos_x += 1
                break;
            elif (block.get_array_of_block()[k][i] == 1) & (pos_x + i >= screen_shape[0]/square_size):
                pos_x -= 1
                break;
                
    return pos_x


def stopCriterion(mesh,block,pos_x,pos_y):
    array_of_block = block.get_array_of_block()
    array_of_mesh = mesh.get_array_of_mesh()
    
    for i in range(0,5):
        for j in range(0,5):
            if (array_of_block[i][j] == 1):
                if pos_y+i+1 == mesh.get_shape()[0]:
                    return True
                if array_of_mesh[int(pos_y)+i+1][pos_x+j] == 1:
                    return True
    
    return False
    
    
    
    

#             WHITE      DeepSkyBlue    RED      YELLOW   SpringGreen  DarkViolet     Silver
colors = [(255,255,255),(0,191,255),(255,0,0),(255,255,0),(0,255,127),(148,0,211),(192,192,192)]
screen_shape = (480,640)
square_size = 20
drop_speed = 0.5
mesh_shape = (int(screen_shape[1]/square_size),int(screen_shape[0]/square_size))

mesh = Mesh(mesh_shape)

pos_x = 9
pos_y = 0

pygame.display.init()
background = pygame.display.set_mode(screen_shape)

play = True

block = generate_random_Block()

clock = pygame.time.Clock()
while play:
    
    for event in pygame.event.get():
        print(event)
        
        if event.type == pygame.QUIT:
            play = False
        elif event.type == pygame.KEYDOWN:
            if event.key == 275:
                pos_x,pos_y = move(block,'RIGHT',pos_x,pos_y)
            elif event.key == 276:
                pos_x,pos_y = move(block,'LEFT',pos_x,pos_y)
            elif event.key == 100:
                rotate(block,'CLOCKWISE')
            elif event.key == 97:
                rotate(block,'ANTICLOCKWISE')
            pos_x = adjust(block,pos_x)
    
    pos_y += drop_speed
    
    background.fill(colors[0])
    draw_block(block,colors[1],pos_x,pos_y)
    draw_mesh(mesh,colors[1])
    pygame.display.update()
    
    if int(pos_y) == pos_y:
        if stopCriterion(mesh,block,pos_x,pos_y):
            mesh.add_block(block,(int(pos_y),int(pos_x)))
            block = generate_random_Block()
            pos_x = 9
            pos_y = 0
            
    
    clock.tick(12)

pygame.display.quit()
