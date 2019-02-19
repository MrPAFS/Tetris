# -*- coding: utf-8 -*-
"""
Created on Mon Feb 18 20:56:13 2019

@author: Casa
"""

import pygame

pygame.display.init()

pygame.display.set_mode((640,640))

play = True

while play:
    for event in pygame.event.get():
        print(event)
        if event.type == pygame.QUIT:
            play = False
        
pygame.display.quit()