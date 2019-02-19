# -*- coding: utf-8 -*-
"""
Created on Tue Feb 19 12:54:46 2019

@author: Casa
"""
import numpy as np
class Mesh:
    def __init__(self,shape=(20,20)):
        self.__edge = 2
        self.__shape = shape
        mesh = np.zeros(shape)
        edge_shapex2 = np.ones((shape[0],2))
        edge_2xshape = np.ones((2,shape[1]+4))
        self.__mesh = np.r_[ edge_2xshape, np.c_[edge_shapex2, mesh, edge_shapex2], edge_2xshape ].astype('int').tolist()
        
    def add_block(self,block,initial_location):
        
        array_of_block = block.get_array_of_block()
        block_size = (len(array_of_block),len(array_of_block[0]))
        
        for i in range(block_size[0]):
            for k in range(block_size[1]):
                if array_of_block[i][k] == 1:
                    self.__mesh[initial_location[0]+i][initial_location[1]+k] = 1
    
    def detect_full_line(self):
        
        full_lines = []
        for i in range(2,self.__shape[0]+2):
            counter = 0
            for k in range(2,self.__shape[1]+2):
                counter += self.__mesh[i][k]
            if counter == self.__shape[1]:
                full_lines.append(i)
            
        for line in full_lines:
            i = line
            while i > 2:
                self.__mesh[i] = self.__mesh[i-1].copy()
                i -= 1
                    
    def get_array_of_mesh(self):
        return self.__mesh
    
    def get_shape(self):
        return self.__shape