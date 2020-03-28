# -*- coding: utf-8 -*-
"""
Created on Mon Feb 18 20:56:13 2019

@author: Casa
"""

import pygame
import time
from random import randint
from random import choice
from Mesh import Mesh
from Block import Block

class Tetris:

    def generate_random_Block(self):

        possible_blocs_name = ['I', 'T', 'L-NORMAL', 'L-INVERTED', 'S-NORMAL', 'S-INVERTED', 'O']   
        block_name = choice(possible_blocs_name)

        color = randint(1, 6)

        block = Block(block_name, color)

        how_many_rotation = randint(0, 4)
        for i in range(how_many_rotation):
            block.rotate_clockwise()

        return block

    #
    def draw_block(self,background, colors, square_size, block, position_x, position_y):
        array_of_block = block.get_array_of_block()
        for i in range(5):
            for k in range(5):
                if array_of_block[i][k] == 1:
                    pygame.draw.rect(background, colors[block.get_color()], ((position_x + k)*square_size, (position_y + i)*square_size, square_size, square_size))

    #
    def draw_mesh(self,background,colors,square_size,mesh,zero_mesh):
        array_of_mesh = mesh.get_array_of_mesh()
        shape = mesh.get_shape()
        
        for i in range(shape[0]):
            for j in range(shape[1]):
                #if(array_of_mesh[i][j] != 0):
                real_pos_x = (j+zero_mesh)*square_size
                pos_y = i*square_size
                pygame.draw.rect(background,colors[int(array_of_mesh[i][j])],(real_pos_x,pos_y, square_size, square_size))

    def switch(self,movent):
        return {
                'DOWN':(0,1),
                'LEFT':(-1,0),
                'RIGHT':(1,0)}[movent]
        
    def move(self,block,movement,position_x,position_y):
        move_x,move_y = self.switch(movement)
        
        position_x += move_x
        position_y += move_y
        
        return (position_x,position_y)

    def rotate(self,block,direction):
        if(direction == 'CLOCKWISE'):
            block.rotate_clockwise()
        elif(direction == 'ANTICLOCKWISE'):
            block.rotate_anticlockwise()
    
    #       
    def adjust(self,mesh,block,real_pos_x,pos_y,zero_mesh):
        array_of_block = block.get_array_of_block()
        array_of_mesh = mesh.get_array_of_mesh()
        shape = mesh.get_shape()
        
        pos_x = real_pos_x - zero_mesh
        
        for i in range(5):
            for k in range(5):
                if array_of_block[k][i] == 1:
                    if pos_x + i < 0:
                        return True
                    elif pos_x + i >= shape[1]:
                        return True
                    elif pos_y+k >= 20:
                        return True
                    elif array_of_mesh[pos_y+k][pos_x+i] != 0:
                        return True
                    
        return False


    #
    def stopCriterion(self,mesh,block,real_pos_x,pos_y,zero_mesh):
        array_of_block = block.get_array_of_block()
        array_of_mesh = mesh.get_array_of_mesh()
        
        pos_x = real_pos_x - zero_mesh
        
        for i in range(0,5):
            for j in range(0,5):
                if (array_of_block[i][j] == 1):
                    if pos_y+i+1 == mesh.get_shape()[0]:
                        return True
                    if array_of_mesh[int(pos_y)+i+1][pos_x+j] != 0:
                        return True
        
        return False
        
    def toTop(self,block,pos_y):
        array_of_block = block.get_array_of_block()
        
        a = 0
        
        while a == 0:
            for i in range(5):
                a += array_of_block[0-pos_y][i]
            if a == 0:
                pos_y -= 1
        
        return pos_y
    #    
    def lose(self,mesh, block,real_pos_x,pos_y,zero_mesh):
        array_of_mesh = mesh.get_array_of_mesh()
        array_of_block = block.get_array_of_block()
        
        pos_x = real_pos_x - zero_mesh
        
        for i in range(4,-1,-1):
            for j in range(5):
                if(array_of_block[i][j] == 1) & (array_of_mesh[i+pos_y][j+pos_x] != 0):
                    return True     
                
        return False

    def calc_score(self,number_of_full_lines):
        return{0:0,
            1:100,
            2:300,
            3:500,
            4:800
                }[number_of_full_lines]
            
    def start_menu(self,background, clock):
        menu = True
        menu_font = pygame.font.SysFont("monospace", 15)
        
        while menu:
            
            background.fill((255,255,255))
            pygame.draw.rect(background,(240,240,240),(62.5,218.75,375,62.5))
            label = menu_font.render("Pressione qualquer tecla para iniciar", 1, (0,0,0))
            background.blit(label, (82.5, 242.5))
            pygame.display.update()
            
            for event in pygame.event.get():
            
                if event.type == pygame.QUIT:
                    return False
                elif event.type == pygame.KEYDOWN:
                    menu = False
                    
            clock.tick(16)
        return True

    def lose_menu(self,background, clock):
        menu = True
        lose_font = pygame.font.SysFont("monospace", 30)
        menu_font = pygame.font.SysFont("monospace", 15)
        
        while menu:
            
            background.fill((255,255,255))
            pygame.draw.rect(background,(240,240,240),(62.5,218.75,375,62.5))
            
            label1 = lose_font.render("Você Perdeu", 1, (255,0,0))
            background.blit(label1, (150, 188.75))
            label2 = menu_font.render("Pressione qualquer tecla para iniciar", 1, (0,0,0))
            background.blit(label2, (82.5, 242.5))
            
            pygame.display.update()
            
            for event in pygame.event.get():
            
                if event.type == pygame.QUIT:
                    return False
                elif event.type == pygame.KEYDOWN:
                    menu = False
                    
            clock.tick(16)
        return True

    def play(self):
        
        zero_mesh = 5
        #             WHITE      DeepSkyBlue    RED      YELLOW   SpringGreen  DarkViolet     Silver     Black
        colors = [(255,255,255),(0,191,255),(255,0,0),(255,255,0),(0,255,127),(148,0,211),(192,192,192),(0,0,0)]
        screen_shape = (500,500)
        square_size = 25
        drop_speed = 1
        mesh_shape = (20,10)

        mesh = Mesh(mesh_shape)

        pos_x = 2 + zero_mesh
        pos_y = 0

        pygame.init()
        background = pygame.display.set_mode(screen_shape)
        score_font = pygame.font.SysFont("monospace", 15)
        pygame.mixer.music.load("Tetris Theme.mp3")

        block = self.generate_random_Block()
        pos_y = self.toTop(block, pos_y)

        score = 0

        clock = pygame.time.Clock()
        timer = time.time()

        play = self.start_menu(background,clock)

        pygame.mixer.music.play(-1)

        while play:
        
            background.fill(colors[7])
        
            self.draw_mesh(background,colors,square_size,mesh,zero_mesh)
            self.draw_block(background,colors,square_size,block,pos_x,pos_y)
            label = score_font.render("Score: " + str(score), 1, colors[0])
            background.blit(label, (0, 0))
            pygame.display.update()
        
            for event in pygame.event.get():
                #print(event)
            
                if event.type == pygame.QUIT:
                    play = False
                elif event.type == pygame.KEYDOWN:
                
                    if event.key == 275:
                        pos_x,pos_y = self.move(block,'RIGHT',pos_x,pos_y)
                    
                        if(self.adjust(mesh,block,pos_x,pos_y,zero_mesh)):
                            pos_x,pos_y = self.move(block,'LEFT',pos_x,pos_y)
                        
                    elif event.key == 276:
                        pos_x,pos_y = self.move(block,'LEFT',pos_x,pos_y)
                    
                        if(self.adjust(mesh,block,pos_x,pos_y,zero_mesh)):
                            pos_x,pos_y = self.move(block,'RIGHT',pos_x,pos_y)
                        
                    elif event.key == 100:
                        self.rotate(block,'CLOCKWISE')
                    
                        if(self.adjust(mesh,block,pos_x,pos_y,zero_mesh)):
                            self.rotate(block,'ANTICLOCKWISE')
                        
                    elif event.key == 97:
                        self.rotate(block,'ANTICLOCKWISE')
                    
                        if(self.adjust(mesh,block,pos_x,pos_y,zero_mesh)):
                            self.rotate(block,'CLOCKWISE')
                        
                    elif event.key ==  274:
                        pos_y += drop_speed
                        score += drop_speed
                    
                        if(self.adjust(mesh,block,pos_x,pos_y,zero_mesh)):
                            pos_y -= drop_speed
                            score -= drop_speed               
        
            if(time.time() - timer >= 0.5):
                pos_y += drop_speed
                if(self.adjust(mesh,block,pos_x,pos_y,zero_mesh)):
                    pos_y -= drop_speed
                timer = time.time()
        
            clock.tick(16)
        
            if pos_y == pos_y:
                if self.stopCriterion(mesh,block,pos_x,pos_y,zero_mesh):
                    mesh.add_block(block,(pos_y,pos_x-zero_mesh))
                    score += self.calc_score(mesh.detect_full_line())
                    block = self.generate_random_Block()
                    pos_x = 2 + zero_mesh
                    pos_y = 0
                    pos_y = self.toTop(block, pos_y)
                
                    if self.lose(mesh,block,pos_x,pos_y,zero_mesh):
                        pygame.mixer.music.stop()
                        if self.lose_menu(background,clock):
                            pygame.mixer.music.play()
                            mesh = Mesh(mesh_shape)
                            score = 0
                        else:
                            break

        pygame.mixer.music.stop()
        pygame.display.quit()

# if __name__ == "__main__":
#     main()