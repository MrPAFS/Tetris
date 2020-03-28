# -*- coding: utf-8 -*-
"""
    Contém ambientes de simulação para um apredizado de máquina (Reinforcement Learning)
"""

import pygame
import time
from random import randint
from random import choice
from Mesh import Mesh
from Block import Block
from Environment_Exceptions import InvalidAction

"""
    Ambiente para treinamento de uma IA que joga tetris
    
    OBS: O código do arquivo Tetris.py está sendo modificado neste arquivo para melhor adequar para o treinamento de uma rede neural.
"""
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
    
    """
        Constroi um array que constitui a observação do jogo

        Parâmetros:
        -------------------------------------

        Retorno:
            observation: A observação atual do ambiente
    """
    def make_observation():

        array_of_block = self.block.get_array_of_block()
        array_of_mesh = self.block.get_array_of_mesh()

        observation = np.zeros(self.mesh_shape)

        for i in range(self.mesh_shape[0]):
            for j in range(self.mesh_shape[1]):
                if (array_of_mesh[i][j] != 0):
                    observation[i][j] = 1

        for i in range(5):
            for j in range(5):
                if array_of_block[i][j] == 1:
                    observation[self.pos_y + i][self.pos_x + j] = 1

        return observation

    """
        Inicia o ambiente de jogo tetris

        Parâmetros
        ------------------------------------- 

        Retorno
        -------------------------------------

    """
    def __init__(self):

        self.mesh_shape = (20,10)

        return

    """
        Inicia a simulação do jogo tetris

        Parâmetros
        -------------------------------------

        Retorno

            observation: A observação atual do ambiente
            score: A pontuação inicial do jogo, usada futuramente para calcular a recompensa
            done: Indica o fim da simulação

    """
    def reset(self):

        self.mesh = Mesh(mesh_shape)
        self.block = self.generate_random_Block()

        self.pos_x = 2
        self.pos_y = self.toTop(self.block, 0)

        score = 0
        observation = self.make_observation()
        done = False

        return observation, score, done

    """
        Executa a próxima ação no ambiente

        Parâmetros:

            action (list com tipo uint): próxima ação a ser executada

        Retorno:

            observation: A observação atual do ambiente
            reward: Recompensa dada pela ação
            done: Indica o fim da simulação
    """

    def step(self,action):

        if action == 0: #DOWN
            #Será implementada após a função render
        elif action == 1: #RIGHT
            pos_x,pos_y = move(block,'RIGHT',pos_x,pos_y)

                if adjust(mesh,block,pos_x,pos_y):
                    pos_x,pos_y = move(block,'LEFT',pos_x,pos_y)

        elif action == 2: #LEFT
            pos_x,pos_y = move(block,'LEFT',pos_x,pos_y)
                
            if(adjust(mesh,block,pos_x,pos_y)):
                pos_x,pos_y = move(block,'RIGHT',pos_x,pos_y)

        elif action == 3: #CLOCKWISE
            rotate(block,'CLOCKWISE')
                
                if(adjust(mesh,block,pos_x,pos_y)):
                    rotate(block,'ANTICLOCKWISE')

        elif action == 4: #ANTICLOCKWISE
            rotate(block,'ANTICLOCKWISE')
                
                if(adjust(mesh,block,pos_x,pos_y)):
                    rotate(block,'CLOCKWISE')
        else:
            raise InvalidAction(str(action), [0,1,2,3,4])

        return observation, reward, done

    """
        Renderiza a o frame atual do ambiente

        Parâmetros
            -------------------------------------
        Retorno
            -------------------------------------
    """
    def render(self):

        return