# -*- coding: utf-8 -*-
"""
Created on Mon Feb 18 21:22:14 2019

@author: Casa
"""
from Block import Block
from Mesh import Mesh

mesh = Mesh((5,5))

for i in mesh.get_array_of_mesh():
    print(i)
    
print()

block = Block('O')

mesh.add_block(block,(3,1))

for i in mesh.get_array_of_mesh():
    print(i)
print()
    
mesh.add_block(block,(3,3))

for i in mesh.get_array_of_mesh():
    print(i)
    
print()

block = Block('I')
    
mesh.add_block(block,(3,4))

for i in mesh.get_array_of_mesh():
    print(i)
    
print()

mesh.detect_full_line()

for i in mesh.get_array_of_mesh():
    print(i)