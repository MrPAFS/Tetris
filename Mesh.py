# -*- coding: utf-8 -*-
import numpy as np

""" 
Representa a malha do Tetris, aonde se encaixam os blocos

Atributos:
    shape: As dimensões da malha
    mesh: O numpy array correspondente a malha
"""
class Mesh:

    """ 
    Inicia uma nova malha

    Argumentos

        shape: Indica as dimensões da malha
    
    Retorno
    -------------------------------------
    """
    def __init__(self,shape=(20,20)):
        self.__shape = shape
        self.__mesh = np.zeros(shape)
        
    """
    Adiciona um bloco a malha, a partir desse momento ele se torna estático e se torna parte da malha

    Argumentos

        block: O bloco a ser adicionado a malha
        initial_location: O bloco e composto por 25 partes distribuidas de bidimensional 5x5 (ver Block.py), a variável indica a localização da primeira parte

    Retorno
    -------------------------------------
    """
    def add_block(self,block,initial_location):
        
        array_of_block = block.get_array_of_block()
        block_size = (len(array_of_block),len(array_of_block[0]))
        
        for i in range(block_size[0]):
            
            # if initial_location[0]+i >= self.__shape[0]:
            #     break
            # elif initial_location[0]+i < 0:
            #     continue
                
            for k in range(block_size[1]):
                
                # if initial_location[1]+k >= self.__shape[1]:
                #     break
                # elif initial_location[1]+k < 0:
                #     continue
                
                if array_of_block[i][k] == 1:
                    self.__mesh[initial_location[0]+i][initial_location[1]+k] = block.get_color()
    
    """
    Detecta na malha as linhas completas na horizontal, formadas pelos blocos adicionados à malha, e as apagam

    Argumentos:
    -------------------------------------
    Retorno:

        len(full_lines): A quantidade encontrada dessas linhas
    """
    def detect_full_line(self):
        full_lines = []
        for i in range(0,self.__shape[0]):
            counter = 0
            for k in range(0,self.__shape[1]):
                if(self.__mesh[i][k] != 0):
                    counter += 1
                    #counter += self.__mesh[i][k]
            if counter == self.__shape[1]:
                full_lines.append(i)
            
        for line in full_lines:
            i = line
            while i > 0:
                self.__mesh[i] = self.__mesh[i-1].copy()
                i -= 1
        return len(full_lines)

    """
    Retorna o numpy array correspondente à malha

    Argumentos:
    -------------------------------------
    Retorno:

        self.__mesh: O numpy array correspondente à malha

    """         
    def get_array_of_mesh(self):
        return self.__mesh
    
    """
    Retorna as dimensões da malha

    Argumentos:
    -------------------------------------
    Retorno:

        self.__shape: As dimensões da malha

    """
    def get_shape(self):
        return self.__shape