# -*- coding: utf-8 -*-
"""
Created on Tue Feb 19 10:51:58 2019

@author: Casa
"""
class Block:
    
    def __build_block(self,block_name):
        return {
                'I': [(0,2),(1,2),(2,2),(3,2)],
                'T': [(2,1),(2,2),(2,3),(3,2)],
                'L-NORMAL': [(1,2),(2,2),(3,2),(3,3)],
                'L-INVERTED': [(1,2),(2,2),(3,1),(3,2)],
                'S-NORMAL': [(1,1),(2,1),(2,2),(3,2)],
                'S-INVERTED': [(1,3),(2,2),(2,3),(3,2)],
                'O':[(2,1),(2,2),(3,1),(3,2)]} [block_name]
        
    def __init__(self,block_name):
        self.__block = [[0,0,0,0,0],
                        [0,0,0,0,0],
                        [0,0,0,0,0],
                        [0,0,0,0,0],
                        [0,0,0,0,0]]
        block_index = self.__build_block(block_name)
        
        for i in block_index:
            self.__block[i[0]][i[1]] = 1
            
    def rotate_clockwise(self):
        self.__block = list(zip(*reversed(self.__block)))
        
    def rotate_anticlockwise(self):
        self.__block =list(reversed(list(zip(*self.__block))))
        
    def get_array_of_block(self):
        return self.__block