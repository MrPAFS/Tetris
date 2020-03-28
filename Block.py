# -*- coding: utf-8 -*-
"""
Created on Tue Feb 19 10:51:58 2019

@author: Casa
"""

""" 
    Representa um bloco do Tetris

    Atributos:

        color: A cor do bloco
        block: A list correspondente ao bloco
"""
class Block:
    
    """
        Funciona como um switch, para cada tipo de bloco é dado os pontos que dão o formato no vetor

        Argumentos

            block_name: O tipo do bloco (I, T, L-NORMAL, L-INVERTED, S-NORMAL, S-INVERTED ou O)

        Retorno

            ***: Os pontos na list block que dão o formato do bloco
    """
    def __build_block(self,block_name):
        return {
                'I': [(0,2),(1,2),(2,2),(3,2)],
                'T': [(2,1),(2,2),(2,3),(3,2)],
                'L-NORMAL': [(1,2),(2,2),(3,2),(3,3)],
                'L-INVERTED': [(1,2),(2,2),(3,1),(3,2)],
                'S-NORMAL': [(1,1),(2,1),(2,2),(3,2)],
                'S-INVERTED': [(1,3),(2,2),(2,3),(3,2)],
                'O':[(2,1),(2,2),(3,1),(3,2)]} [block_name]
    
    """
    Cria um novo bloco

    Argumentos

        block_name: O tipo do bloco (I, T, L-NORMAL, L-INVERTED, S-NORMAL, S-INVERTED ou O)
        color: A list correspondente ao bloco

    Retorno
    -------------------------------------    
    """
    def __init__(self,block_name,color):
        self.__color = color
        
        self.__block = [[0,0,0,0,0],
                        [0,0,0,0,0],
                        [0,0,0,0,0],
                        [0,0,0,0,0],
                        [0,0,0,0,0]]
        block_index = self.__build_block(block_name)
        
        for i in block_index:
            self.__block[i[0]][i[1]] = 1
    
    """
    Rotaciona o bloco no sentido horário

    Argumentos
    -------------------------------------
    Retorno
    -------------------------------------
    """
    def rotate_clockwise(self):
        self.__block = list(zip(*reversed(self.__block)))
       
    """
    Rotaciona o bloco no sentido anti-horário

    Argumentos
    -------------------------------------
    Retorno
    -------------------------------------
    """ 
    def rotate_anticlockwise(self):
        self.__block =list(reversed(list(zip(*self.__block))))

    """
    Retorna a list correspondente ao bloco

    Argumentos
    -------------------------------------
    Retorno

        self.__block: A list correspondente ao bloco
    
    """ 
    def get_array_of_block(self):
        return self.__block
    
    """
    Retorna a cor do bloco

    Argumentos
    -------------------------------------
    Retorno

        self.__color: A cor do bloco
    
    """
    def get_color(self):
        return self.__color