# -*- coding: utf-8 -*-
"""
Created on Mon Feb 18 21:22:14 2019

@author: Casa
"""
import pygame

colors = [(255,255,255),(0,191,255),(255,0,0),(255,255,0),(0,255,127),(148,0,211),(192,192,192)]
screen_shape = (480,640)
rect_size = 20

pygame.display.init()
background = pygame.display.set_mode(screen_shape)

play = True
while play:
    
    background.fill(colors[0])
    pygame.draw.rect(background,colors[1],(20,0,rect_size,rect_size))
    pygame.display.update()
    
    for event in pygame.event.get():
        print(event)
        
        if event.type == pygame.QUIT:
            play = False
    
pygame.display.quit()