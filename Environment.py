# -*- coding: utf-8 -*-
"""
    Contém ambientes de simulação para um apredizado de máquina (Reinforcement Learning)
"""

import pygame
import numpy as np
from random import randint
from random import choice
import time
from Mesh import Mesh
from Block import Block
from EnvironmentExceptions import InvalidAction

"""
    Ambiente para treinamento de uma IA que joga tetris
    
    OBS: O código do arquivo Tetris.py está sendo modificado neste arquivo para melhor adequar para o treinamento de uma rede neural.
"""
class Tetris:
    """
    Gera um bloco de um tipo aleatório e de uma cor aleatória

    Argumentos
    -------------------------------------
    Retorno

        block: O bloco gerado

    """
    def generate_random_Block(self):

        possible_blocs_name = ['I', 'T', 'L-NORMAL', 'L-INVERTED', 'S-NORMAL', 'S-INVERTED', 'O']   
        block_name = choice(possible_blocs_name)

        color = randint(1, 6)

        block = Block(block_name, color)

        how_many_rotation = randint(0, 4)
        for i in range(how_many_rotation):
            block.rotate_clockwise()

        return block

    """
    Função equivalente a um switch do C, dado o tipo do movimento (DOWN, LEFT ou RIGHT) é retornado o vetor respectivo

    Argumentos

        movement: O tipo do movimento(DOWN, LEFT ou RIGHT)

    Retorno

        ***: O vetor respectivo ao movimento
    
    """
    def switch(self,movent):
        return {
                'DOWN':(0,1),
                'LEFT':(-1,0),
                'RIGHT':(1,0)}[movent]
    
    """
    Movimenta o bloco no plano

    Argumentos

        block: O bloco a ser movimentado
        movement: O tipo do movimento (DOWN, LEFT ou RIGHT)
        position_x: A abscissa do ponto inicial do bloco no plano
        position_y: A ordenada do ponto inicial do bloco no plano

    Retorno

        position_x: A nova abscissa do ponto inicial do bloco
        position_y: A nova ordenada do ponto inicial do bloco

    OBS: Verificar arquivo block.py e método reset para entender melhor como funciona um bloco e sua localização
    """
    def move(self,block,movement,position_x,position_y):
        move_x,move_y = self.switch(movement)
        
        position_x += move_x
        position_y += move_y
        
        return (position_x,position_y)

    """
    Rotaciona um bloco no sentido horário ou anti-horário

    Argumentos

        block: O bloco a ser rotacionado
        direction: Define se a rotação é no sentido horário ou anti-horário

    Retorno
    -------------------------------------

    OBS: Ver código Block.py para melhor entender o funcionamento de um bloco
    """
    def rotate(self,block,direction):
        if(direction == 'CLOCKWISE'):
            block.rotate_clockwise()
        elif(direction == 'ANTICLOCKWISE'):
            block.rotate_anticlockwise()
    
    """
    Movimentar ou rotacionar um bloco pode jogar sua parte observável para fora da malha, esse função identifica se ocorreu esse e erro

    Argumentos

        mesh: A malha do jogo
        block: Um bloco do jogo
        zero_mesh: Representa a margem esquerda na tela antes do início da malha
        real_pos_x: A abscissa do ponto inicial do bloco na malha mais a margem esquerda
        pos_y: A ordenada do ponto inicial do bloco na malha
    
    Retorno:

        boolean: Identifica se ocorreu ou não o erro

    """       
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


    """
    Representa o critério que define se um bloco atingiu o estágio para ser adicionada a malha.

    Argumentos
        
        mesh: A malha do jogo
        block: O bloco a ser testado
        zero_mesh: Representa a margem esquerda na tela antes do início da malha
        real_pos_X: A abscissa do ponto inicial do bloco na malha mais a margem esquerda
        pos_y: A ordenada do ponto inicial do bloco na malha

    Retorno

        boolean: Indica se o bloco deve ou não ser adicionado a malha
    
    """
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

    """
    Ajusta o bloco para que sua parte visível esteja na posição correta da tela

    Argumentos

        block: O bloco a ser analisado
        pos_y: A ordenada do ponto inicial do bloco na malha

    Retorno

        pos_y: A nova ordenada do ponto inicial do bloco na malha
    
    """  
    def toTop(self,block,pos_y):
        array_of_block = block.get_array_of_block()
        
        a = 0
        
        while a == 0:
            for i in range(5):
                a += array_of_block[0-pos_y][i]
            if a == 0:
                pos_y -= 1
        
        return pos_y

    """
    Testa se o jogo deve ser finalizado (GAME OVER)

    Argumentos

        mesh: A malha do jogo
        block: O último bloco gerado
        zero_mesh: Representa a margem esquerda na tela antes do início da malha
        real_pos_X: A abscissa do ponto inicial do bloco na malha mais a margem esquerda
        pos_y: A ordenada do ponto inicial do bloco na malha

    Retorno

        boolean: A resultado do teste
    
    """   
    def lose(self,mesh, block,real_pos_x,pos_y,zero_mesh):
        array_of_mesh = mesh.get_array_of_mesh()
        array_of_block = block.get_array_of_block()
        
        pos_x = real_pos_x - zero_mesh
        
        for i in range(4,-1,-1):
            for j in range(5):
                if(array_of_block[i][j] == 1) & (array_of_mesh[i+pos_y][j+pos_x] != 0):
                    return True     
                
        return False

    """
    Cálcula a pontuação obtida dada a quantidade de linhas horizontais preenchidas
    
    Argumentos

        number_of_full_lines: A quantidade de linhas horizontais preenchidas

    Retorno

        ***: A pontuação dada pela quantidade de linhas horizontais preenchidas
    
    """
    def calc_score(self,number_of_full_lines):
        return{0:0,
            1:100,
            2:300,
            3:500,
            4:800
                }[number_of_full_lines]

    """
    Desenha um bloco na tela

    Argumentos

        background: O fundo da tela
        color: Uma lista que contém o correspondente o valor rgb respectivo de block.get_color()*
        square_size: O altura e comprimento, em pixels, das partes do bloco*
        block: O bloco a ser desenhado
        position_x: A abscissa do ponto inicial do bloco na malha mais a margem esquerda
        position_y: A ordenada do ponto inicial do bloco na malha

    Retorno
    -------------------------------------

    *Ver Block.py

    """
    def draw_block(self,background,colors,square_size,block,position_x,position_y):
        array_of_block = block.get_array_of_block()
        for i in range(5):
            for k in range(5):
                if array_of_block[i][k] == 1:
                    pygame.draw.rect(background,colors[block.get_color()],((position_x + k)*square_size,(position_y + i)*square_size, square_size, square_size))

    """
    Desenha a malha na tela

    Argumentos

        background: O fundo da tela
        color: Uma lista que contém o correspondente o valor rgb respectivo dos valores contidos em mesh.get_array_of_mesh()*
        square_size: O altura e comprimento, em pixels, das partes do bloco**
        mesh: A malha do jogo
        zero_mesh: A margem esquerda da malha

    Retorno
    -------------------------------------

    *Ver Mesh.py
    **Ver Block.py

    """
    def draw_mesh(self,background,colors,square_size,mesh,zero_mesh):
        array_of_mesh = mesh.get_array_of_mesh()
        shape = mesh.get_shape()
        
        for i in range(shape[0]):
            for j in range(shape[1]):
                real_pos_x = (j+zero_mesh)*square_size
                pos_y = i*square_size
                pygame.draw.rect(background,colors[int(array_of_mesh[i][j])],(real_pos_x,pos_y, square_size, square_size))
    
    def start_menu(self, background, clock):
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

    """
        Constroi um array que constitui a observação do jogo

        Parâmetros:
        -------------------------------------

        Retorno:
            observation: A observação atual do ambiente
    """
    def make_observation(self):

        array_of_block = self.block.get_array_of_block()
        array_of_mesh = self.mesh.get_array_of_mesh()

        observation = np.zeros(self.mesh_shape, dtype=np.float32)

        for i in range(self.mesh_shape[0]):
            for j in range(self.mesh_shape[1]):
                if (array_of_mesh[i][j] != 0):
                    observation[i][j] = 1

        for i in range(5):
            for j in range(5):
                if array_of_block[i][j] == 1:
                    observation[self.pos_y + i][self.pos_x - self.zero_mesh + j] = 1

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
        self.drop_speed = 1
        self.zero_mesh = 5

        #             WHITE      DeepSkyBlue    RED      YELLOW   SpringGreen  DarkViolet     Silver     Black
        self.colors = [(255,255,255),(0,191,255),(255,0,0),(255,255,0),(0,255,127),(148,0,211),(192,192,192),(0,0,0)]
        self.screen_shape = (500,500)
        self.square_size = 25

        self.begin_render = False

        self.score = -1
        
        return

    """
        Inicia a simulação do jogo tetris

        Parâmetros
        -------------------------------------

        Retorno

            observation: A observação atual do ambiente

    """
    def reset(self):

        self.mesh = Mesh(self.mesh_shape)
        self.block = self.generate_random_Block()

        self.pos_x = 2 + self.zero_mesh
        self.pos_y = self.toTop(self.block, 0)

        self.score = 0
        observation = self.make_observation()

        return observation


    def run_action(self, action):

        if action == 1: #RIGHT
            self.pos_x, self.pos_y = self.move(self.block, 'RIGHT', self.pos_x, self.pos_y)

            if self.adjust(self.mesh, self.block, self.pos_x, self.pos_y, self.zero_mesh):
                self.pos_x, self.pos_y = self.move(self.block, 'LEFT', self.pos_x, self.pos_y)

        elif action == 2: #LEFT
            self.pos_x, self.pos_y = self.move(self.block, 'LEFT', self.pos_x, self.pos_y)
                
            if self.adjust(self.mesh, self.block, self.pos_x, self.pos_y, self.zero_mesh):
                self.pos_x, self.pos_y = self.move(self.block, 'RIGHT', self.pos_x, self.pos_y)

        elif action == 3: #CLOCKWISE
            self.rotate(self.block, 'CLOCKWISE')
                
            if self.adjust(self.mesh, self.block, self.pos_x, self.pos_y, self.zero_mesh):
                self.rotate(self.block, 'ANTICLOCKWISE')

        elif action == 4: #ANTICLOCKWISE
            self.rotate(self.block, 'ANTICLOCKWISE')
                
            if self.adjust(self.mesh, self.block, self.pos_x, self.pos_y, self.zero_mesh):
                self.rotate(self.block, 'CLOCKWISE')
        else:
            raise InvalidAction(action, [0,1,2,3,4])
    
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

        reward = 1
        done = False

        self.run_action(action)
            
        self.pos_y += self.drop_speed
        if(self.adjust(self.mesh,self.block,self.pos_x,self.pos_y, self.zero_mesh)):
            self.pos_y -= self.drop_speed
        
        if self.stopCriterion(self.mesh, self.block, self.pos_x, self.pos_y, self.zero_mesh):
            self.mesh.add_block(self.block, (self.pos_y, self.pos_x - self.zero_mesh))
            reward += self.calc_score(self.mesh.detect_full_line())
            self.block = self.generate_random_Block()
            self.pos_x = 2 + self.zero_mesh
            self.pos_y = self.toTop(self.block, 0)

            if self.lose(self.mesh, self.block, self.pos_x, self.pos_y, self.zero_mesh):
                done = True

        self.score += reward

        observation = self.make_observation()

        return observation, reward, done

    """
        Renderiza a o frame atual do ambiente

        Parâmetros
            -------------------------------------
        Retorno
            -------------------------------------
    """
    def render(self):

        if(not self.begin_render):
            pygame.init()
            self.background = pygame.display.set_mode(self.screen_shape)
            self.score_font = pygame.font.SysFont("monospace", 15)
        
        self.background.fill(self.colors[7])
        self.draw_mesh(self.background,self.colors,self.square_size,self.mesh, self.zero_mesh)
        self.draw_block(self.background,self.colors,self.square_size,self.block,self.pos_x,self.pos_y)
        label = self.score_font.render("Score: " + str(self.score), 1, self.colors[0])
        self.background.blit(label, (0, 0))
        pygame.display.update()

        return
    
    """
    Encerra a tela do jogo

    Argumentos
    -------------------------------------
    Retorno
    -------------------------------------
    """
    def close(self):
        pygame.display.quit()

    """
    Fornece as dimensões do array da observação

    Argumentos
    -------------------------------------
    Retorno
    -------------------------------------
    """
    def observation_shape(self):
        return self.mesh_shape

    """
    Fornece a quantidade total de ações possíveis
    
    Argumentos
    -------------------------------------
    Retorno
    -------------------------------------
    """
    def action_scope_size(self):
        return 5

    """
    Retorna a pontuação total até o momento
    """
    def get_score(self):
        return self.score

    def play(self):
        history = []

        state = self.reset().flatten()

        clock = pygame.time.Clock()
        timer = time.time()

        done = False

        # play = self.start_menu(self.background,clock)
        play = True

        action = 0
        change_state = False
        while play:

            self.render()

            reward = 1
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    play = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == 275: 
                        self.run_action(1)
                        action = 1
                    elif event.key == 276: 
                        self.run_action(2)
                        action = 2
                    elif event.key == 100: 
                        self.run_action(3)
                        action = 3
                    elif event.key == 97: 
                        self.run_action(4)
                        action = 4
            
            if(time.time() - timer >= 0.5):
                self.pos_y += self.drop_speed
                if(self.adjust(self.mesh, self.block, self.pos_x, self.pos_y, self.zero_mesh)):
                    self.pos_y -= self.drop_speed
                timer = time.time()
                change_state = True

            clock.tick(16)

            if self.stopCriterion(self.mesh, self.block, self.pos_x, self.pos_y, self.zero_mesh):
                self.mesh.add_block(self.block, (self.pos_y, self.pos_x - self.zero_mesh))
                reward += self.calc_score(self.mesh.detect_full_line())
                self.block = self.generate_random_Block()
                self.pos_x = 2 + self.zero_mesh
                self.pos_y = self.toTop(self.block, 0)

                if self.lose(self.mesh, self.block, self.pos_x, self.pos_y, self.zero_mesh):
                    done = True
                    play = self.lose_menu(self.background, clock)

            next_state = self.make_observation().flatten()

            if change_state:
                history.append((state, action, reward, next_state, done))
                state = next_state
                action = 0
                change_state = False
                print("History lenght: {}".format(len(history)), end="")
                self.score += reward
        
        self.close()

        return history
