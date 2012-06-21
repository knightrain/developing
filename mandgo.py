#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import pygame
from pygame.locals import *
import speak
import person

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

    background = pygame.image.load("test/mario/mario_background_01.png").convert()
    background = pygame.transform.smoothscale(background, (640, 480))
    screen.blit(background, (0, 0))

    mario = person.create_person('test/mario.xml')
    princess = person.create_person('test/princess.xml');

    mario.set_state('running')
    mario.rect = Rect(400, 325, 39, 39)
    mario.update_speed(3, 0)

    princess.set_state('still')
    princess.rect = Rect(500, 321, 39, 39)

    speaker = speak.Speaker()
    pygame.mixer.init(speaker.framerate, speaker.sampwidth*8, speaker.nchannels, 4096)

    portrait = None
    text_bg = pygame.Surface((640, 120))
    ar = pygame.PixelArray(text_bg)
    ar[:] = (50, 50, 192)
    del ar
    text_bg.set_alpha(125)

    clock = pygame.time.Clock()

    while True:

        for event in pygame.event.get():
            if event.type in (QUIT, KEYDOWN):
                return

        screen.blit(background, (0, 0))

        if  mario.state == 'running' and mario.rect.right >= princess.rect.left:
            mario.update_speed(0, 0)
            mario.set_state('speaking')
            sound = read_script(speaker)
            portrait = mario.get_portrait();
            portrait = pygame.transform.smoothscale(portrait, (105,240))
        elif mario.state == 'speaking' and not sound.get_busy():
            mario.set_state('still')
            portrait = None

        mario.update()
        screen.blit(mario.image, mario.rect)
        princess.update()
        screen.blit(princess.image, princess.rect)

        if portrait != None:
            screen.blit(text_bg, (0, 360, 640, 120))
            screen.blit(portrait, (0, 240, 105, 240))

        pygame.display.update()

        clock.tick(30)

if __name__ == '__main__':
	main()
