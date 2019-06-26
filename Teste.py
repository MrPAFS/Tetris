# -*- coding: utf-8 -*-
"""
Created on Mon Feb 18 21:22:14 2019

@author: Casa
"""
from threading import Timer

def p():
    print('30 segundos')

t = Timer(30,p);
t.start()