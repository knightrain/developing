#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import pygame
from pygame.locals import *
import win32com.client 
import speak

STILL = 0
MOVING = 1
SPEAKING = 2

def load_resource_image(file):
    try:
        resource = pygame.image.load(file).convert_alpha()
    except pygame.error:
        raise SystemExit('Could not load image "%s" %s'%(file, pygame.get_error()))
    return resource

def load_image(resource, pos_x, pox_y, width=None, height=None, number=None):
    if width == None or height == None:
        return None
 
    return [resource.subsurface(
        Rect((pos_x + i * width, pox_y), (width, height))
        ) for i in xrange(number)]

class Figure(pygame.sprite.Sprite):
    def __init__(self, name):
        self.name = name
        self.status = STILL

class Mario(Figure):
    xspeed = 3
    yspeed = 0
    g = 200 
    def __init__(self, resources):
        self.order = 0
        Figure.__init__(self, "Mario")
        self.still_image = load_image(resources, 0, 39*2, 39, 39, 1)[0]
        self.running_images = load_image(resources, 0, 39*2, 39, 39, 3)
        self.speaking_images = load_image(resources, 39*3, 39*2, 39, 39, 1)
        self.image = self.still_image
        self.rect = Rect(400, 325, 39, 39)

    def update_moving(self):
        self.rect.left += self.xspeed
        self.order += 1
       	if self.order >= 3:
            self.order = 0 
        self.image = self.running_images[self.order]

    def update_speaking(self):
        if self.sound and self.sound.get_busy():
            self.sound_end = 0
        else:
            self.sound_end = 1

        if self.sound_end == 0 and self.yspeed == 0:
            self.yspeed = -100
            self.speech_end = 0
            self.base_time = pygame.time.get_ticks()
            self.base_top = self.rect.top
            self.image = self.speaking_images[0]
        elif self.yspeed == 0:
            self.speech_end = 1
        else:
            time_passed = pygame.time.get_ticks() - self.base_time 
            time_passed /= 1000.0
            d = self.yspeed*time_passed + self.g * time_passed * time_passed / 2
            print d, time_passed
            self.rect.top = self.base_top + int(d)
            if self.rect.top > self.base_top:
                self.rect.top = self.base_top
                self.image = self.running_images[0]
                self.yspeed = 0

    def update(self):
        if self.status == MOVING:
            self.update_moving()
        elif self.status == SPEAKING:
            self.update_speaking()
        else:
            self.image = self.still_image
    
class Princess(Figure):
    def __init__(self, resources):
        self.order = 0
        Figure.__init__(self, "Princess")
        self.images = load_image(resources, 39*9, 39*5, 39, 39, 1)
        self.image = self.images[self.order]
        self.rect = Rect(500, 321, 39, 39)

    def update(self):
        self.order += 1
        if self.order >= len(self.images):
            self.order = 0 
        self.image = self.images[self.order]
    
def read_script(speaker):
    text = speaker.preprocess_str(u"我爱你")
    nsamps, channel = speaker.speak_words(pygame.mixer, text)
    sound_length = 1000*nsamps/speaker.framerate
    return channel
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

    resources = load_resource_image("mario/mario_01.jpg")
    mario = Mario(resources);
    mario.status = MOVING
    princess = Princess(resources);

    speaker = speak.Speaker()
    pygame.mixer.init(speaker.framerate, speaker.sampwidth*8, speaker.nchannels, 4096)

    clock = pygame.time.Clock()

    while True:

        for event in pygame.event.get():
            if event.type in (QUIT, KEYDOWN):
                return

        screen.blit(background, (0, 0))

        if  mario.status == MOVING and mario.rect.right >= princess.rect.left:
            mario.status = SPEAKING
            mario.sound = read_script(speaker)
        elif mario.status == SPEAKING and mario.speech_end == 1:
            mario.status == STILL

        mario.update()
        screen.blit(mario.image, mario.rect)
        princess.update()
        screen.blit(princess.image, princess.rect)

        pygame.display.update()

        clock.tick(30)

if __name__ == '__main__':
	main()
