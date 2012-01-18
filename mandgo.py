#!/usr/bin/env python
# -*- coding: cp936 -*-

import os
import sys
import pygame
from pygame.locals import *
import win32com.client 

def load_image(file, pos_x, pox_y, width=None, height=None, number=None):
    try:
        surface = pygame.image.load(file).convert_alpha()
    except pygame.error:
        raise SystemExit('Could not load image "%s" %s'%(file, pygame.get_error()))
    if width == None:
        return surface
    if height == None:
        height = surface.get_height()
 
    return [surface.subsurface(
        Rect((pos_x + i * width, pox_y), (width, height))
        ) for i in xrange(number)]

class Mario(pygame.sprite.Sprite):
    images = []
    speed = 3 
    def __init__(self):
        self.order = 0
        pygame.sprite.Sprite.__init__(self)
        if len(self.images) == 0:
            self.images = load_image("mario/mario_01.jpg",
                    0, 39*2, 39, 39, 3)
        self.image = self.images[self.order]
        self.rect = Rect(0, 325, 39, 39)

    def update(self):
        if self.speed > 0:
            self.rect.left += self.speed
            self.order += 1
       	    if self.order >= len(self.images):
           	    self.order = 0 
       	    self.image = self.images[self.order]
        else:
            self.image = self.images[0]
    
class Princess(pygame.sprite.Sprite):
    images = []
    def __init__(self):
        self.order = 0
        pygame.sprite.Sprite.__init__(self)
        if len(self.images) == 0:
            self.images = load_image("mario/mario_01.jpg",
                    39*9, 39*5, 39, 39, 1)
        self.image = self.images[self.order]
        self.rect = Rect(500, 321, 39, 39)

    def update(self):
        self.order += 1
        if self.order >= len(self.images):
            self.order = 0 
        self.image = self.images[self.order]
    
def set_voice(speaker, voice_id):
    tokens = speaker.GetVoices()
    for token in tokens:
        if token.Id == voice_id:
            speaker.Voice = token
            return
    print("No voice found!")
    
def read_script():
    speaker = win32com.client.Dispatch("SAPI.SpVoice")
    set_voice(speaker, "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\RMTTS_Wang")
    speaker.Speak("我爱你")
    #file_object = open('script.txt')
    #try:
    #    for line in file_object:
    #        process line
    #finally:
    #    file_object.close( )
    

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480), 0, 32)

    background = pygame.image.load("mario/mario_background_01.png").convert()
    background = pygame.transform.smoothscale(background, (640, 480))
    screen.blit(background, (0, 0))

    mario = Mario();
    princess = Princess();

    clock = pygame.time.Clock()

    while True:

        for event in pygame.event.get():
            if event.type in (QUIT, KEYDOWN):
                return

        screen.blit(background, (0, 0))

        if mario.rect.right >= princess.rect.left and mario.speed != 0:
            mario.speed = 0
            read_script()
        mario.update()
        screen.blit(mario.image, mario.rect)
        princess.update()
        screen.blit(princess.image, princess.rect)

        pygame.display.update()

        clock.tick(30)

if __name__ == '__main__':
	main()
